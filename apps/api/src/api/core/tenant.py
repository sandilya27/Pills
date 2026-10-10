from datetime import datetime, timezone
from typing import Annotated, Optional
from uuid import UUID
import jwt
from fastapi import Depends, Header, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, select

from api.config import get_settings
from api.db.models import Member, Organization, Session, User
from api.db.session import get_db
from forge.tenant import TenantContext

settings = get_settings()
security = HTTPBearer(auto_error=False)


def _safe_uuid(val: str | UUID) -> UUID:
    if isinstance(val, UUID):
        return val
    try:
        return UUID(str(val))
    except ValueError:
        # Generate a deterministic UUID if string is not standard UUID format
        import uuid
        return uuid.uuid5(uuid.NAMESPACE_DNS, str(val))


async def get_tenant_context(
    request: Request,
    auth: Annotated[Optional[HTTPAuthorizationCredentials], Depends(security)],
    db: Annotated[AsyncSession, Depends(get_db)],
    x_organization_id: Annotated[Optional[str], Header(alias="X-Organization-Id")] = None,
    x_organization_slug: Annotated[Optional[str], Header(alias="X-Organization-Slug")] = None,
) -> TenantContext:
    """FastAPI Dependency Injection for TenantContext.
    
    Validates organization boundaries on incoming requests.
    Extracts the authenticated user, verifies organization membership,
    and returns a strictly scoped TenantContext.
    
    Raises:
        HTTPException 401: Missing, invalid, or expired credentials
        HTTPException 403: User does not belong to requested organization (tenant boundary violation)
        HTTPException 404: Requested organization does not exist
    """
    token: Optional[str] = None
    if auth and auth.credentials:
        token = auth.credentials
    else:
        # Check cookie fallback for BetterAuth session
        token = request.cookies.get("better-auth.session_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Provide Bearer token or session cookie.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 1. First attempt: verify if token is a signed JWT
    user_id: Optional[str] = None
    org_id_claim: Optional[str] = None
    org_slug_claim: Optional[str] = None
    role_claim: Optional[str] = None

    try:
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=["HS256"],
            options={"verify_exp": True},
        )
        user_id = payload.get("sub") or payload.get("userId")
        org_id_claim = payload.get("org_id") or payload.get("activeOrganizationId")
        org_slug_claim = payload.get("org_slug")
        role_claim = payload.get("role", "member")
    except (jwt.PyJWTError, Exception):
        # Not a JWT or invalid JWT; fall back to database session token lookup
        pass

    # 2. Database session lookup if not resolved via JWT
    if not user_id:
        stmt = select(Session).where(col(Session.token) == token)
        res = await db.execute(stmt)
        session_record = res.scalar_one_or_none()

        if not session_record:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid session token.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        now = datetime.now(timezone.utc)
        expires_at = session_record.expiresAt
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        if expires_at < now:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session token has expired.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_id = session_record.userId
        org_id_claim = session_record.activeOrganizationId

    # Target organization resolution:
    # Precedence: Header X-Organization-Id / Slug > session/JWT claim
    target_org: Optional[Organization] = None

    if x_organization_id:
        res = await db.execute(select(Organization).where(col(Organization.id) == x_organization_id))
        target_org = res.scalar_one_or_none()
        if not target_org:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Organization with id '{x_organization_id}' not found.",
            )
    elif x_organization_slug:
        res = await db.execute(select(Organization).where(col(Organization.slug) == x_organization_slug))
        target_org = res.scalar_one_or_none()
        if not target_org:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Organization with slug '{x_organization_slug}' not found.",
            )
    elif org_id_claim:
        res = await db.execute(select(Organization).where(col(Organization.id) == org_id_claim))
        target_org = res.scalar_one_or_none()
        if not target_org and org_slug_claim:
            res = await db.execute(select(Organization).where(col(Organization.slug) == org_slug_claim))
            target_org = res.scalar_one_or_none()

    if not target_org:
        # Check if user has an active membership in any organization
        membership_res = await db.execute(
            select(Member).where(col(Member.userId) == user_id).limit(1)
        )
        first_membership = membership_res.scalar_one_or_none()
        if first_membership:
            org_res = await db.execute(
                select(Organization).where(col(Organization.id) == first_membership.organizationId)
            )
            target_org = org_res.scalar_one_or_none()

    if not target_org:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No organization workspace associated with this user session.",
        )

    # 3. STRICT TENANT BOUNDARY CHECK:
    # Verify user is explicitly a member of the resolved organization in the database
    member_stmt = select(Member).where(
        col(Member.organizationId) == target_org.id,
        col(Member.userId) == user_id,
    )
    member_res = await db.execute(member_stmt)
    membership = member_res.scalar_one_or_none()

    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Tenant boundary violation: User does not belong to organization '{target_org.slug}'.",
        )

    role = membership.role or role_claim or "member"
    permissions = ["read", "write"] if role in ("owner", "admin") else ["read"]

    return TenantContext(
        org_id=_safe_uuid(target_org.id),
        org_slug=target_org.slug,
        user_id=_safe_uuid(user_id),
        user_role=role,
        permissions=permissions,
    )


TenantContextDep = Annotated[TenantContext, Depends(get_tenant_context)]

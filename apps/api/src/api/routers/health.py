from datetime import datetime, timezone
from typing import Any, Dict
from fastapi import APIRouter, status
from pydantic import BaseModel

from api.core.tenant import TenantContextDep
from api.db.session import check_db_health, check_redis_health

router = APIRouter(prefix="", tags=["Health"])


class PublicHealthResponse(BaseModel):
    status: str
    timestamp: str
    services: Dict[str, str]


class TenantHealthResponse(BaseModel):
    status: str
    timestamp: str
    tenant: Dict[str, Any]
    services: Dict[str, str]


@router.get("/health", response_model=PublicHealthResponse, status_code=status.HTTP_200_OK)
async def public_healthcheck() -> PublicHealthResponse:
    """Public system healthcheck inspecting database and redis connectivity."""
    db_ok = await check_db_health()
    redis_ok = await check_redis_health()

    return PublicHealthResponse(
        status="healthy" if (db_ok and redis_ok) else "degraded",
        timestamp=datetime.now(timezone.utc).isoformat(),
        services={
            "database": "connected" if db_ok else "unreachable",
            "redis": "connected" if redis_ok else "unreachable",
        },
    )


@router.get(
    "/health/tenant",
    response_model=TenantHealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Tenant-Authenticated Healthcheck",
)
async def tenant_authenticated_healthcheck(
    tenant: TenantContextDep,
) -> TenantHealthResponse:
    """Tenant-authenticated ping verifying organization context scoping and boundaries."""
    db_ok = await check_db_health()
    redis_ok = await check_redis_health()

    return TenantHealthResponse(
        status="healthy",
        timestamp=datetime.now(timezone.utc).isoformat(),
        tenant={
            "org_id": str(tenant.org_id),
            "org_slug": tenant.org_slug,
            "user_id": str(tenant.user_id),
            "user_role": tenant.user_role,
            "permissions": tenant.permissions,
        },
        services={
            "database": "connected" if db_ok else "unreachable",
            "redis": "connected" if redis_ok else "unreachable",
        },
    )

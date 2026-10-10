from datetime import datetime, timedelta, timezone
from uuid import uuid4
import jwt
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool
from sqlmodel import SQLModel

from api.config import get_settings
from api.db.models import Member, Organization, Session, User
import api.db.session as db_session_module
from api.main import app

settings = get_settings()

test_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    poolclass=NullPool,
)

test_session_factory = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@pytest_asyncio.fixture(autouse=True)
async def setup_test_db(monkeypatch):
    monkeypatch.setattr(db_session_module, "engine", test_engine)
    monkeypatch.setattr(db_session_module, "async_session_factory", test_session_factory)
    yield
    await test_engine.dispose()


@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_public_healthcheck(async_client: AsyncClient):
    """Verify that public healthcheck returns healthy status and service connectivity."""
    response = await async_client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["services"]["database"] == "connected"
    assert data["services"]["redis"] == "connected"


@pytest.mark.asyncio
async def test_tenant_healthcheck_unauthenticated(async_client: AsyncClient):
    """Verify that requests without credentials fail with 401 Unauthorized."""
    response = await async_client.get("/api/v1/health/tenant")
    assert response.status_code == 401
    assert "Authentication required" in response.json()["detail"]


@pytest.mark.asyncio
async def test_tenant_healthcheck_invalid_token(async_client: AsyncClient):
    """Verify that requests with invalid credentials fail with 401 Unauthorized."""
    headers = {"Authorization": "Bearer invalid_garbage_token"}
    response = await async_client.get("/api/v1/health/tenant", headers=headers)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_tenant_healthcheck_cross_tenant_forbidden(async_client: AsyncClient):
    """Verify that a user cannot access an organization they do not belong to (403 Forbidden)."""
    user_id = str(uuid4())
    org_a_id = str(uuid4())
    org_b_id = str(uuid4())

    async with test_session_factory() as session:
        user = User(id=user_id, name="Alice", email=f"alice-{user_id[:8]}@example.com")
        org_a = Organization(id=org_a_id, name="Org A", slug=f"org-a-{org_a_id[:8]}")
        org_b = Organization(id=org_b_id, name="Org B", slug=f"org-b-{org_b_id[:8]}")
        session.add_all([user, org_a, org_b])
        await session.flush()

        member_a = Member(id=str(uuid4()), organizationId=org_a_id, userId=user_id, role="member")
        session.add(member_a)
        await session.commit()

    token = jwt.encode(
        {
            "sub": user_id,
            "org_id": org_b_id,
            "org_slug": org_b.slug,
            "role": "member",
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        },
        settings.BETTER_AUTH_SECRET,
        algorithm="HS256",
    )

    headers = {"Authorization": f"Bearer {token}", "X-Organization-Id": org_b_id}
    response = await async_client.get("/api/v1/health/tenant", headers=headers)
    assert response.status_code == 403
    assert "Tenant boundary violation" in response.json()["detail"]


@pytest.mark.asyncio
async def test_tenant_healthcheck_authorized_via_jwt(async_client: AsyncClient):
    """Verify that an authenticated user receives validated tenant context via signed JWT."""
    user_id = str(uuid4())
    org_id = str(uuid4())
    org_slug = f"acme-{org_id[:8]}"

    async with test_session_factory() as session:
        user = User(id=user_id, name="Bob", email=f"bob-{user_id[:8]}@example.com")
        org = Organization(id=org_id, name="Acme Corp", slug=org_slug)
        session.add_all([user, org])
        await session.flush()

        member = Member(id=str(uuid4()), organizationId=org_id, userId=user_id, role="owner")
        session.add(member)
        await session.commit()

    token = jwt.encode(
        {
            "sub": user_id,
            "org_id": org_id,
            "org_slug": org_slug,
            "role": "owner",
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        },
        settings.BETTER_AUTH_SECRET,
        algorithm="HS256",
    )

    headers = {"Authorization": f"Bearer {token}", "X-Organization-Id": org_id}
    response = await async_client.get("/api/v1/health/tenant", headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert data["tenant"]["org_id"] == org_id
    assert data["tenant"]["org_slug"] == org_slug
    assert data["tenant"]["user_id"] == user_id
    assert data["tenant"]["user_role"] == "owner"
    assert "read" in data["tenant"]["permissions"]
    assert "write" in data["tenant"]["permissions"]
    assert data["services"]["database"] == "connected"
    assert data["services"]["redis"] == "connected"


@pytest.mark.asyncio
async def test_tenant_healthcheck_authorized_via_db_session(async_client: AsyncClient):
    """Verify that an authenticated user receives validated tenant context via BetterAuth DB session."""
    user_id = str(uuid4())
    org_id = str(uuid4())
    org_slug = f"globex-{org_id[:8]}"
    session_token = f"sess_{uuid4()}"

    async with test_session_factory() as session:
        user = User(id=user_id, name="Charlie", email=f"charlie-{user_id[:8]}@example.com")
        org = Organization(id=org_id, name="Globex", slug=org_slug)
        session.add_all([user, org])
        await session.flush()

        member = Member(id=str(uuid4()), organizationId=org_id, userId=user_id, role="admin")
        db_session = Session(
            id=str(uuid4()),
            userId=user_id,
            token=session_token,
            expiresAt=datetime.now(timezone.utc) + timedelta(days=7),
            activeOrganizationId=org_id,
        )
        session.add_all([member, db_session])
        await session.commit()

    headers = {"Authorization": f"Bearer {session_token}"}
    response = await async_client.get("/api/v1/health/tenant", headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert data["tenant"]["org_id"] == org_id
    assert data["tenant"]["org_slug"] == org_slug
    assert data["tenant"]["user_id"] == user_id
    assert data["tenant"]["user_role"] == "admin"

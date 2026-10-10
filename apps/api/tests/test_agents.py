from datetime import datetime, timedelta, timezone
from uuid import uuid4
import jwt
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool
from sqlmodel import SQLModel, select

from api.config import get_settings
from api.db.models import Agent, Member, Organization, Session, User
import api.db.session as db_session_module
from api.db.seed import seed
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


@pytest.fixture
def auth_headers():
    token = jwt.encode(
        {
            "sub": "a0000000-0000-0000-0000-000000000001",
            "org_id": "b0000000-0000-0000-0000-000000000001",
            "org_slug": "acme-cybernetics",
            "role": "owner",
            "exp": (datetime.now(timezone.utc) + timedelta(hours=1)).timestamp(),
        },
        settings.BETTER_AUTH_SECRET,
        algorithm="HS256",
    )
    return {
        "Authorization": f"Bearer {token}",
        "X-Organization-Id": "b0000000-0000-0000-0000-000000000001",
    }


@pytest.mark.asyncio
async def test_seed_founding_agents():
    """Verify that database seeding creates the 7 founding agents under the demo organization."""
    await seed()

    async with test_session_factory() as session:
        org_id = "b0000000-0000-0000-0000-000000000001"
        res = await session.execute(select(Agent).where(Agent.org_id == org_id))
        agents = res.scalars().all()

        assert len(agents) == 7
        agent_names = {a.name for a in agents}
        expected_names = {"Dex", "Cipher", "Pulse", "Nootrop", "Remedy", "Aura", "Dose"}
        assert agent_names == expected_names

        # Verify specific capsule identities
        dex = next(a for a in agents if a.name == "Dex")
        assert dex.slug == "dex"
        assert dex.avatar_seed == "DexLead"
        assert dex.accent_color.upper() == "#00F0FF"
        assert dex.body_silhouette == "pill"
        assert dex.model_name == "claude-3-7-sonnet"
        assert dex.status == "idle"

        cipher = next(a for a in agents if a.name == "Cipher")
        assert cipher.slug == "cipher"
        assert cipher.avatar_seed == "CipherSec"
        assert cipher.accent_color.upper() == "#FF2E63"
        assert cipher.body_silhouette == "column"


@pytest.mark.asyncio
async def test_get_agents_unauthenticated(async_client: AsyncClient):
    """Verify that GET /api/v1/agents requires authentication."""
    response = await async_client.get("/api/v1/agents")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_agents_tenant_scoped(async_client: AsyncClient, auth_headers):
    """Verify that authenticated requests return the founding agents for the tenant."""
    await seed()

    response = await async_client.get("/api/v1/agents", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 7

    slugs = [item["slug"] for item in data]
    assert "dex" in slugs
    assert "cipher" in slugs
    assert "pulse" in slugs
    assert "remedy" in slugs
    assert "nootrop" in slugs
    assert "aura" in slugs
    assert "dose" in slugs

    # Check serialization schema
    sample = data[0]
    assert "id" in sample
    assert "name" in sample
    assert "slug" in sample
    assert "role" in sample
    assert "tagline" in sample
    assert "system_prompt" in sample
    assert "avatar_seed" in sample
    assert "accent_color" in sample
    assert "body_silhouette" in sample
    assert "status" in sample


@pytest.mark.asyncio
async def test_get_agents_multi_tenant_isolation(async_client: AsyncClient):
    """Verify strict tenant isolation: an agent in Org B is never returned to Org A."""
    async with test_session_factory() as session:
        # Create second organization and user
        org_b_id = str(uuid4())
        user_b_id = str(uuid4())

        org_b_slug = f"beta-dynamics-{org_b_id}"
        org_b = Organization(id=org_b_id, name="Beta Dynamics", slug=org_b_slug)
        user_b = User(id=user_b_id, name="Beta User", email=f"beta-{user_b_id}@dynamics.corp")
        member_b = Member(id=str(uuid4()), organizationId=org_b_id, userId=user_b_id, role="owner")

        # Custom agent only in Org B
        agent_b = Agent(
            id=str(uuid4()),
            org_id=org_b_id,
            name="Shadow",
            slug="shadow",
            role="Stealth Auditor",
            system_prompt="You are Shadow.",
            avatar_seed="ShadowAgent",
            accent_color="#333333",
            body_silhouette="column",
        )

        session.add_all([org_b, user_b, member_b, agent_b])
        await session.commit()

    token_b = jwt.encode(
        {
            "sub": user_b_id,
            "org_id": org_b_id,
            "org_slug": org_b_slug,
            "role": "owner",
            "exp": (datetime.now(timezone.utc) + timedelta(hours=1)).timestamp(),
        },
        settings.BETTER_AUTH_SECRET,
        algorithm="HS256",
    )

    headers_b = {
        "Authorization": f"Bearer {token_b}",
        "X-Organization-Id": org_b_id,
    }

    response_b = await async_client.get("/api/v1/agents", headers=headers_b)
    assert response_b.status_code == 200
    data_b = response_b.json()

    # Org B must only see Shadow, not Dex or Cipher from Org A
    assert len(data_b) == 1
    assert data_b[0]["name"] == "Shadow"
    assert data_b[0]["slug"] == "shadow"

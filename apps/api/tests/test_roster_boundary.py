from uuid import uuid4

import pytest
from sqlmodel import select

from api.db.models import Agent, Organization
from api.db.seed import seed
from test_agents import (
    async_client,
    auth_headers,
    setup_test_db,
    test_session_factory as agent_session_factory,
)


@pytest.mark.asyncio
async def test_roster_rejects_unrelated_organization(async_client, auth_headers):
    org_id = str(uuid4())
    async with agent_session_factory() as db:
        db.add(Organization(id=org_id, name="Private workspace", slug=f"private-{org_id}"))
        await db.commit()
    response = await async_client.get(
        "/api/v1/agents", headers={**auth_headers, "X-Organization-Id": org_id}
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_repeat_seed_preserves_personas_and_status(async_client, auth_headers):
    await seed()
    await seed()
    response = await async_client.get("/api/v1/agents", headers=auth_headers)
    assert response.status_code == 200
    pills = response.json()
    assert len(pills) == 7
    assert len({pill["system_prompt"] for pill in pills}) == 7
    assert len({pill["body_color"] for pill in pills}) == 7

    async with agent_session_factory() as db:
        result = await db.execute(select(Agent).where(
            Agent.org_id == auth_headers["X-Organization-Id"], Agent.slug == "dex"
        ))
        dex = result.scalar_one()
        original_status = dex.status
        try:
            dex.status = "awaiting_approval"
            await db.commit()
            await seed()
            response = await async_client.get("/api/v1/agents", headers=auth_headers)
            assert next(p for p in response.json() if p["slug"] == "dex")["status"] == "awaiting_approval"
        finally:
            dex.status = original_status
            await db.commit()

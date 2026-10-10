from typing import Annotated, Literal

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, select

from api.core.tenant import TenantContextDep
from api.db.models import Agent
from api.db.session import get_db

router = APIRouter(tags=["agents"])


class AgentResponse(SQLModel):
    id: str
    name: str
    slug: str
    role: str
    tagline: str
    system_prompt: str
    avatar_seed: str
    accent_color: str
    body_color: str
    body_silhouette: str
    status: Literal["idle", "thinking", "executing_tool", "awaiting_approval"]


@router.get("/agents", response_model=list[AgentResponse])
async def list_agents(tenant: TenantContextDep, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(Agent).where(Agent.org_id == str(tenant.org_id)).order_by(Agent.name)
    )
    return result.scalars().all()

import asyncio
from datetime import datetime, timedelta, timezone
from sqlmodel import SQLModel, select
from api.db.models import Agent, Organization, User, Member, Session
from api.db import session as db_session


async def seed():
    async with db_session.engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    async with db_session.async_session_factory() as session:
        user_id = "a0000000-0000-0000-0000-000000000001"
        org_id = "b0000000-0000-0000-0000-000000000001"
        session_token = "sess_demo_alex_vance_acme_cybernetics"

        # 1. Ensure User exists
        existing_user = await session.execute(select(User).where(User.id == user_id))
        if not existing_user.scalar_one_or_none():
            user = User(
                id=user_id,
                name="Alex Vance",
                email="alex@acme.corp",
                emailVerified=True,
            )
            session.add(user)

        # 2. Ensure Organization exists
        existing_org = await session.execute(select(Organization).where(Organization.id == org_id))
        if not existing_org.scalar_one_or_none():
            org = Organization(
                id=org_id,
                name="Acme Cybernetics",
                slug="acme-cybernetics",
            )
            session.add(org)

        await session.commit()

        # 3. Ensure Member exists
        existing_member = await session.execute(
            select(Member).where(Member.userId == user_id, Member.organizationId == org_id)
        )
        if not existing_member.scalar_one_or_none():
            member = Member(
                id="m0000000-0000-0000-0000-000000000001",
                organizationId=org_id,
                userId=user_id,
                role="owner",
            )
            session.add(member)

        # 4. Ensure Session exists
        existing_session = await session.execute(select(Session).where(Session.token == session_token))
        if not existing_session.scalar_one_or_none():
            demo_session = Session(
                id="s0000000-0000-0000-0000-000000000001",
                userId=user_id,
                token=session_token,
                expiresAt=datetime.now(timezone.utc) + timedelta(days=365),
                activeOrganizationId=org_id,
            )
            session.add(demo_session)

        await session.commit()
        for name, role, focus, seed_name, body, accent, silhouette in FOUNDING_PILLS:
            existing = await session.execute(
                select(Agent).where(Agent.org_id == org_id, Agent.slug == name.lower())
            )
            if not existing.scalar_one_or_none():
                session.add(Agent(
                    org_id=org_id, name=name, slug=name.lower(), role=role, tagline=focus,
                    system_prompt=f"You are {name}, the {role} Pill. {focus}. Work within your organization's permissions and explain your findings clearly.",
                    avatar_seed=seed_name, body_color=body, accent_color=accent,
                    body_silhouette=silhouette,
                ))
        await session.commit()
        print("Database seeded successfully with demo organization, user, and founding Pills.")


FOUNDING_PILLS = [
    ("Dex", "Team Lead", "Coordinate initiatives, delegate work, and synthesize findings", "DexLead", "#1d4ed8", "#00F0FF", "pill"),
    ("Cipher", "Security & Compliance", "Audit code, dependencies, and least privilege", "CipherSec", "#059669", "#FF2E63", "column"),
    ("Pulse", "SRE & Infrastructure", "Monitor services and diagnose operational incidents", "PulseSRE", "#d97706", "#fb923c", "pill"),
    ("Remedy", "Codebase Architect", "Diagnose regressions and design maintainable fixes", "RemedyCode", "#be123c", "#fb7185", "pill"),
    ("Nootrop", "Research & Knowledge", "Investigate primary sources and build shared knowledge", "NootropResearch", "#7c3aed", "#818cf8", "pill"),
    ("Aura", "Product Strategist", "Turn ideas into specifications and user stories", "AuraProduct", "#c026d3", "#c084fc", "pill"),
    ("Dose", "Automation", "Automate repeatable workflows and scheduled operations", "DoseAuto", "#0d9488", "#94a3b8", "pill"),
]


if __name__ == "__main__":
    asyncio.run(seed())

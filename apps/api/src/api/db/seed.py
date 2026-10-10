import asyncio
from datetime import datetime, timedelta, timezone
from sqlmodel import SQLModel, select
from api.db.models import Organization, User, Member, Session
from api.db.session import engine, async_session_factory


async def seed():
    async with async_session_factory() as session:
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
            db_session = Session(
                id="s0000000-0000-0000-0000-000000000001",
                userId=user_id,
                token=session_token,
                expiresAt=datetime.now(timezone.utc) + timedelta(days=365),
                activeOrganizationId=org_id,
            )
            session.add(db_session)

        await session.commit()
        print("Database seeded successfully with demo organization and user.")


if __name__ == "__main__":
    asyncio.run(seed())

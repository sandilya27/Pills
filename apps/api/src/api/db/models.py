from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import DateTime, func


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Organization(SQLModel, table=True):
    __tablename__ = "organization"

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    name: str = Field(index=True)
    slug: str = Field(unique=True, index=True)
    logo: Optional[str] = Field(default=None)
    extra_metadata: Optional[str] = Field(default=None, sa_column_kwargs={"name": "metadata"})
    createdAt: datetime = Field(
        default_factory=_utc_now,
        sa_column=Column("createdAt", DateTime(timezone=True), server_default=func.now()),
    )


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    name: str
    email: str = Field(unique=True, index=True)
    emailVerified: bool = Field(default=False, sa_column_kwargs={"name": "emailVerified"})
    image: Optional[str] = Field(default=None)
    createdAt: datetime = Field(
        default_factory=_utc_now,
        sa_column=Column("createdAt", DateTime(timezone=True), server_default=func.now()),
    )
    updatedAt: datetime = Field(
        default_factory=_utc_now,
        sa_column=Column("updatedAt", DateTime(timezone=True), server_default=func.now(), onupdate=func.now()),
    )


class Session(SQLModel, table=True):
    __tablename__ = "session"

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    userId: str = Field(index=True, sa_column_kwargs={"name": "userId"})
    token: str = Field(unique=True, index=True)
    expiresAt: datetime = Field(sa_column=Column("expiresAt", DateTime(timezone=True)))
    ipAddress: Optional[str] = Field(default=None, sa_column_kwargs={"name": "ipAddress"})
    userAgent: Optional[str] = Field(default=None, sa_column_kwargs={"name": "userAgent"})
    activeOrganizationId: Optional[str] = Field(default=None, sa_column_kwargs={"name": "activeOrganizationId"})
    createdAt: datetime = Field(
        default_factory=_utc_now,
        sa_column=Column("createdAt", DateTime(timezone=True), server_default=func.now()),
    )
    updatedAt: datetime = Field(
        default_factory=_utc_now,
        sa_column=Column("updatedAt", DateTime(timezone=True), server_default=func.now()),
    )


class Member(SQLModel, table=True):
    __tablename__ = "member"

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    organizationId: str = Field(index=True, sa_column_kwargs={"name": "organizationId"})
    userId: str = Field(index=True, sa_column_kwargs={"name": "userId"})
    role: str = Field(default="member")
    createdAt: datetime = Field(
        default_factory=_utc_now,
        sa_column=Column("createdAt", DateTime(timezone=True), server_default=func.now()),
    )

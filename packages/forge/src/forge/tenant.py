from uuid import UUID
from pydantic import BaseModel, Field


class TenantContext(BaseModel):
    """Authenticated organization boundary injected into requests and workers.
    
    Strictly isolates all tenant-scoped queries, agent executions, and tool permissions
    to prevent cross-tenant data leakage.
    """
    org_id: UUID = Field(..., description="Unique organization UUID")
    org_slug: str = Field(..., description="URL-friendly organization identifier")
    user_id: UUID = Field(..., description="Authenticated user UUID")
    user_role: str = Field(default="member", description="Role within the organization (e.g. owner, admin, member)")
    permissions: list[str] = Field(default_factory=list, description="Explicit permissions granted to the user in this organization")

    def has_permission(self, permission: str) -> bool:
        """Check if tenant context includes a specific permission."""
        return permission in self.permissions or self.user_role in ("owner", "admin")

    def validate_same_tenant(self, target_org_id: UUID) -> bool:
        """Verify that target resource belongs strictly to this tenant context."""
        return self.org_id == target_org_id

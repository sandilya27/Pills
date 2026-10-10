export interface TenantContextPayload {
  org_id: string;
  org_slug: string;
  user_id: string;
  user_role: string;
  permissions: string[];
}

export interface TenantHealthResponse {
  status: string;
  timestamp: string;
  tenant: TenantContextPayload;
  services: {
    database: string;
    redis: string;
  };
}

export interface PublicHealthResponse {
  status: string;
  timestamp: string;
  services: {
    database: string;
    redis: string;
  };
}

const API_BASE =
  process.env.NEXT_PUBLIC_API_URL ||
  (typeof window !== "undefined" ? "/api/v1" : "http://127.0.0.1:8000/api/v1");

export async function fetchPublicHealth(): Promise<PublicHealthResponse> {
  const res = await fetch(`${API_BASE}/health`, {
    method: "GET",
    headers: {
      "Accept": "application/json",
    },
  });

  if (!res.ok) {
    throw new Error(`Public healthcheck failed: ${res.status} ${res.statusText}`);
  }

  return res.json();
}

export async function fetchTenantHealth(options: {
  token: string;
  orgId?: string;
  orgSlug?: string;
}): Promise<TenantHealthResponse> {
  const headers: Record<string, string> = {
    "Accept": "application/json",
    "Authorization": `Bearer ${options.token}`,
  };

  if (options.orgId) {
    headers["X-Organization-Id"] = options.orgId;
  }
  if (options.orgSlug) {
    headers["X-Organization-Slug"] = options.orgSlug;
  }

  const res = await fetch(`${API_BASE}/health/tenant`, {
    method: "GET",
    headers,
  });

  if (!res.ok) {
    const errorBody = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(errorBody.detail || `Tenant healthcheck failed with status ${res.status}`);
  }

  return res.json();
}

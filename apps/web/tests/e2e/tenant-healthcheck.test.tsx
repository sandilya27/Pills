import React from "react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import HomePage from "../../app/page";

describe("Ticket 01: Tenant-Authenticated Healthcheck E2E", () => {
  const mockTenantResponse = {
    status: "healthy",
    timestamp: "2026-10-10T14:00:00Z",
    tenant: {
      org_id: "b0000000-0000-0000-0000-000000000001",
      org_slug: "acme-cybernetics",
      user_id: "a0000000-0000-0000-0000-000000000001",
      user_role: "owner",
      permissions: ["read", "write"],
    },
    services: {
      database: "connected",
      redis: "connected",
    },
  };

  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it("renders the monorepo workspace and organization status correctly", () => {
    render(<HomePage />);

    expect(screen.getByText("PILLS")).toBeInTheDocument();
    expect(screen.getByText("Acme Cybernetics")).toBeInTheDocument();
    expect(screen.getByText("acme-cybernetics")).toBeInTheDocument();
    expect(screen.getByText("Alex Vance")).toBeInTheDocument();
    expect(screen.getByText("PostgreSQL 16 + pgvector")).toBeInTheDocument();
    expect(screen.getByText("Redis 7")).toBeInTheDocument();
    expect(screen.getByText("FastAPI API")).toBeInTheDocument();
  });

  it("authenticated user triggers healthcheck ping and receives validated tenant context", async () => {
    const fetchMock = vi.fn().mockImplementation(() =>
      Promise.resolve({
        ok: true,
        status: 200,
        json: () => Promise.resolve(mockTenantResponse),
      })
    );
    vi.stubGlobal("fetch", fetchMock);

    render(<HomePage />);

    const pingButton = screen.getByRole("button", { name: /Trigger Authenticated Ping/i });
    fireEvent.click(pingButton);

    await waitFor(() => {
      expect(fetchMock).toHaveBeenCalled();
    });

    await waitFor(
      () => {
        expect(
          screen.getByText("Tenant Context Successfully Validated by Backend")
        ).toBeInTheDocument();
      },
      { timeout: 3000 }
    );

    // Assert that the validated tenant context is rendered
    expect(screen.getAllByText("b0000000-0000-0000-0000-000000000001").length).toBeGreaterThanOrEqual(2);
    expect(screen.getByText("a0000000-0000-0000-0000-000000000001")).toBeInTheDocument();
    expect(screen.getAllByText(/owner/i).length).toBeGreaterThanOrEqual(2);
    expect(screen.getByText(/PostgreSQL: connected/i)).toBeInTheDocument();
    expect(screen.getByText(/Redis: connected/i)).toBeInTheDocument();
  });

  it("triggers cross-tenant boundary breach simulation and surfaces 403 error", async () => {
    const fetchMock = vi.fn().mockImplementation(() =>
      Promise.resolve({
        ok: false,
        status: 403,
        statusText: "Forbidden",
        json: () =>
          Promise.resolve({
            detail: "Tenant boundary violation: User does not belong to organization 'unauthorized'.",
          }),
      })
    );
    vi.stubGlobal("fetch", fetchMock);

    render(<HomePage />);

    const breachButton = screen.getByRole("button", { name: /Simulate Boundary Breach/i });
    fireEvent.click(breachButton);

    await waitFor(() => {
      expect(
        screen.getByText("Tenant Boundary Enforcement Succeeded")
      ).toBeInTheDocument();
      expect(
        screen.getByText(/Tenant boundary violation: User does not belong to organization/i)
      ).toBeInTheDocument();
    });
  });
});

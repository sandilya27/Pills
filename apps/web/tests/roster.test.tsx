import React from "react";
import { act, cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { RosterBar } from "@/components/roster-bar";
import { PillAvatar } from "@/components/pill-avatar";
import type { Pill, PillStatus } from "@/lib/api-client";

const pill = (name: string, status: PillStatus = "idle"): Pill => ({
  id: name, name, slug: name.toLowerCase(), role: "Teammate", tagline: "Help the team",
  avatar_seed: name, body_color: "#1d4ed8", accent_color: "#22d3ee", body_silhouette: "column", status,
});

afterEach(() => { cleanup(); vi.useRealTimers(); vi.unstubAllGlobals(); });

describe("Pill roster", () => {
  it("loads all seven Pills with authenticated organization headers", async () => {
    const names = ["Dex", "Cipher", "Pulse", "Remedy", "Nootrop", "Aura", "Dose"];
    const fetchMock = vi.fn().mockResolvedValue({ ok: true, json: async () => names.map(name => pill(name)) });
    vi.stubGlobal("fetch", fetchMock);
    render(<RosterBar token="session" orgId="acme" />);
    expect(screen.getByRole("status")).toHaveTextContent("Loading Pills");
    await screen.findByText("7 teammates");
    for (const name of names) expect(screen.getByRole("img", { name: `${name} — Idle` })).toBeInTheDocument();
    expect(fetchMock).toHaveBeenCalledWith(expect.stringContaining("/agents"), expect.objectContaining({
      headers: expect.objectContaining({ Authorization: "Bearer session", "X-Organization-Id": "acme" }),
    }));
  });

  it("refreshes status and clears the roster when the organization changes", async () => {
    vi.useFakeTimers({ toFake: ["setTimeout", "clearTimeout"] });
    const fetchMock = vi.fn().mockResolvedValueOnce({ ok: true, json: async () => [pill("Dex")] })
      .mockResolvedValueOnce({ ok: true, json: async () => [pill("Dex", "thinking")] })
      .mockResolvedValue({ ok: true, json: async () => [] });
    vi.stubGlobal("fetch", fetchMock);
    const { rerender } = render(<RosterBar token="session" orgId="acme" />);
    await act(async () => {});
    expect(screen.getByRole("img", { name: "Dex — Idle" })).toBeInTheDocument();
    await act(async () => { await vi.advanceTimersByTimeAsync(5000); });
    expect(screen.getByRole("img", { name: "Dex — Thinking" })).toBeInTheDocument();
    rerender(<RosterBar token="session" orgId="beta" />);
    expect(screen.queryByText("Dex")).not.toBeInTheDocument();
    await act(async () => {});
    expect(screen.getByText("No Pills in this workspace yet.")).toBeInTheDocument();
  });

  it("shows API errors without substituting a demo roster", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: false, status: 403, json: async () => ({ detail: "Forbidden" }) }));
    render(<RosterBar token="session" orgId="beta" />);
    expect(await screen.findByRole("alert")).toHaveTextContent("Forbidden");
    expect(screen.queryByRole("img")).not.toBeInTheDocument();
  });

  it.each([ ["idle", "Idle"], ["thinking", "Thinking"], ["executing_tool", "Executing tool"], ["awaiting_approval", "Awaiting approval"] ] as const)("labels %s and generates animated dual-tone SVG", (status, label) => {
    const { rerender } = render(<PillAvatar pill={pill("Dex", status)} />);
    const image = screen.getByRole("img", { name: `Dex — ${label}` });
    const svg = decodeURIComponent(image.getAttribute("src")!.split(",")[1]);
    expect(svg).toContain("capsule-tone");
    expect(svg).toContain('fill="url(#capsule-tone)"');
    expect(svg).toContain("dbgaBlink");
    expect(svg).toContain("dbgaLook");
    expect(svg).toContain("prefers-reduced-motion");
    rerender(<PillAvatar pill={pill("Dex", "thinking")} />);
    expect(screen.getByRole("img", { name: "Dex — Thinking" })).toHaveAttribute("src", image.getAttribute("src"));
  });
});

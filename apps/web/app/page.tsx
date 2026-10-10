"use client";

import React, { useState } from "react";
import { 
  ShieldCheck, 
  Database, 
  Activity, 
  Building2, 
  User as UserIcon, 
  CheckCircle2, 
  AlertCircle, 
  RefreshCw,
  Server,
  Layers,
  Sparkles
} from "lucide-react";
import { fetchTenantHealth, type TenantHealthResponse } from "@/lib/api-client";
import { RosterBar } from "@/components/roster-bar";

export default function HomePage() {
  // Demo session state representing an authenticated organization workspace
  const [currentUser, setCurrentUser] = useState({
    id: "a0000000-0000-0000-0000-000000000001",
    name: "Alex Vance",
    email: "alex@acme.corp",
  });

  const [activeOrg, setActiveOrg] = useState({
    id: "b0000000-0000-0000-0000-000000000001",
    name: "Acme Cybernetics",
    slug: "acme-cybernetics",
    role: "owner",
  });

  // Client JWT token matching BetterAuth session secret
  const [token, setToken] = useState(
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhMDAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMDEiLCJvcmdfaWQiOiJiMDAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMDEiLCJvcmdfc2x1ZyI6ImFjbWUtY3liZXJuZXRpY3MiLCJyb2xlIjoib3duZXIiLCJleHAiOjE4OTM0NTYwMDB9.PZWAOu6ouiIWLuYW0oZQe99XEd4d25Zz8DMnykHIlrM"
  );

  const [isLoading, setIsLoading] = useState(false);
  const [healthResult, setHealthResult] = useState<TenantHealthResponse | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [isSimulatedBreach, setIsSimulatedBreach] = useState(false);

  const handlePingHealthcheck = async (simulatedOrgId?: string) => {
    setIsLoading(true);
    setErrorMsg(null);
    setHealthResult(null);
    setIsSimulatedBreach(Boolean(simulatedOrgId));

    try {
      const data = await fetchTenantHealth({
        token,
        orgId: simulatedOrgId || activeOrg.id,
        orgSlug: simulatedOrgId ? undefined : activeOrg.slug,
      });
      setHealthResult(data);
    } catch (err: any) {
      setErrorMsg(err.message || "Failed to communicate with API");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="min-h-screen px-4 py-8 md:px-12 lg:px-24 max-w-7xl mx-auto flex flex-col gap-10">
      {/* Top Brand Navigation */}
      <header className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-800/80 pb-6">
        <div className="flex items-center gap-3">
          <div className="relative flex items-center justify-center w-10 h-16 rounded-[9999px] border border-cyan-400/40 bg-gradient-to-b from-cyan-400/30 to-slate-900 shadow-lg shadow-cyan-500/10">
            <div className="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-pulse shadow-[0_0_10px_#22d3ee]" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-bold tracking-tight text-white">PILLS</h1>
              <span className="text-xs font-mono uppercase px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
                Ticket 01 Verified
              </span>
            </div>
            <p className="text-xs text-slate-400">Enterprise Multi-Agent Platform • Monorepo Foundation</p>
          </div>
        </div>

        {/* System Infrastructure Indicators */}
        <div className="flex items-center gap-3 text-xs font-mono">
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-300">
            <Database className="w-3.5 h-3.5 text-emerald-400" />
            <span>PostgreSQL 16 + pgvector</span>
          </div>
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-300">
            <Activity className="w-3.5 h-3.5 text-rose-400" />
            <span>Redis 7</span>
          </div>
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-300">
            <Server className="w-3.5 h-3.5 text-cyan-400" />
            <span>FastAPI API</span>
          </div>
        </div>
      </header>

      <RosterBar token={token} orgId={activeOrg.id} />

      {/* Hero Overview */}
      <section className="flex flex-col gap-3">
        <h2 className="text-3xl font-extrabold tracking-tight text-white md:text-4xl">
          Tenant-Authenticated <span className="gradient-text">Healthcheck Ping</span>
        </h2>
        <p className="text-sm md:text-base text-slate-400 max-w-3xl leading-relaxed">
          Verification of Ticket 01 architecture: The Next.js 15 client communicates with the FastAPI API backend,
          passing BetterAuth session credentials and organization workspace scoping. The application-level{" "}
          <code className="text-cyan-300 bg-cyan-950/50 px-1.5 py-0.5 rounded border border-cyan-800/40">TenantContext</code>{" "}
          dependency injection strictly validates organization boundaries.
        </p>
      </section>

      {/* Main Grid: Authentication Workspace + Healthcheck Interactive Card */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Column: Organization & Session Context */}
        <div className="lg:col-span-5 flex flex-col gap-6">
          <div className="glass-panel rounded-2xl p-6 flex flex-col gap-5 border border-slate-800">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div className="flex items-center gap-2">
                <Building2 className="w-4 h-4 text-cyan-400" />
                <h3 className="font-semibold text-sm text-slate-200">Organization Workspace</h3>
              </div>
              <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                BetterAuth Multi-Tenancy
              </span>
            </div>

            <div className="space-y-3 text-xs">
              <div>
                <label className="text-slate-400 block mb-1">Organization Name</label>
                <div className="p-2.5 rounded-lg bg-slate-900/90 border border-slate-800 text-slate-200 font-medium">
                  {activeOrg.name}
                </div>
              </div>
              <div>
                <label className="text-slate-400 block mb-1">Organization Slug</label>
                <div className="p-2.5 rounded-lg bg-slate-900/90 border border-slate-800 font-mono text-cyan-400">
                  {activeOrg.slug}
                </div>
              </div>
              <div>
                <label className="text-slate-400 block mb-1">Organization ID (UUID)</label>
                <div id="org-id-display" className="p-2.5 rounded-lg bg-slate-900/90 border border-slate-800 font-mono text-[11px] text-slate-400 break-all">
                  {activeOrg.id}
                </div>
              </div>
            </div>

            <div className="border-t border-slate-800 pt-4 flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-full bg-cyan-950 border border-cyan-800/60 flex items-center justify-center text-cyan-300">
                  <UserIcon className="w-4 h-4" />
                </div>
                <div>
                  <div className="text-xs font-semibold text-white">{currentUser.name}</div>
                  <div className="text-[11px] text-slate-400">{currentUser.email}</div>
                </div>
              </div>
              <span className="text-xs font-mono uppercase px-2 py-0.5 rounded bg-slate-800 text-slate-300">
                {activeOrg.role}
              </span>
            </div>
          </div>

          {/* Architecture Summary Card */}
          <div className="glass-panel rounded-2xl p-6 flex flex-col gap-3 text-xs text-slate-400 border border-slate-800">
            <div className="flex items-center gap-2 text-slate-200 font-semibold">
              <Layers className="w-4 h-4 text-purple-400" />
              <span>Monorepo Topology</span>
            </div>
            <ul className="space-y-2 font-mono text-[11px]">
              <li className="flex items-center justify-between">
                <span>• apps/web</span>
                <span className="text-slate-300">Next.js 15 App Router</span>
              </li>
              <li className="flex items-center justify-between">
                <span>• apps/api</span>
                <span className="text-slate-300">FastAPI + SQLModel</span>
              </li>
              <li className="flex items-center justify-between">
                <span>• packages/forge</span>
                <span className="text-slate-300">Pydantic AI Engine</span>
              </li>
              <li className="flex items-center justify-between">
                <span>• docker/compose</span>
                <span className="text-slate-300">PostgreSQL 16 + Redis 7</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Right Column: Interactive End-to-End Ping & Validated Tenant Scope Display */}
        <div className="lg:col-span-7 flex flex-col gap-6">
          <div className="glass-panel-glow rounded-2xl p-6 flex flex-col gap-6">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div className="flex items-center gap-2">
                <ShieldCheck className="w-5 h-5 text-cyan-400" />
                <h3 className="font-semibold text-base text-white">End-to-End Tenant Ping</h3>
              </div>
              <span className="text-xs text-slate-400 font-mono">GET /api/v1/health/tenant</span>
            </div>

            <div className="flex flex-col sm:flex-row gap-3">
              <button
                id="btn-tenant-ping"
                onClick={() => handlePingHealthcheck()}
                disabled={isLoading}
                className="flex-1 flex items-center justify-center gap-2 px-5 py-3 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-bold text-sm shadow-lg shadow-cyan-500/20 transition-all disabled:opacity-50"
              >
                {isLoading ? (
                  <RefreshCw className="w-4 h-4 animate-spin text-slate-950" />
                ) : (
                  <Sparkles className="w-4 h-4 text-slate-950" />
                )}
                <span>Trigger Authenticated Ping</span>
              </button>

              <button
                id="btn-simulate-violation"
                onClick={() => handlePingHealthcheck("ffffffff-ffff-ffff-ffff-ffffffffffff")}
                disabled={isLoading}
                className="flex items-center justify-center gap-2 px-4 py-3 rounded-xl bg-rose-950/40 hover:bg-rose-900/50 border border-rose-800/40 text-rose-300 font-semibold text-xs transition-all disabled:opacity-50"
                title="Test cross-tenant isolation by passing an unauthorized organization ID"
              >
                <AlertCircle className="w-4 h-4" />
                <span>Simulate Boundary Breach</span>
              </button>
            </div>

            {/* Error Display */}
            {errorMsg && (
              <div
                id="error-banner"
                className="p-4 rounded-xl bg-rose-950/40 border border-rose-800/60 text-rose-300 flex items-start gap-3 text-xs font-mono"
              >
                <AlertCircle className="w-5 h-5 flex-shrink-0 text-rose-400 mt-0.5" />
                <div>
                  <div className="font-bold text-rose-200">
                    {isSimulatedBreach
                      ? "Tenant Boundary Enforcement Succeeded"
                      : "Connection Error / Request Failed"}
                  </div>
                  <div className="mt-1">{errorMsg}</div>
                </div>
              </div>
            )}

            {/* Validated Response Display */}
            {healthResult && (
              <div id="health-result-card" className="flex flex-col gap-4 animate-in fade-in duration-300">
                <div className="flex items-center gap-2 text-emerald-400 text-xs font-semibold">
                  <CheckCircle2 className="w-4 h-4" />
                  <span>Tenant Context Successfully Validated by Backend</span>
                </div>

                <div className="rounded-xl bg-slate-950/90 border border-slate-800/90 p-4 font-mono text-xs flex flex-col gap-3">
                  <div className="text-slate-400 text-[11px] border-b border-slate-800/80 pb-2 flex justify-between">
                    <span>INJECTED TENANT CONTEXT</span>
                    <span className="text-cyan-400">{healthResult.timestamp}</span>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                    <div>
                      <span className="text-slate-500 block">Organization ID</span>
                      <span id="result-org-id" className="text-cyan-300 break-all">{healthResult.tenant.org_id}</span>
                    </div>
                    <div>
                      <span className="text-slate-500 block">Organization Slug</span>
                      <span id="result-org-slug" className="text-emerald-400">{healthResult.tenant.org_slug}</span>
                    </div>
                    <div>
                      <span className="text-slate-500 block">User ID</span>
                      <span id="result-user-id" className="text-purple-300 break-all">{healthResult.tenant.user_id}</span>
                    </div>
                    <div>
                      <span className="text-slate-500 block">User Role</span>
                      <span id="result-user-role" className="text-amber-300 uppercase">{healthResult.tenant.user_role}</span>
                    </div>
                  </div>

                  <div className="border-t border-slate-800/80 pt-2 flex flex-col gap-1.5">
                    <span className="text-slate-500">Service Status Verification:</span>
                    <div className="flex items-center gap-4 text-[11px]">
                      <span className="text-emerald-400 flex items-center gap-1">
                        ● PostgreSQL: {healthResult.services.database}
                      </span>
                      <span className="text-emerald-400 flex items-center gap-1">
                        ● Redis: {healthResult.services.redis}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}

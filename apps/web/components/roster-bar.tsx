"use client";

import React, { useEffect, useState } from "react";
import { fetchAgents, type Pill } from "@/lib/api-client";
import { PillAvatar, PILL_STATUSES } from "./pill-avatar";

export function RosterBar({ token, orgId }: { token: string; orgId: string }) {
  const [roster, setRoster] = useState<{ orgId: string; pills: Pill[] } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [retry, setRetry] = useState(0);
  const pills = roster?.orgId === orgId ? roster.pills : null;

  useEffect(() => {
    const controller = new AbortController();
    let timer: ReturnType<typeof setTimeout>;
    setRoster(null);
    setError(null);
    const load = async () => {
      try {
        const data = await fetchAgents({ token, orgId, signal: controller.signal });
        if (!controller.signal.aborted) {
          setRoster({ orgId, pills: data });
          setError(null);
        }
      } catch (err) {
        if (!controller.signal.aborted) setError(err instanceof Error ? err.message : "Unable to load Pills");
      } finally {
        if (!controller.signal.aborted) timer = setTimeout(load, 5000);
      }
    };
    void load();
    return () => { controller.abort(); clearTimeout(timer); };
  }, [token, orgId, retry]);

  return (
    <section aria-label="Workspace Pills" className="glass-panel rounded-2xl p-5">
      <div className="mb-4 flex items-center justify-between gap-3">
        <h2 className="text-lg font-semibold">Your Pills</h2>
        <span className="text-xs text-slate-400">{pills ? `${pills.length} teammates` : "Workspace roster"}</span>
      </div>
      {error && <div role="alert" className="mb-3 text-sm text-rose-300">{error} <button className="underline" onClick={() => setRetry(value => value + 1)}>Retry roster</button></div>}
      {!pills && !error && <p role="status" className="text-sm text-slate-400">Loading Pills…</p>}
      {pills?.length === 0 && <p className="text-sm text-slate-400">No Pills in this workspace yet.</p>}
      {pills && <ul aria-label="Pill roster" tabIndex={0} className="flex gap-4 overflow-x-auto pb-3 focus-visible:outline focus-visible:outline-cyan-400">
        {pills.map(pill => <li key={pill.id} className="flex min-w-36 flex-1 flex-col items-center rounded-xl border border-slate-800 bg-slate-950/50 px-4 py-3 text-center" title={pill.tagline}>
          <PillAvatar pill={pill} />
          <span className="mt-2 font-semibold">{pill.name}</span>
          <span className="mt-1 text-xs text-slate-400">{pill.role}</span>
          <span className="mt-2 text-xs text-slate-300">{(PILL_STATUSES[pill.status] || PILL_STATUSES.idle).label}</span>
        </li>)}
      </ul>}
    </section>
  );
}

"use client";

import React, { useMemo, type CSSProperties } from "react";
import { Avatar, Style } from "@dicebear/core";
import gaze from "@dicebear/styles/gaze.json";
import type { Pill, PillStatus } from "@/lib/api-client";

export const PILL_STATUSES: Record<PillStatus, { label: string; color: string }> = {
  idle: { label: "Idle", color: "#94a3b8" },
  thinking: { label: "Thinking", color: "#22d3ee" },
  executing_tool: { label: "Executing tool", color: "#a78bfa" },
  awaiting_approval: { label: "Awaiting approval", color: "#fbbf24" },
};

const gazeStyle = new Style(gaze);
const safeColor = (color: string, fallback: string) => /^#[0-9a-f]{6}$/i.test(color) ? color : fallback;

export function PillAvatar({ pill, size = 88 }: {
  pill: Pick<Pill, "name" | "avatar_seed" | "body_color" | "accent_color" | "body_silhouette" | "status">;
  size?: number;
}) {
  const status = PILL_STATUSES[pill.status] || PILL_STATUSES.idle;
  const source = useMemo(() => {
    const body = safeColor(pill.body_color, "#1d4ed8");
    const accent = safeColor(pill.accent_color, "#22d3ee");
    // Keep Gaze's seeded eyes and native wander/blink animations. Give its
    // capsule body a two-tone gradient without injecting SVG into the DOM.
    const svg = new Avatar(gazeStyle, {
      seed: pill.avatar_seed,
      shapeVariant: pill.body_silhouette === "column" ? "column" : "pill",
      animationVariant: "medium",
      bodyColor: [body],
      inkColor: ["#ffffff"],
    }).toString()
      .replaceAll(`fill="${body}"`, 'fill="url(#capsule-tone)"')
      .replace("<defs>", `<defs><linearGradient id="capsule-tone" x1="0" y1="0" x2="0" y2="1"><stop offset="50%" stop-color="${body}"/><stop offset="50%" stop-color="${accent}"/></linearGradient>`);
    return `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`;
  }, [pill.avatar_seed, pill.body_color, pill.accent_color, pill.body_silhouette]);

  return (
    <span className="pill-avatar" data-status={pill.status}
      style={{ width: size, height: size, "--pill-led": status.color } as CSSProperties}>
      <img src={source} width={size} height={size} alt={`${pill.name} — ${status.label}`} />
      <span className="pill-led" aria-hidden="true" />
    </span>
  );
}

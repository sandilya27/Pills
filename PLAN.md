# Pills — The Complete Product, Architectural & Frontend Plan

> **Product:** Pills — Enterprise-Grade Multi-Agent AI Teammate Platform  
> **Status:** Final Execution Plan (Fullstack Edition)  
> **Target Architecture:** Monorepo (Next.js 15 + shadcn/ui + assistant-ui + OpenIntelligentUI + FastAPI + Forge over Pydantic AI)  
> **Design Identity:** Cylindrical Capsule Avatars, DiceBear Gaze Animated Characters, Generative UI Widgets  
> **License Strategy:** Closed-source SaaS built on MIT / Apache-2.0 / CC0 open-source building blocks  

---

## 1. Executive Summary & Vision

**Pills** is a self-hosted & cloud-ready AI Teammate SaaS platform. Instead of generic chat prompts, teams hire, train, and collaborate with specialized AI agents who possess distinct roles, maintain long-term memory, follow standardized operational procedures (Skills), securely interface with external systems (MCP), and execute long-running asynchronous tasks in sandboxes.

### The "Pill" Metaphor & Brand Identity
In medicine, a pill is a concentrated, potent dose that targets a specific ailment. In **Pills**, each AI teammate is a specialized, targeted capsule that cures a specific operational headache:
- **Dex** coordinates and leads the team.
- **Cipher** audits security, pull requests, and dependencies.
- **Pulse** monitors SRE health, logs, and infrastructure.
- **Nootrop** conducts deep research and document synthesis.
- **Remedy** debugs and refactors codebase issues.
- **Aura** crafts product specs, design critiques, and user stories.
- **Dose** automates repetitive operations, syncs, and cron tasks.

Every agent is visually personified as an animated cylindrical pill with wander-and-blink expressive eyes powered by **DiceBear Gaze** inside a bespoke glassmorphic capsule avatar.

---

## 2. The Core Entity Hierarchy

To prevent architectural decay, Pills enforces a strict conceptual separation:

```
┌────────────────────────────────────────────────────────────────────────┐
│                              AGENT (THE PILL)                          │
│             "Who" performs the work (Identity, Persona, Model)         │
│          e.g. Dex (Lead), Cipher (Security), Pulse (SRE)               │
└───────────────────┬────────────────────────────────┬───────────────────┘
                    │ assigns                        │ grants
┌───────────────────▼──────────────┐   ┌─────────────▼───────────────────┐
│              SKILL               │   │          TOOL REGISTRY          │
│ "How" the task is performed      │   │ "What" external capabilities    │
│ (Instruction-only SOP package,   │   │ are available (Built-in, MCP,   │
│  declares prerequisite tools)    │   │  Sandboxed E2B, Agent Zero)     │
└──────────────────────────────────┘   └─────────────┬───────────────────┘
                                                     │ intercepted by
                                       ┌─────────────▼───────────────────┐
                                       │          TOOL GATEWAY           │
                                       │ (Callable decorator wrapper,    │
                                       │  per-agent permission policy,   │
                                       │  approval interrupts & audits)  │
                                       └─────────────┬───────────────────┘
                                                     │ controls
                                       ┌─────────────▼───────────────────┐
                                       │      PER-AGENT PERMISSIONS      │
                                       │ (ALLOW, REQUIRE_APPROVAL, DENY) │
                                       └─────────────────────────────────┘
```

| Entity | Canonical Definition | Example in Pills |
|---|---|---|
| **Pill (Agent)** | Autonomous worker with dedicated identity, model, persona, memory scope, and assigned capabilities. | *Cipher* (Security Auditor), *Pulse* (SRE Sentinel) |
| **Agent Group** | Configured team of Pills led by an Admin Lead Pill who orchestrates and delegates to Member Pills. | *Security Response Team* (Dex as Lead, Cipher & Remedy as Members) |
| **Thread** | Persistent conversational timeline in a workspace containing an ordered sequence of messages and tasks. | Thread `/workspace/threads/uuid` |
| **Message** | Discrete entry in a Thread authored by a user, a Pill, or the system. | User request or Pill final synthesis |
| **Task** | Durable, stateful async execution unit running on SAQ workers, emitting events over Redis Streams. | Background task processing a prompt turn |
| **Task Checkpoint**| Serialized model message history and tool parameters stored in PostgreSQL during approval pauses. | Checkpoint state resuming via synthetic `ToolReturn` |
| **Skill** | Versioned, instruction-only SOP document (`SKILL.md`) that declares required tool prerequisites. | `incident-postmortem`, `audit-security-pr` |
| **Skill Release** | Immutable, semver-pinned snapshot of a Skill deployed to agents. | `audit-security-pr@1.2.0` |
| **Tool Registry** | Central tenant-wide catalog of all registered tools with schemas, risk levels, and sandboxed runtimes. | Approved organizational tools |
| **Tool Gateway** | Callable decorator wrapper enforcing permissions, step caps, approval interrupts, and audit logs. | Security enforcement proxy before any tool runs |
| **Approval Gate** | Suspension point where a Task pauses execution because an invoked tool requires human authorization. | Gated execution awaiting human sign-off |
| **Generative UI** | Catalog-driven React widget emitted via schema-validated `render_widget` tool calls into sandboxed iframes. | `DataTableWidget`, `MetricsChartWidget` |

---

## 3. The 22 OSS Building Blocks (Leverage Map)

We refuse to reinvent commodity infrastructure. Pills uses battle-tested open-source components so development is focused 100% on the core product differentiators:

| Layer | Selected OSS Tool | License | Role in Pills |
|---|---|---|---|
| **Chat UI Primitives** | **assistant-ui** | MIT | Thread management, message streaming, composer, action bars, tool execution blocks. |
| **Generative UI** | **OpenIntelligentUI (CopilotKit)** | MIT | Sandboxed iframe generative UI widgets (charts, 3D scenes, calculators, dynamic tables) via AG-UI protocol. |
| **Component Primitives** | **shadcn/ui + Tailwind CSS** | MIT | Accessible, highly customized enterprise component design system. |
| **Avatar Engine** | **DiceBear Gaze** | CC0 1.0 | Animated SVG avatars with wandering/blinking eyes and hopping pill bodies. |
| **Notifications** | **Novu** | MIT | Multi-channel notifications with drop-in `<Inbox />` for human approvals. |
| **Agent Runtime** | **Pydantic AI** | MIT | Core agent execution loop, structured typing, dependency injection. |
| **LLM Gateway** | **LiteLLM** | MIT | Unified provider proxy (OpenAI, Anthropic, Gemini, local models), fallback, cost tracking. |
| **Frontend Framework** | **Next.js 15 (App Router)** | MIT | Enterprise web dashboard, SSR, streaming layouts. |
| **Authentication** | **BetterAuth** | MIT | Multi-tenant auth, session handling, OAuth, organizations/teams plugin. |
| **Backend API** | **FastAPI** | MIT | High-performance async Python REST & SSE endpoints. |
| **ORM / Data Access** | **SQLModel** | MIT | Unified SQLAlchemy database models and Pydantic schemas. |
| **Database Migrations**| **Alembic** | MIT | Safe, version-controlled PostgreSQL schema migrations. |
| **Primary Database** | **PostgreSQL 16** | PostgreSQL | Relational storage for tenants, agents, tasks, and audit trails. |
| **Vector Engine** | **pgvector** | PostgreSQL | Vector similarity search for skills and memory retrieval inside PostgreSQL. |
| **Cache & Broker** | **Redis 7** | BSD-3 | Session cache, pub/sub for SSE updates, task queue backend. |
| **Background Queue** | **SAQ (Simple Async Queue)** | MIT | Async-native worker pool, task scheduling, retries, and job dispatching. |
| **Agent Memory** | **Mem0** | Apache-2.0 | Contextual memory extraction, deduplication, user/agent/session scoping. |
| **Sandbox Execution** | **E2B** | Apache-2.0 | Isolated cloud/self-hosted microVM sandboxes for code execution & file handling. |
| **Computer Use** | **Agent Zero** | MIT | Containerized computer-use capability (terminal, browser, desktop) for Phase 7. |
| **MCP Integration** | **Pydantic AI MCPToolset** | MIT | Native Model Context Protocol client for connecting external servers. |
| **Observability** | **Langfuse** | MIT | Self-hosted traces, token counting, latency metrics, and execution graphs. |
| **LLM Testing / Evals**| **Promptfoo** | MIT | CI/CD eval suite, regression tests, skill accuracy benchmarks, prompt red-teaming. |
| **Deployment** | **Docker Compose / Coolify** | Apache-2.0 | Reproducible local development and self-hosted production orchestration. |

---

## 4. Frontend Architecture & Generative UI Deep Dive

The frontend for Pills is not a simple generic chat clone. It is a high-polish, interactive command center built on three tightly integrated pillars:

```
┌────────────────────────────────────────────────────────────────────────┐
│                         PILLS FRONTEND WORKSPACE                       │
│                                                                        │
│  ┌────────────────────────┐  ┌──────────────────────────────────────┐  │
│  │   shadcn/ui Primitives │  │       assistant-ui Chat System       │  │
│  │ (Modals, Tabs, Drawers,│  │ (<Thread />, <Composer />, Streaming,│  │
│  │  DataTables, Tooltips) │  │  Branching, Action Bars, Tool Cards) │  │
│  └───────────┬────────────┘  └──────────────────┬───────────────────┘  │
│              │                                  │                      │
│              └─────────────────┬────────────────┘                      │
│                                │                                       │
│                                ▼                                       │
│          ┌───────────────────────────────────────────┐                 │
│          │    OpenIntelligentUI (CopilotKit Engine)  │                 │
│          │   - Dynamic Generative UI in Sandboxed    │                 │
│          │     iframes (Charts, 3D, Custom Forms)    │                 │
│          │   - AG-UI (Agent-User Interaction) Proto  │                 │
│          │   - Live Reactive Component Streaming     │                 │
│          └─────────────────────┬─────────────────────┘                 │
│                                │                                       │
│                                ▼                                       │
│          ┌───────────────────────────────────────────┐                 │
│          │     Pills Capsule Persona & Avatar System │                 │
│          │   - Cylindrical Capsule profile containers│                 │
│          │   - DiceBear Gaze animated hopping SVGs   │                 │
│          │   - Live LED status halos (Thinking/Idle) │                 │
│          └───────────────────────────────────────────┘                 │
└────────────────────────────────────────────────────────────────────────┘
```

### 4.1 Chat System with `assistant-ui`
`assistant-ui` provides high-performance, modular React primitives tailored for AI workflows:
- **Thread Management:** Multi-conversation switching, branch editing, regenerative prompts.
- **Message Streaming:** Word-by-word streaming with smooth auto-scroll lock.
- **Rich Code Blocks:** Syntax highlighting, line numbers, one-click copy, and run-in-sandbox triggers.
- **Human-In-The-Loop Cards:** Inline widgets embedded into the message stream when an agent pauses at an approval gate, presenting tool payload diffs and one-click `[Approve]` / `[Reject]` actions.

### 4.2 Generative UI with `OpenIntelligentUI`
While standard chats output static markdown, Pills leverages **OpenIntelligentUI** (built on the AG-UI protocol) to let agents render rich, interactive client-side interfaces on the fly:
1. **Interactive Data Tables:** Agents analyzing CSVs or SQL results render sortable, filterable tables with instant export.
2. **Dynamic Charts & Graphs:** Live charts (Recharts / Chart.js) generated dynamically with reactive parameters.
3. **Interactive Simulation & Calculators:** Financial comparisons, quote calculators, or algorithmic step-by-step visualizers.
4. **Sandboxed Security:** Every dynamic interface is isolated in a sandboxed iframe to guarantee that AI-generated scripts cannot access authentication tokens or compromise the parent application DOM.

#### Code Architecture: Generative UI Message Component
```tsx
// apps/web/components/chat/generative-ui-message.tsx
"use client";

import React from "react";
import { OpenIntelligentUIRenderer } from "@copilotkit/open-intelligent-ui";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Sparkles } from "lucide-react";

interface GenerativeUIProps {
  componentType: string;
  propsPayload: Record<string, any>;
  title?: string;
}

export function GenerativeUIMessage({ componentType, propsPayload, title }: GenerativeUIProps) {
  return (
    <Card className="my-3 border-cyan-500/30 bg-slate-950/80 shadow-lg shadow-cyan-950/20 backdrop-blur-md">
      {title && (
        <CardHeader className="flex flex-row items-center gap-2 border-b border-border/40 py-2.5 px-4">
          <Sparkles className="h-4 w-4 text-cyan-400 animate-pulse" />
          <CardTitle className="text-xs font-semibold tracking-wide uppercase text-slate-300">
            {title}
          </CardTitle>
        </CardHeader>
      )}
      <CardContent className="p-4">
        {/* Isolated sandbox iframe via OpenIntelligentUI */}
        <OpenIntelligentUIRenderer
          component={componentType}
          props={propsPayload}
          sandboxConfig={{
            allowScripts: true,
            allowPopups: false,
            strictOrigin: true,
          }}
        />
      </CardContent>
    </Card>
  );
}
```

---

## 5. Visual Identity: Cylindrical Capsule Avatars & DiceBear Gaze

### 5.1 The DiceBear Gaze Persona Engine
Avatars are generated deterministically using the official **DiceBear Gaze** library (`@dicebear/collection` or the high-speed SVG endpoint).
- **Style:** Clean colored geometric body silhouettes featuring wandering, blinking eyes and an animated hopping body.
- **Pill Shape Silhouette:** Gaze includes specific body silhouettes, notably the cylindrical pill/capsule shape (`pill`, `column`).
- **Endpoint URL:**
  ```
  https://api.dicebear.com/10.x/gaze/svg?seed={seed}&eyes={eye_type}&eyeSpacing={spacing}&body={body_shape}&backgroundColor={hex}&animated=true
  ```

### 5.2 The Cylindrical Capsule Container
Rather than generic circular profile icons, Pills agents are encased in distinct vertical cylindrical capsule containers:
- **Aspect Ratio & Geometry:** High border-radius capsule (`rounded-[9999px]`, aspect ratio ~ `3:5` or tall pill `48px × 72px`).
- **Dual-Tone Split:** Upper capsule dome in the agent's signature neon tone, lower half in glassmorphic dark slate with translucent frost.
- **Interactive Status Halo:** Pulsing LED indicator ring around the capsule:
  - 🟢 **Online / Idle:** Subtle green breathing ring.
  - 🔵 **Thinking / Reasoning:** Revolving cyan halo with rapid eye movement.
  - 🟣 **Executing Tool / Sandbox:** Shimmering violet pulse as the body hops.
  - 🟠 **Awaiting Approval:** Amber alert pulse with attention-seeking gaze.
  - 🔴 **Failed / Blocked:** Red glow with static eyes.

#### Code Architecture: `<PillAvatar />` Component
```tsx
// apps/web/components/agents/pill-avatar.tsx
"use client";

import React from "react";
import Image from "next/image";
import { cn } from "@/lib/utils";

export type AgentStatus = "idle" | "thinking" | "executing" | "waiting_approval" | "error";

interface PillAvatarProps {
  seed: string;
  name: string;
  accentColor: string; // e.g. '#00F0FF'
  status?: AgentStatus;
  size?: "sm" | "md" | "lg" | "xl";
  className?: string;
}

const sizeConfig = {
  sm: { width: "w-8", height: "h-12", icon: 28 },
  md: { width: "w-12", height: "h-18", icon: 42 },
  lg: { width: "w-16", height: "h-24", icon: 56 },
  xl: { width: "w-24", height: "h-36", icon: 84 },
};

const statusGlows: Record<AgentStatus, string> = {
  idle: "ring-emerald-500/40 shadow-emerald-500/20",
  thinking: "ring-cyan-400/80 shadow-cyan-400/50 animate-pulse",
  executing: "ring-purple-500/80 shadow-purple-500/50 animate-bounce",
  waiting_approval: "ring-amber-500/90 shadow-amber-500/60 animate-pulse",
  error: "ring-rose-500/90 shadow-rose-500/60",
};

export function PillAvatar({
  seed,
  name,
  accentColor,
  status = "idle",
  size = "md",
  className,
}: PillAvatarProps) {
  const { width, height, icon } = sizeConfig[size];
  const avatarUrl = `https://api.dicebear.com/10.x/gaze/svg?seed=${encodeURIComponent(
    seed
  )}&animated=true&radius=50`;

  return (
    <div
      className={cn(
        "relative flex flex-col items-center justify-center rounded-[9999px] border border-white/20 p-1 shadow-lg backdrop-blur-md transition-all duration-300",
        width,
        height,
        "ring-2 ring-offset-2 ring-offset-slate-950",
        statusGlows[status],
        className
      )}
      style={{
        background: `linear-gradient(180deg, ${accentColor}33 0%, rgba(15, 23, 42, 0.9) 100%)`,
      }}
      title={`${name} (${status})`}
    >
      {/* Top Cap Gloss Highlight */}
      <div className="absolute top-1 left-1/2 h-2 w-3/5 -translate-x-1/2 rounded-full bg-white/30 blur-[1px]" />

      {/* Animated DiceBear Gaze SVG Character */}
      <div className="relative z-10 flex items-center justify-center overflow-hidden rounded-full">
        <Image
          src={avatarUrl}
          alt={name}
          width={icon}
          height={icon}
          unoptimized
          className="pointer-events-none select-none"
        />
      </div>

      {/* Bottom Status LED Indicator */}
      <div
        className={cn(
          "absolute bottom-1.5 h-1.5 w-1.5 rounded-full",
          status === "idle" && "bg-emerald-400",
          status === "thinking" && "bg-cyan-400 shadow-[0_0_8px_#22d3ee]",
          status === "executing" && "bg-purple-400 shadow-[0_0_8px_#c084fc]",
          status === "waiting_approval" && "bg-amber-400 shadow-[0_0_8px_#fbbf24]",
          status === "error" && "bg-rose-400 shadow-[0_0_8px_#f43f5e]"
        )}
      />
    </div>
  );
}
```

---

## 6. The Flagship Agent Roster (Default Pills)

Pills ships with an out-of-the-box squad of pre-configured AI teammates. Each has a dedicated specialty, personality prompt, signature color, DiceBear seed, and permitted toolset:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        THE PILLS FOUNDING SQUAD                        │
├─────────────┬──────────────┬──────────────┬─────────────┬──────────────┤
│    DEX      │    CIPHER    │    PULSE     │   NOOTROP   │    REMEDY    │
│  The Lead   │  The Auditor │   The SRE    │ The Scholar │  The Fixer   │
│  [Cyan Pill]│ [Crimson Pill] [Green Pill] │[Purple Pill]│[Orange Pill] │
└─────────────┴──────────────┴──────────────┴─────────────┴──────────────┘
```

### Detailed Agent Profiles

#### 1. 🌐 Dex — The Orchestrator & Team Lead
- **Role:** High-agency coordinator. Breaks down complex goals into sub-tasks, assigns work to other teammates, synthesizes final deliverables.
- **Personality:** Decisive, structured, articulate, delegating.
- **Visuals:** Neon Cyan (`#00F0FF`), Gaze Seed: `DexLead`, Silhouette: `pill`
- **Default LLM:** Claude 3.7 Sonnet / GPT-4o
- **Assigned Skills:** `project-breakdown`, `task-delegation`, `executive-summary`
- **Tool Grants:** Agent-to-Agent Delegation, Notion/Slack read/write, Task Scheduler.

#### 2. 🛡️ Cipher — The Security & Code Auditor
- **Role:** Zero-trust sentinel. Inspects git pull requests, audits dependencies, hunts secret leakage, validates zero-day vulnerabilities.
- **Personality:** Skeptical, rigorous, uncompromising, paranoid.
- **Visuals:** Crimson Ruby (`#FF2E63`), Gaze Seed: `CipherSec`, Silhouette: `column`
- **Default LLM:** Claude 3.7 Sonnet (Thinking Mode enabled)
- **Assigned Skills:** `audit-security-pr`, `scan-secrets`, `dependency-cve-triage`
- **Tool Grants:** GitHub PR read/comment, Snyk/Trivy CLI via E2B sandbox.

#### 3. ⚡ Pulse — The SRE & Infrastructure Sentinel
- **Role:** First responder for outages, latency spikes, and error floods. Correlates logs with recent releases.
- **Personality:** Urgent, metric-driven, calm under pressure, concise.
- **Visuals:** Emerald Neon (`#00FF88`), Gaze Seed: `PulseSRE`, Silhouette: `arch`
- **Default LLM:** GPT-4o
- **Assigned Skills:** `incident-triage`, `blameless-postmortem`, `sentry-error-grouping`
- **Tool Grants:** Sentry query, Prometheus metrics, AWS/GCP log fetcher.

#### 4. 🧠 Nootrop — The Deep Researcher & Intelligence Analyst
- **Role:** High-context synthesis. Digests technical whitepapers, competitor releases, 500-page regulatory PDFs, and financial filings.
- **Personality:** Academic, comprehensive, heavily citing sources, analytical.
- **Visuals:** Deep Violet (`#A855F7`), Gaze Seed: `NootropMind`, Silhouette: `egg`
- **Default LLM:** Gemini 1.5 Pro (2M token context window)
- **Assigned Skills:** `deep-literature-review`, `competitor-matrix`, `sec-10k-analysis`
- **Tool Grants:** Web search, arXiv query, PDF extraction, vector memory search.

#### 5. 🔧 Remedy — The Bug Fixer & Refactor Specialist
- **Role:** Surgical coder. Reproduces reported bugs inside an isolated E2B sandbox, writes reproduction unit tests, authoring minimal clean patches.
- **Personality:** Hands-on, pragmatic, test-first, clean-code advocate.
- **Visuals:** Sunset Amber (`#FF9F1C`), Gaze Seed: `RemedyFix`, Silhouette: `pill`
- **Default LLM:** Claude 3.5 Sonnet
- **Assigned Skills:** `reproduce-bug-sandbox`, `write-unit-tests`, `refactor-clean-code`
- **Tool Grants:** E2B Sandbox execution, GitHub create-branch & push-commit.

#### 6. 🎨 Aura — The Product & UX Strategist
- **Role:** Bridges technical teams with user needs. Crafts user stories, acceptance criteria, critiques frontend layouts, and reviews marketing copy.
- **Personality:** Empathetic, creative, vision-oriented, clear.
- **Visuals:** Warm Rose Gold (`#FB7185`), Gaze Seed: `AuraProduct`, Silhouette: `pill`
- **Default LLM:** GPT-4o
- **Assigned Skills:** `write-prd`, `user-flow-critique`, `release-notes-generation`
- **Tool Grants:** Figma metadata read, Jira/Linear create-issue, generative UI widgets.

#### 7. ⏱️ Dose — The Ops & Routine Automator
- **Role:** Steady background executor. Syncs CRM contacts, monitors webhook queues, generates scheduled daily summaries, cleans stale records.
- **Personality:** Methodical, silent, reliable, punctual.
- **Visuals:** Slate Electric Blue (`#3B82F6`), Gaze Seed: `DoseOps`, Silhouette: `column`
- **Default LLM:** Claude 3.5 Haiku / GPT-4o-mini
- **Assigned Skills:** `crm-data-sync`, `daily-ops-digest`, `stale-record-cleanup`
- **Tool Grants:** HubSpot/Salesforce API, SQL query runner, Email digest dispatcher.

---

## 7. Frontend User Experience & Screens

### 7.1 The Team Workspace (`/workspace`)
- **Teammate Capsule Bar:** Horizontal scrollable rail at the top showcasing all organization agents in their animated `<PillAvatar />` capsules with real-time status halos. Clicking a capsule filters threads or initiates a direct pairing session.
- **Multi-Agent Group Thread (`/workspace/group`):** A shared room where users can tag `@Dex` and `@Cipher`. Dex breaks down the problem and delegates subtasks in real time while assistant-ui renders handoff cards.

### 7.2 The Agent Builder (`/agents/new` or `/agents/[id]`)
- **Interactive Capsule Customizer:** Live preview on the left showing the custom pill capsule with real-time color sliders, DiceBear Gaze seed generator, and eye animation toggle.
- **Capability Matrix:** Checkbox grid with categorised tools (Built-In, MCP connections). Each tool has three explicit radio states: `Allow`, `Require Human Approval`, or `Deny`.
- **Skill Attachments:** Drag-and-drop skills from the organization library to the agent.

### 7.3 Skill Studio (`/skills`)
- **Split-Pane Editor:** Left pane contains the `SKILL.md` editor with YAML frontmatter autocomplete and markdown formatting. Right pane runs live validation against the schema.
- **Integrated Test Runner:** One-click simulation using **Promptfoo** to benchmark the skill against synthetic user prompts before publishing version `v1.1.0`.

### 7.4 MCP Studio (`/mcp`)
- **Connection Wizard:** Add an external MCP server via Server-Sent Events (SSE) URL or Docker STDIO command.
- **Auto-Discovery Catalog:** Automatically queries the server's tools via Pydantic AI's `MCPToolset`, parses parameters, and lets admins set organization-wide default risk levels (`READ`, `WRITE`, `DESTRUCTIVE`).

### 7.5 Task Runs & Human Approval Center (`/tasks` & `<Inbox />`)
- **Novu Notification Bell:** Drop-in `<Inbox />` widget in the top header. When an agent like *Remedy* wants to execute a `github.push_commit` marked as `REQUIRE_APPROVAL`, an instant in-app notification fires.
- **Live Run Inspector:** Clicking the notification opens the task stream: real-time execution steps via SSE, terminal output logs from the E2B sandbox, and a prominent `[Authorize Action]` / `[Reject]` modal.

---

## 8. Relational Database Schema (SQLModel / PostgreSQL)

### 8.1 Agents & Agent Groups
```sql
CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,              -- e.g. 'Dex', 'Cipher'
    slug VARCHAR(100) NOT NULL,
    tagline VARCHAR(255),                    -- e.g. 'The Master Orchestrator'
    description TEXT,
    system_prompt TEXT NOT NULL,
    model_provider VARCHAR(50) DEFAULT 'anthropic',
    model_name VARCHAR(100) DEFAULT 'claude-3-7-sonnet',
    temperature FLOAT DEFAULT 0.2,
    max_tokens INT DEFAULT 4096,
    
    -- Visual & Capsule Identity Tokens
    avatar_seed VARCHAR(100) NOT NULL,       -- DiceBear Gaze seed
    accent_color VARCHAR(30) DEFAULT '#00F0FF',
    body_silhouette VARCHAR(30) DEFAULT 'pill', -- 'pill', 'column', 'arch', 'egg'
    eye_type VARCHAR(30) DEFAULT 'default',
    enable_animation BOOLEAN DEFAULT TRUE,
    
    is_active BOOLEAN DEFAULT TRUE,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(org_id, slug)
);

CREATE TABLE agent_groups (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    lead_agent_id UUID NOT NULL REFERENCES agents(id),
    member_agent_ids JSONB NOT NULL DEFAULT '[]', -- UUID array of member pills
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 8.2 Conversational Layer: Threads & Messages
```sql
CREATE TABLE threads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id),
    title VARCHAR(255) NOT NULL DEFAULT 'New Conversation',
    agent_id UUID REFERENCES agents(id),           -- Direct 1:1 pill thread
    agent_group_id UUID REFERENCES agent_groups(id),-- Or collaborative group thread
    sandbox_id VARCHAR(100),                       -- Thread-scoped active E2B sandbox ID
    sandbox_expires_at TIMESTAMPTZ,                -- Idle TTL timestamp (15m)
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    thread_id UUID NOT NULL REFERENCES threads(id) ON DELETE CASCADE,
    org_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    role VARCHAR(30) NOT NULL,                     -- 'user', 'assistant', 'system'
    content TEXT NOT NULL,
    agent_id UUID REFERENCES agents(id),           -- Authoring pill (if assistant)
    task_id UUID,                                  -- Originating completed task ID
    metadata JSONB DEFAULT '{}',                   -- Citations, widget references
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 8.3 Tool Registry & Per-Agent Permissions
```sql
CREATE TABLE tool_registry (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(150) NOT NULL,                    -- e.g. 'github.create_issue', 'render_widget'
    display_name VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    source_type VARCHAR(50) NOT NULL,              -- 'BUILT_IN', 'MCP', 'SANDBOX'
    source_connection_id UUID,                     -- NULL if BUILT_IN, else mcp_connections(id)
    input_schema JSONB NOT NULL,                   -- JSONSchema for parameters
    output_schema JSONB,
    risk_level VARCHAR(30) DEFAULT 'LOW',          -- 'READ', 'WRITE', 'DESTRUCTIVE', 'FINANCIAL'
    default_requires_approval BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(org_id, name)
);

CREATE TABLE agent_tool_permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    tool_id UUID REFERENCES tool_registry(id) ON DELETE CASCADE,
    permission VARCHAR(30) NOT NULL,               -- 'ALLOW', 'DENY', 'REQUIRE_APPROVAL'
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(agent_id, tool_id)
);
```

### 8.4 Execution Layer: Tasks, Checkpoints & Approvals
```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    thread_id UUID REFERENCES threads(id) ON DELETE CASCADE,
    trigger_message_id UUID REFERENCES messages(id),
    agent_id UUID REFERENCES agents(id),
    user_id UUID REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    input_prompt TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'PENDING',          -- 'PENDING', 'RUNNING', 'WAITING_APPROVAL', 'COMPLETED', 'FAILED', 'CANCELLED'
    checkpoint_state JSONB,                        -- Serialized Pydantic AI message history
    step_count INT DEFAULT 0,
    max_steps INT DEFAULT 25,                      -- Deterministic step cap safeguard
    result_summary TEXT,
    error_message TEXT,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE task_events (
    id BIGSERIAL PRIMARY KEY,
    task_id UUID REFERENCES tasks(id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL,               -- 'STEP', 'TOOL_CALL', 'TOOL_RESULT', 'GENERATIVE_UI', 'APPROVAL_REQUESTED', 'ERROR'
    payload JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE approvals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    task_id UUID REFERENCES tasks(id) ON DELETE CASCADE,
    agent_id UUID REFERENCES agents(id),
    tool_name VARCHAR(150) NOT NULL,
    tool_arguments JSONB NOT NULL,
    status VARCHAR(30) DEFAULT 'PENDING',          -- 'PENDING', 'APPROVED', 'REJECTED', 'TIMEOUT'
    requested_at TIMESTAMPTZ DEFAULT NOW(),
    resolved_at TIMESTAMPTZ,
    resolved_by UUID REFERENCES users(id),
    rejection_reason TEXT
);
```

### 8.5 Memory & Skills Layer
```sql
CREATE TABLE agent_memories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    scope VARCHAR(30) NOT NULL,                    -- 'USER', 'AGENT_PRIVATE', 'ORGANIZATION'
    user_id UUID REFERENCES users(id),             -- Populated if USER scope
    agent_id UUID REFERENCES agents(id),           -- Populated if AGENT_PRIVATE scope
    content TEXT NOT NULL,
    embedding vector(1536),                        -- pgvector similarity embedding
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE skills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    slug VARCHAR(100) NOT NULL,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(org_id, slug)
);

CREATE TABLE skill_releases (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    skill_id UUID NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
    version VARCHAR(30) NOT NULL,                  -- Semver: '1.0.0', '1.1.0'
    skill_markdown TEXT NOT NULL,                  -- Full SKILL.md content
    required_tool_names JSONB NOT NULL DEFAULT '[]',-- Declared tool prerequisites
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(skill_id, version)
);

CREATE TABLE agent_skills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    skill_release_id UUID REFERENCES skill_releases(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(agent_id, skill_release_id)
);
```

---

## 9. Monorepo Project Structure

```
pills/
├── apps/
│   ├── web/                              # Next.js 15 Web Application
│   │   ├── app/
│   │   │   ├── (auth)/                   # Login, Signup via BetterAuth
│   │   │   ├── (dashboard)/
│   │   │   │   ├── workspace/            # Main multi-agent chat workspace
│   │   │   │   ├── agents/               # Agent roster & Capsule Builder
│   │   │   │   ├── skills/               # Skill Studio & Promptfoo evals
│   │   │   │   ├── mcp/                  # MCP Connections & Tool Registry
│   │   │   │   ├── tasks/                # Async Task Runs & Approvals
│   │   │   │   └── settings/             # Tenant settings & API keys
│   │   ├── components/
│   │   │   ├── agents/
│   │   │   │   ├── pill-avatar.tsx       # Cylindrical Capsule avatar with DiceBear Gaze
│   │   │   │   ├── agent-capsule-card.tsx# Card showcase with live LED halos
│   │   │   │   └── roster-bar.tsx        # Horizontal scrolling agent rail
│   │   │   ├── chat/
│   │   │   │   ├── assistant-thread.tsx  # assistant-ui chat implementation
│   │   │   │   ├── generative-ui.tsx     # OpenIntelligentUI sandboxed renderer
│   │   │   │   ├── approval-card.tsx     # Inline human-in-the-loop action card
│   │   │   │   └── tool-call-pill.tsx    # Styled tool execution widget
│   │   │   └── ui/                       # shadcn/ui components
│   │   └── lib/
│   │       ├── auth-client.ts            # BetterAuth frontend client
│   │       └── api-client.ts             # Typed OpenAPI / FastAPI fetcher
│   └── api/                              # FastAPI Backend
│       ├── routers/
│       │   ├── agents.py
│       │   ├── tools.py
│       │   ├── mcp.py
│       │   ├── skills.py
│       │   ├── tasks.py
│       │   └── approvals.py
│       └── main.py
├── packages/
│   ├── forge/                            # Agent execution engine over Pydantic AI
│   │   ├── core/agent.py
│   │   ├── gateway/pipeline.py           # Tool Gateway permission & approval checks
│   │   ├── generative_ui/ag_ui.py        # AG-UI protocol handlers for OpenIntelligentUI
│   │   └── skills/loader.py
│   ├── database/                         # SQLModel definitions & Alembic
│   └── workers/                          # SAQ background consumer
├── docker/
│   └── docker-compose.yml
└── package.json
```

---

## 10. Phased Execution Roadmap

```
PHASE 1 (Weeks 1-2): Foundation, Capsule Persona & Unified Durable Task Engine
  ├── Monorepo setup (Next.js 15, FastAPI, SQLModel, PostgreSQL 16 + pgvector, Redis 7)
  ├── BetterAuth multi-tenancy & application-level tenant context dependency
  ├── Relational schema: `threads`, `messages`, `tasks`, `task_events`, `agents`
  ├── Capsule UI System: `<PillAvatar />` with DiceBear Gaze animated SVGs
  ├── Default Founding Squad seeded (Dex, Cipher, Pulse, Remedy, Nootrop)
  ├── SAQ worker service + Redis Streams with `Last-Event-ID` SSE event replay
  └── Forge Core MVP over Pydantic AI executing durable tasks from Day 1

PHASE 2 (Weeks 3-4): assistant-ui Chat, Tool Gateway & Sandboxed MCP
  ├── assistant-ui integration for thread streaming, branching, and code blocks
  ├── Central `tool_registry` & `agent_tool_permissions` tables
  ├── Tool Gateway callable decorator wrapper (permission checks, step cap limit)
  ├── MCP Connection Manager (SSE & isolated container sandboxes for STDIO)
  └── Agent Builder UI with live capsule preview & permission checkboxes

PHASE 3 (Weeks 5-6): Catalog-Driven Generative UI & Stateless Approval Gates
  ├── Typed catalog of Generative UI React widgets (DataTable, MetricsChart, DiffViewer)
  ├── First-class schema-validated `render_widget` tool in Forge
  ├── Stateless Checkpoint Resumption (`ApprovalRequiredInterrupt` + synthetic `ToolReturn`)
  ├── Inline approval cards in assistant-ui + Novu multi-channel `<Inbox />`
  └── Task Runs dashboard in Next.js with step-by-step audit inspection

PHASE 4 (Weeks 7-8): Skill Studio, Agent Groups & Production Evals
  ├── Instruction-only `SKILL.md` parser with immutable semver `skill_releases`
  ├── Skill Studio UI (split-pane editor, schema validation, release promotion)
  ├── Agent Groups (Lead Pill orchestration + collapsible Subtask Delegation Cards)
  ├── Thread-scoped E2B sandboxes with 15-minute inactivity TTL
  └── Automated Promptfoo skill evals & Langfuse telemetry dashboard

PHASE 5 (Weeks 9-10): Persistent Memory & Context Engine
  ├── Mem0 integration with PostgreSQL + pgvector
  ├── Asynchronous multi-tier memory extraction: User, Agent Private, and Org scopes
  ├── Multi-signal retrieval pipeline in Forge Context Builder
  └── Memory inspection & privacy retention UI

PHASE 6 (Weeks 11-12): Dynamic Agent Recruitment & Hardening
  ├── Phase 2 Agent Groups: dynamic teammate recruitment tool for Lead Pills
  ├── Advanced multi-agent group collaboration & consensus protocols
  ├── Organization usage metering, token quotas, and Stripe billing
  └── Coolify / Kubernetes multi-container deployment orchestration

PHASE 7 (Post-MVP): Computer Use with Agent Zero
  ├── Docker-isolated Agent Zero daemon deployment
  ├── Computer-use tool capability (terminal, browser, desktop interaction)
  └── Streamed visual session playback in the web UI
```

---

## 11. Detailed 4-Week Sprint Plan (MVP Vertical Slice)

### Sprint 1 (Week 1): Foundation, Capsule Persona & Unified Durable Task Engine
- [ ] Initialize monorepo with `uv` workspaces and Turborepo.
- [ ] Set up Docker Compose for local PostgreSQL 16 (with pgvector) and Redis 7.
- [ ] Implement BetterAuth with organization support and FastAPI application-level tenant dependency.
- [ ] Create base database models: `organizations`, `users`, `agents`, `threads`, `messages`, `tasks`, `task_events`.
- [ ] Build `<PillAvatar />` component with DiceBear Gaze SVG integration and dual-tone capsule styling.
- [ ] Seed the 7 founding agents (Dex, Cipher, Pulse, Nootrop, Remedy, Aura, Dose).
- [ ] Configure SAQ worker pool and Redis Streams event emitter with `Last-Event-ID` SSE replay endpoint.
- [ ] Implement Forge Core MVP over Pydantic AI executing prompts as asynchronous durable tasks.
- **Milestone:** User logs in, sees the 7 founding agents in their animated cylindrical pill avatars, starts a Thread with *Dex*, and the conversation executes via the production SAQ worker stream over SSE.

### Sprint 2 (Week 2): assistant-ui Chat, Tool Gateway & Sandboxed MCP
- [ ] Integrate `assistant-ui` with custom streaming adapter hooked into the SSE task event stream.
- [ ] Implement `tool_registry` and `agent_tool_permissions` schemas with tenant scoping.
- [ ] Build the `ToolGateway` callable decorator wrapper enforcing permissions, audit logs, and 25-step cap.
- [ ] Connect external MCP servers via SSE and container-sandboxed STDIO (e.g. GitHub MCP).
- [ ] Build Agent Builder UI: customize instructions, model parameters, and toggle per-tool permission checkboxes.
- **Milestone:** User assigns GitHub tools to *Cipher*; *Dex* is denied permission if he attempts calling them; all tool calls are verified and logged in `task_events`.

### Sprint 3 (Week 3): Catalog-Driven Generative UI & Stateless Approval Gates
- [ ] Implement typed Generative UI React widgets (`DataTableWidget`, `MetricsChartWidget`, `DiffViewerWidget`).
- [ ] Register `render_widget` built-in tool in Forge with strict JSON Schema prop validation.
- [ ] Build Stateless Checkpoint Resumption: Tool Gateway raises `ApprovalRequiredInterrupt`, persists Pydantic AI message history to `tasks.checkpoint_state`, and suspends the worker.
- [ ] Implement Approval API endpoint `/api/v1/approvals/{id}` that schedules a resumption task passing synthetic `ToolReturn` to Pydantic AI.
- [ ] Render inline approval cards in `assistant-ui` and trigger Novu `<Inbox />` notifications.
- **Milestone:** *Remedy* generates a reproduction test, pauses at the approval gate to request write authorization, the worker cleanly suspends, the user approves inline, execution resumes, and *Remedy* renders an interactive `DataTableWidget`.

### Sprint 4 (Week 4): Skill Studio, Agent Groups & Production Evals
- [ ] Implement instruction-only `SKILL.md` parser, `skills` and `skill_releases` tables.
- [ ] Implement Forge Skill Loader: inject active immutable skill release instructions into agent context with tool prerequisite validation.
- [ ] Build Skill Studio UI: split-pane editor, syntax checks, and version promotion.
- [ ] Implement Agent Groups (Phase 1): designate Lead Pill (Dex) and static Member Pills (Cipher, Remedy) with collapsible Subtask Delegation Cards.
- [ ] Provision thread-scoped E2B microVM sandboxes with 15-minute idle TTL.
- [ ] Connect Promptfoo for skill regression evals and Langfuse for execution tracing.
- **Milestone:** A complete, production-ready MVP: Create Agent Group → Lead delegates to Member with pinned Skill Release → Sandboxed tool execution → Human approval checkpoint → Generative UI report → Traced in Langfuse.

---

## 12. Definition of Done & Success Criteria

The Pills MVP is production-viable when all following conditions are verified:

1. **Unique Brand Identity:** Every agent is rendered in a distinct cylindrical capsule with an animated DiceBear Gaze SVG and responsive status LED halo.
2. **Generative UI Capabilities:** Agents can return dynamic, interactive UI widgets (tables, charts, forms) securely isolated via OpenIntelligentUI.
3. **Deterministic Permissions:** An agent can never invoke a tool that is not explicitly marked `ALLOW` in `agent_tool_permissions`.
4. **Fail-Safe Approvals:** Sensitive actions cannot proceed without an explicit HTTP approval event signed by an authenticated organization member.
5. **Resilient Asynchrony:** Background tasks survive browser disconnects and stream progress uninterrupted when reconnected.
6. **Traceability:** Every model prompt, tool call, token cost, and approval decision is audited in PostgreSQL and traced in Langfuse.

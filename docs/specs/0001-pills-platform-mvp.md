# Specification: Pills Multi-Agent AI Teammate Platform (MVP)

## Problem Statement

Modern engineering, product, and operations teams spend an enormous amount of time on repetitive, fragmented workflows—such as triaging pull requests, investigating infrastructure alerts, synthesizing research documents, and debugging codebases. Existing AI chat assistants fail to function as true teammates for several core reasons:

1. **Lack of Specialization and Identity:** Generic chatbots have no consistent role, persistent persona, or bounded domain heuristics. Users must repeatedly re-prompt them with lengthy instructions.
2. **Fragile and Unsafe Execution:** Chat tools either execute unvetted code directly on host systems without isolation, or lack granular human-in-the-loop authorization gates, risking unauthorized mutations or data corruption.
3. **Transient and Volatile Runtimes:** Typical assistants rely on ephemeral HTTP connections. When network connections drop or a human approval takes hours to grant, long-running agent executions either fail, restart from scratch, or exhaust worker pool memory while blocked waiting.
4. **Poor Collaboration and Transparency:** Existing multi-agent frameworks operate as opaque "swarms" or flat, noisy group chats where sub-agents flood the conversation, burying actionable conclusions.
5. **Static and Rigid UI:** Traditional chat interfaces are restricted to markdown text blocks, forcing structured tabular data, metrics graphs, or configuration diffs into clumsy text snippets rather than interactive widgets.

## Solution

**Pills** delivers an enterprise-grade multi-agent SaaS platform where teams deploy, configure, and collaborate with specialized AI teammates ("Pills") encapsulated in distinctive cylindrical avatars with animated DiceBear Gaze expressions.

The platform provides:

1. **Unified Durable Task Execution:** Every interaction—from a quick conversational prompt to a multi-hour infrastructure diagnostic—runs as an asynchronous durable Task on background workers, streaming execution telemetry over Redis Streams with full SSE replay resilience.
2. **Stateless Checkpoint Resumption:** When a Pill encounters a high-risk tool action (e.g. merging code, deploying containers), the Tool Gateway intercepts the action, serializes the conversation and tool state to PostgreSQL, and suspends the worker. Once approved by a user, execution resumes via a synthetic tool return without idle worker consumption.
3. **Granular Security and Sandboxing:** An instruction-only Skill model ensures prompt SOPs cannot escalate permissions. STDIO Model Context Protocol (MCP) servers and command-line tasks execute inside isolated micro-containers and thread-scoped sandboxes with automated idle timeouts.
4. **Hierarchical Multi-Agent Collaboration:** Agent Groups operate with an explicit Lead Pill who orchestrates the team and delegates subtasks to Member Pills. Delegated execution traces are rendered in collapsible Subtask Delegation Cards, keeping the main conversational timeline focused on outcomes.
5. **Catalog-Driven Generative UI:** Pills dynamically render interactive, schema-validated React widgets (data tables, diff viewers, metrics charts) securely within sandboxed frames rather than running arbitrary generated code.

---

## User Stories

### Core Identity & Thread Interaction
1. As an organization member, I want to view my workspace's roster of Pills with their cylindrical capsule avatars and animated DiceBear Gaze eyes, so that I immediately recognize each AI teammate's role and status.
2. As an organization member, I want to create a new Thread with a specific Pill, so that I can collaborate on a dedicated initiative without conversational crosstalk.
3. As an organization member, I want to send a Message in a Thread and immediately receive word-by-word streamed responses, so that my conversational feedback loop remains instantaneous.
4. As an organization member, I want to see a live LED halo on a Pill's avatar indicating whether it is idle, thinking, executing a tool, or awaiting approval, so that I have immediate ambient awareness of its state.
5. As an organization member, I want to disconnect or refresh my browser during a long-running Task and have the execution stream seamlessly resume using `Last-Event-ID`, so that I never lose progress or view a broken UI.
6. As an organization member, I want intermediate tool execution traces and subtask logs isolated in collapsible cards rather than cluttering the primary Thread timeline, so that the conversation stays readable and executive-focused.
7. As an organization member, I want to edit a previous Message in a Thread and branch the conversation, so that I can explore alternative instructions without losing earlier history.

### Tool Registry, Gateway & Security Policy
8. As a workspace administrator, I want a centralized Tool Registry cataloging all available capabilities with risk classifications, so that I can audit and govern external system access.
9. As a workspace administrator, I want to configure per-Pill tool permissions (`ALLOW`, `REQUIRE_APPROVAL`, `DENY`), so that specialized Pills adhere strictly to the principle of least privilege.
10. As an organization member, I want a Pill attempting to execute an unauthorized tool to be rejected deterministically by the Tool Gateway with an explanatory audit log, so that system security is never bypassed.
11. As a platform engineer, I want all tool callables wrapped with a standardized security decorator preserving native Python function signatures, so that typing and validation remain idiomatic across all tools.
12. As a workspace administrator, I want all Tasks to enforce a hard Step Cap of 25 tool cycles, so that runaway agent loops and unexpected LLM billing spikes are prevented.
13. As a compliance officer, I want every tool invocation, duration, argument payload, and output logged to `task_events`, so that complete forensic audit trails are maintained.

### Human-in-the-Loop & Stateless Resumption
14. As an organization member, I want a Task to pause at an Approval Gate when an agent invokes a high-risk tool, so that dangerous modifications cannot execute without explicit authorization.
15. As an organization member, I want an inline Approval Card displayed in the Thread showing the exact tool parameters and proposed diff, so that I can review the action in context.
16. As a workspace administrator, I want worker processes to cleanly suspend and persist a Task Checkpoint to PostgreSQL during approval waits, so that background worker resources are not starved.
17. As an authorized approver, I want to click `Approve` on an Approval Card, so that the Task resumes on a fresh worker with a synthetic `ToolReturn` payload containing the execution output.
18. As an authorized approver, I want to click `Reject` with optional feedback on an Approval Card, so that the Task resumes with a rejection message informing the Pill to adjust its approach.
19. As an organization member, I want to receive multi-channel inbox notifications when a Task is blocked waiting for my approval, so that urgent workflows do not stall.

### Sandboxed MCP & Execution Isolation
20. As a workspace administrator, I want to connect external MCP servers over SSE or containerized STDIO, so that Pills can interact with external services like GitHub or Linear.
21. As a security architect, I want STDIO MCP subprocesses isolated in dedicated micro-containers with encrypted credential injection, so that host environments and cluster networks are protected from compromised packages.
22. As an organization member collaborating on code, I want a Pill to execute terminal commands and tests inside an isolated E2B Sandbox Session, so that the host system remains untouched.
23. As a platform administrator, I want Thread-scoped sandboxes to automatically shut down after 15 minutes of inactivity or upon thread closure, so that idle cloud compute costs are eliminated while preserving multi-turn filesystem state.

### Skills & Version Pinning
24. As a prompt engineer, I want to author declarative, instruction-only Standard Operating Procedures (`SKILL.md`) in Skill Studio, so that Pills follow rigorous step-by-step methodologies.
25. As a prompt engineer, I want a Skill to declare prerequisite tools without granting or bundling executable code, so that Skills cannot introduce unauthorized privilege escalation.
26. As a workspace administrator, I want Skills published as immutable, semver-pinned Skill Releases, so that modifications in Skill Studio do not destabilize active production Pills.
27. As a prompt engineer, I want to run Promptfoo regression evaluations against a Skill Release before promoting it, so that prompt enhancements are quantitatively proven.
28. As an organization member, I want a Pill executing a Skill to automatically verify all prerequisite tools exist in its assigned permissions before running, so that missing capability failures are surfaced immediately.

### Agent Groups & Hierarchical Collaboration
29. As an organization member, I want to create an Agent Group by selecting a designated Lead Pill and static Member Pills, so that complex multifaceted projects can be tackled by a coordinated team.
30. As an organization member, I want the Lead Pill to orchestrate subtask assignments to Member Pills, so that specialized tasks are handled by the appropriate expert Pill.
31. As an organization member, I want subtask progress for each Member Pill streamed within an inline Subtask Delegation Card displaying the member's avatar and tool traces, so that multi-agent execution remains transparent.
32. As an organization member, I want the Lead Pill to synthesize member findings into a single executive response in the primary Thread timeline, so that I receive cohesive conclusions without cross-agent chatter.

### Generative UI
33. As an organization member, I want Pills to render rich, interactive Generative UI Components (such as Data Tables, Metrics Charts, and Diff Viewers) directly inside the Thread, so that complex outputs are easy to consume and interact with.
34. As a frontend engineer, I want Generative UI to be strictly catalog-driven from pre-registered, typed React widgets using schema-validated `render_widget` calls, so that arbitrary unvetted code execution and XSS vulnerabilities are eliminated.
35. As an organization member, I want Generative UI components to be responsive, theme-aware, and exportable, so that I can sort tables, filter metrics, and download artifacts directly from the chat.

### Memory & Tenant Scoping
36. As an organization member, I want Pills to recall relevant operational heuristics and user preferences across Threads via asynchronous memory extraction, so that I do not have to repeat context.
37. As an enterprise administrator, I want memories strictly partitioned into User Scope, Agent Private Scope, and Organization Scope, so that sensitive agent learnings or private user data never leak across boundaries.
38. As an enterprise administrator, I want multi-tenant data strictly isolated at the application level via dependency-injected Tenant Context across all queries and background workers, so that cross-tenant access is impossible.

---

## Implementation Decisions

### 1. Modules Built & Modified
- **`TenantContext` Dependency Injection Module:** Authenticates requests via BetterAuth, extracts organization and user identifiers, and injects a validated context object into every FastAPI route, database query, and SAQ worker task.
- **`DurableTaskEngine` & Worker Pool Module:** Manages the lifecycle of background execution tasks running on SAQ. Dispatches tasks, records `task_events`, writes state snapshots, and streams updates into Redis Streams (`task:{id}:events`).
- **`SSEEventReplay` Endpoint Module:** Implements server-sent events with standard `Last-Event-ID` header processing. On client reconnection, reads all missed events from Redis Streams offsets before subscribing to live pub/sub events.
- **`ToolGateway` Decorator Module:** Standardized decorator wrapping all tool functions before registration with Pydantic AI. Verifies tenant and agent permissions against `agent_tool_permissions`, checks the 25-step cap, audits call metadata to `task_events`, and raises `ApprovalRequiredInterrupt`.
- **`StatelessCheckpointResumption` Module:** Catches `ApprovalRequiredInterrupt`, serializes model message history and tool parameters to `tasks.checkpoint_state`, sets task status to `PAUSED_APPROVAL`, and cleanly terminates the SAQ worker. Handles approval/rejection webhooks by dispatching a new worker with synthetic `ToolReturn` data.
- **`MCPConnectionManager` Module:** Manages connections to external MCP servers. Directs remote SSE MCP connections through authenticated client proxies and routes local STDIO MCP tools into isolated Docker/E2B micro-containers.
- **`SkillStudio` & Release Module:** Parses frontmatter and instructions from `SKILL.md`, checks tool prerequisite declarations, tags immutable semver `skill_releases`, and binds releases to Pills.
- **`AgentGroupCoordinator` Module:** Orchestrates multi-agent execution. Designates a Lead Pill who receives the user prompt and delegates subtasks to Member Pills, emitting nested delegation events rendered inside Subtask Delegation Cards.
- **`GenerativeUICatalog` Module:** Registers schema-validated React widgets (`DataTableWidget`, `MetricsChartWidget`, `DiffViewerWidget`). Emits `render_widget` tool invocations parsed and rendered securely by the frontend.
- **`CapsuleAvatar` & Workspace Frontend Module:** Integrates `assistant-ui` primitives, DiceBear Gaze animated SVGs, live LED halos, inline Approval Cards, and Novu notification widgets.

### 2. Interfaces & API Contracts

#### A. Durable Task & Event Replay Interface
- **Trigger Task:** `POST /api/v1/threads/{thread_id}/messages`
  - *Payload:* `{ content: string, parent_message_id?: UUID }`
  - *Response:* `{ message_id: UUID, task_id: UUID, status: "queued" }`
- **Stream Task Events (SSE):** `GET /api/v1/tasks/{task_id}/events`
  - *Headers:* `Last-Event-ID: <redis_stream_id>`
  - *Emitted Events:* `task.started`, `step.delta`, `tool.invoked`, `tool.completed`, `approval.required`, `widget.emitted`, `delegation.started`, `delegation.completed`, `task.completed`, `task.failed`
- **Resolve Approval:** `POST /api/v1/approvals/{approval_id}`
  - *Payload:* `{ decision: "APPROVED" | "REJECTED", feedback?: string }`
  - *Response:* `{ status: "resuming", task_id: UUID }`

#### B. Tool Gateway Decorator Contract
```python
# Prototype contract encoding Tool Gateway decorator behavior
def secure_tool_gate(tool_def: ToolDefinition):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, ctx: RunContext, **kwargs):
            agent_id = ctx.deps.agent_id
            tenant_id = ctx.deps.tenant_id
            task_id = ctx.deps.task_id

            # 1. Enforce Step Cap
            if ctx.deps.current_step >= 25:
                raise StepCapExceededException(task_id, step=25)

            # 2. Check Permission Policy
            permission = await get_tool_permission(tenant_id, agent_id, tool_def.name)
            if permission == "DENY":
                raise PermissionDeniedException(f"Tool {tool_def.name} is not permitted for agent {agent_id}")

            # 3. Intercept for Human Approval
            if permission == "REQUIRE_APPROVAL":
                raise ApprovalRequiredInterrupt(
                    tool_name=tool_def.name,
                    arguments=kwargs,
                    risk_level=tool_def.risk_level
                )

            # 4. Execute and Record Telemetry
            start = time.perf_counter()
            result = await func(*args, **kwargs)
            duration_ms = int((time.perf_counter() - start) * 1000)
            await record_task_event(task_id, "tool.completed", {
                "tool": tool_def.name,
                "duration_ms": duration_ms
            })
            return result
        return wrapper
    return decorator
```

#### C. Stateless Checkpoint Resumption Flow
1. Tool Gateway raises `ApprovalRequiredInterrupt`.
2. Worker catches interrupt, writes serialized Pydantic AI message history into `tasks.checkpoint_state`, sets `tasks.status = 'paused_approval'`, commits an `approvals` row, and exits cleanly.
3. User posts decision to `/api/v1/approvals/{id}`.
4. API validates user authorization in `TenantContext`, marks approval record resolved, and enqueues an SAQ resumption task.
5. Resumed worker instantiates Pydantic AI agent, injects checkpointed message history, and injects a synthetic `ToolReturn` (containing execution result on approval, or error rationale on rejection) to resume generation seamlessly.

### 3. Database Schema Entities

```sql
-- Core Schema Architecture
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    slug VARCHAR(100) NOT NULL,
    name VARCHAR(150) NOT NULL,
    role VARCHAR(150) NOT NULL,
    model_name VARCHAR(100) NOT NULL,
    system_prompt TEXT NOT NULL,
    avatar_config JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(org_id, slug)
);

CREATE TABLE threads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL DEFAULT 'New Conversation',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    thread_id UUID NOT NULL REFERENCES threads(id) ON DELETE CASCADE,
    org_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    agent_id UUID REFERENCES agents(id) ON DELETE SET NULL,
    author_type VARCHAR(20) NOT NULL, -- 'user', 'agent', 'system'
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    thread_id UUID NOT NULL REFERENCES threads(id) ON DELETE CASCADE,
    trigger_message_id UUID REFERENCES messages(id) ON DELETE SET NULL,
    agent_id UUID NOT NULL REFERENCES agents(id),
    status VARCHAR(50) NOT NULL, -- 'queued', 'running', 'paused_approval', 'completed', 'failed'
    checkpoint_state JSONB,
    step_count INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE task_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    event_seq INT NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    payload JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(task_id, event_seq)
);

CREATE TABLE approvals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    org_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    tool_name VARCHAR(150) NOT NULL,
    tool_args JSONB NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'PENDING', -- 'PENDING', 'APPROVED', 'REJECTED'
    decision_reason TEXT,
    decided_by_user_id UUID,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    decided_at TIMESTAMPTZ
);

CREATE TABLE tool_registry (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    risk_level VARCHAR(30) NOT NULL DEFAULT 'NORMAL', -- 'NORMAL', 'HIGH', 'CRITICAL'
    parameters_schema JSONB NOT NULL,
    UNIQUE(org_id, name)
);

CREATE TABLE agent_tool_permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    tool_id UUID NOT NULL REFERENCES tool_registry(id) ON DELETE CASCADE,
    permission VARCHAR(30) NOT NULL DEFAULT 'REQUIRE_APPROVAL', -- 'ALLOW', 'REQUIRE_APPROVAL', 'DENY'
    UNIQUE(agent_id, tool_id)
);

CREATE TABLE skills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    slug VARCHAR(100) NOT NULL,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    UNIQUE(org_id, slug)
);

CREATE TABLE skill_releases (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    skill_id UUID NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
    version VARCHAR(30) NOT NULL, -- Semver '1.0.0'
    skill_markdown TEXT NOT NULL,
    required_tool_names JSONB NOT NULL DEFAULT '[]',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(skill_id, version)
);

CREATE TABLE agent_groups (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(150) NOT NULL,
    lead_agent_id UUID NOT NULL REFERENCES agents(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE agent_group_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    group_id UUID NOT NULL REFERENCES agent_groups(id) ON DELETE CASCADE,
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    UNIQUE(group_id, agent_id)
);
```

---

## Testing Decisions

### What Makes a Good Test
Tests must verify observable external behavior and contracts rather than internal class implementations:
- **No White-Box Private State Testing:** Never assert private helper methods or monkey-patched internal structures. Tests interact with the module at its public interface seam.
- **Deterministic and Fast:** Network boundaries (LLMs, external MCP servers, cloud microVMs) are substituted at adapter seams with deterministic recorded responses or lightweight fakes.
- **Resilience and State Verification:** Tests must assert database persistence invariants, event sequence offsets in Redis Streams, and clean resumption across process suspension.

### Modules Tested
1. **Durable Task & SSE Event Pipeline:** Test end-to-end task dispatching, sequential event emissions, and `Last-Event-ID` reconnection replay.
2. **Tool Gateway Decorator:** Test permission enforcement (`ALLOW`, `REQUIRE_APPROVAL`, `DENY`), step cap termination at step 25, and telemetry event recording.
3. **Stateless Checkpoint Resumption:** Test interrupt handling, checkpoint state serialization to PostgreSQL, worker exit, and successful resumption via synthetic `ToolReturn` upon approval.
4. **Tenant Context Isolation:** Test cross-tenant query prevention and tenant scoping on all API endpoints and background workers.
5. **Agent Group Subtask Delegation:** Test Lead Pill subtask delegation to Member Pills and emission of nested delegation events.
6. **Frontend Stream & UI Components:** Test assistant-ui SSE streaming consumption, Inline Approval Card actions, and Generative UI widget schema validation.

### Testing Seams

#### 1. Primary External Seam: The HTTP & SSE API Seam (Highest Seam)
- **Location:** The FastAPI HTTP and Server-Sent Event boundary (`/api/v1/*`).
- **Surface:** Client sends HTTP requests with Bearer auth headers, listens to `/tasks/{id}/events` SSE streams, and posts approvals.
- **Coverage:** Exercises full integration across TenantContext dependency injection, database transactions, SAQ job dispatch, Pydantic AI execution loop, Tool Gateway wrapper, Redis Streams publishing, and checkpoint state persistence.
- **Adapter Swaps:** Swaps the upstream LiteLLM client with an in-memory LLM adapter, and replaces E2B sandboxes with a local container/in-memory filesystem adapter.

#### 2. Secondary Core Seam: Forge Task Engine Seam
- **Location:** `TaskExecutor.run_task(task_id: UUID, tenant: TenantContext) -> AsyncIterator[TaskEvent]`.
- **Surface:** Direct invocation of the agent execution lifecycle without HTTP network overhead.
- **Coverage:** Exercises Tool Gateway decorator, permission checks, `ApprovalRequiredInterrupt` capture, checkpoint state serialization, and event sequence indexing.

#### 3. Frontend UI Seam: Custom SSE Adapter & Widget Registry
- **Location:** The React SSE stream consumer and `<GenerativeUIWidget />` catalog dispatcher.
- **Surface:** Simulates incoming SSE event payloads (`step.delta`, `approval.required`, `widget.emitted`) and verifies DOM updates, interactive card states, and form submission callbacks.

### Prior Art
- **Standard Async Integration Tests:** FastAPI `httpx.AsyncClient` + `pytest-asyncio` test suites running against disposable PostgreSQL and Redis test containers.
- **VCR / Mock Model Testing:** Deterministic JSON fixture replays for Pydantic AI model interactions.

---

## Out of Scope

1. **Dynamic Agent Recruitment (Phase 2):** In MVP (Sprint 1–4), Agent Groups have statically configured Lead and Member Pills. Dynamic autonomous recruitment tools for Lead Pills are deferred to Phase 6.
2. **Arbitrary Code Evaluation in Generative UI:** Client-side execution of dynamic, unvetted JavaScript/React code synthesized on the fly is strictly prohibited to eliminate XSS risks. Only catalog-registered widgets are supported.
3. **Host Subprocess Execution for STDIO MCP:** STDIO MCP servers cannot execute directly on the FastAPI or SAQ host OS; they must execute within containerized micro-sandboxes.
4. **Database-Level Row-Level Security (RLS):** RLS policies on PostgreSQL are replaced with application-level TenantContext dependency injection.
5. **Computer Use via Agent Zero (Phase 7):** Full OS mouse, keyboard, and display automation is deferred to post-MVP roadmap.
6. **Permanent Sandbox Daemons:** Sandboxes are thread-scoped with a 15-minute inactivity TTL; continuous always-on container instances are out of scope.

---

## Further Notes

- **Domain Language Conformance:** All module interfaces, database tables, and UI components strictly follow [GLOSSARY.md](file:///c:/Users/Admin/Desktop/pills/GLOSSARY.md). Terms such as "bot", "swarm", "job", and "plugin" are prohibited in code and documentation.
- **ADR Alignment:** This specification realizes all 16 settled Architectural Decision Records located in [docs/adr/](file:///c:/Users/Admin/Desktop/pills/docs/adr/):
  - [0001-unified-durable-task-execution.md](file:///c:/Users/Admin/Desktop/pills/docs/adr/0001-unified-durable-task-execution.md)
  - [0002-stateless-checkpoint-resumption-for-approvals.md](file:///c:/Users/Admin/Desktop/pills/docs/adr/0002-stateless-checkpoint-resumption-for-approvals.md)
  - [0003-catalog-driven-generative-ui.md](file:///c:/Users/Admin/Desktop/pills/docs/adr/0003-catalog-driven-generative-ui.md)
  - [0004-sandboxed-isolation-for-stdio-mcp.md](file:///c:/Users/Admin/Desktop/pills/docs/adr/0004-sandboxed-isolation-for-stdio-mcp.md)
  - [0005-thread-message-and-task-decoupling.md](file:///c:/Users/Admin/Desktop/pills/docs/adr/0005-thread-message-and-task-decoupling.md)
  - [0006-interrupt-and-synthetic-tool-return-resumption.md](file:///c:/Users/Admin/Desktop/pills/docs/adr/0006-interrupt-and-synthetic-tool-return-resumption.md)
  - [0007-agent-groups-with-phased-membership-delegation.md](file:///c:/Users/Admin/Desktop/pills/docs/adr/0007-agent-groups-with-phased-membership-delegation.md)
  - [0008-instruction-only-skill-boundaries.md](file:///c:/Users/Admin/Desktop/pills/docs/adr/0008-instruction-only-skill-boundaries.md)
  - [0009-thread-scoped-sandboxes-with-inactivity-ttl.md](file:///c:/Users/Admin/Desktop/pills/docs/adr/0009-thread-scoped-sandboxes-with-inactivity-ttl.md)
  - [0010-partitioned-scoped-memory-pipeline.md](file:///c:/Users/Admin/Desktop/pills/docs/adr/0010-partitioned-scoped-memory-pipeline.md)
  - [0011-hierarchical-group-delegation-ui.md](file:///c:/Users/Admin/Desktop/pills/docs/adr/0011-hierarchical-group-delegation-ui.md)
  - [0012-immutable-skill-version-pinning.md](file:///c:/Users/Admin/Desktop/pills/docs/adr/0012-immutable-skill-version-pinning.md)
  - [0013-application-level-tenant-context-scoping.md](file:///c:/Users/Admin/Desktop/pills/docs/adr/0013-application-level-tenant-context-scoping.md)
  - [0014-tool-gateway-callable-decorator-pattern.md](file:///c:/Users/Admin/Desktop/pills/docs/adr/0014-tool-gateway-callable-decorator-pattern.md)
  - [0015-resilient-event-replay-via-redis-streams.md](file:///c:/Users/Admin/Desktop/pills/docs/adr/0015-resilient-event-replay-via-redis-streams.md)
  - [0016-sprint-one-unified-task-engine-alignment.md](file:///c:/Users/Admin/Desktop/pills/docs/adr/0016-sprint-one-unified-task-engine-alignment.md)
- **Tracker Integration:** To publish this specification into your issue tracker with appropriate triage labels, configure your repository's tracker by running `/setup-matt-pocock-skills`.

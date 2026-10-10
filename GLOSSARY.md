# Pills Domain Glossary

The canonical domain language for the Pills multi-agent AI teammate platform.

## Core Entities

**Pill**:
An autonomous AI teammate with a distinct persona, system prompt, visual capsule identity, and scoped tool permissions.
_Avoid_: Bot, assistant, custom GPT, agent instance

**Skill**:
A versioned, declarative Standard Operating Procedure document (`SKILL.md`) that instructs a Pill how to perform a specialized workflow.
_Avoid_: Prompt template, playbook, macro, script

**Thread**:
A persistent conversational timeline in a workspace containing an ordered sequence of messages and task executions.
_Avoid_: Chat, session, channel, room

**Message**:
A discrete conversational entry within a Thread authored by a user, a Pill, or the system.
_Avoid_: Prompt, comment, response, turn

**Agent Group**:
A configured ensemble of Pills led by a designated Lead Pill (admin) who orchestrates work across member Pills.
_Avoid_: Multi-agent room, swarm, gang, cluster

**Task**:
A durable, stateful asynchronous execution unit initiated by a user or event, executed by worker pools, and producing an event stream.
_Avoid_: Job, run, invocation, turn

## Execution & Security

**Tool Registry**:
A tenant-wide catalog registering all available executable capabilities and their risk classifications.
_Avoid_: Function list, plugin directory, tool store

**Tool Gateway**:
A security policy enforcement point that intercepts tool invocations to validate permissions, enforce rate limits, and trigger approvals.
_Avoid_: API proxy, middleware wrapper

**Approval Gate**:
A suspension point where a Task safely pauses execution because an invoked tool requires explicit human authorization.
_Avoid_: Checkpoint, interrupt, prompt blocker

**Task Checkpoint**:
A serialized snapshot of a Task's accumulated model message history and pending tool parameters saved to PostgreSQL during suspension.
_Avoid_: Save state, task freeze, snapshot

**Step Cap**:
A hard ceiling on the maximum number of tool invocation cycles a single Task may execute before requiring human intervention.
_Avoid_: Loop limit, recursion depth, max iterations

**Generative UI Component**:
A client-side interactive React widget selected from a typed, pre-registered catalog and populated by agent JSON payloads.
_Avoid_: Dynamic iframe, generated code, AI script

## Runtime, Memory & Governance

**Tenant Context**:
An authenticated organization boundary dependency injected into requests and workers that strictly scopes all database operations.
_Avoid_: Org filter, tenant flag, workspace session

**Tool Wrapper**:
A runtime security decorator encapsulating tool callables to evaluate permissions, enforce approval pauses, and capture execution metrics.
_Avoid_: Tool handler, function interceptor, execution hook

**Event Stream Replay**:
A resilient streaming protocol using Redis Streams and `Last-Event-ID` that replays missed task execution events across client reconnections.
_Avoid_: Event buffer, stream cache, message backlog

**Sandbox Session**:
An isolated microVM execution environment scoped to a Thread with an automated idle timeout for stateful command runs.
_Avoid_: Container instance, VM pod, shell session

**Memory Scope**:
A partitioning boundary that strictly isolates memory facts into User, Agent Private, or Organization visibility domains.
_Avoid_: Memory tag, vector namespace, context partition

**Subtask Delegation Card**:
An inline, expandable UI container inside a Thread rendering the private execution trace of a member Pill directed by the Lead Pill.
_Avoid_: Child chat, subthread, agent bubble

**Skill Release**:
An immutable, semver-tagged snapshot of a Skill document that can be deterministically pinned to Pills.
_Avoid_: Skill draft, skill revision, prompt version

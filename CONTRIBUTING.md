# Contributing to Pills

Thank you for your interest in contributing to **Pills**! This document provides operational guidelines, engineering standards, and development workflows for contributors and AI agents working on this repository.

---

## 🏛️ Guiding Philosophy

1. **Adhere to the Domain Language**: Always use canonical terms defined in [`GLOSSARY.md`](GLOSSARY.md).
   - Use **Pill** (never "bot", "assistant", or "agent instance").
   - Use **Skill** (never "playbook" or "macro").
   - Use **Thread** (never "chat" or "session").
   - Use **Message** (never "turn" or "prompt").
   - Use **Agent Group** (never "swarm" or "cluster").
   - Use **Task** (never "job" or "run").
   - Use **Task Checkpoint** (never "snapshot" or "freeze").
   - Use **Tool Gateway** (never "middleware proxy").
   - Use **Tenant Context** (never "org filter" or "workspace session").

2. **Respect Settled ADRs**:
   All architectural decisions are governed by the 16 ADRs in [`docs/adr/`](docs/adr/). If your proposed changes contradict an ADR, you must explicitly flag and justify the reopening in your proposal.

3. **Application-Level Multi-Tenancy**:
   All database queries, background workers, and API endpoints must inject and validate `TenantContext` ([ADR-0013](docs/adr/0013-application-level-tenant-context-scoping.md)). Never query multi-tenant models without strict organization scoping.

---

## 🛠️ Prerequisites

Ensure you have the following installed on your machine:
- **Node.js**: v20+ (recommended: v22+ or v24)
- **pnpm**: v10+ (`corepack enable && corepack use pnpm@latest` or `npm install -g pnpm`)
- **Python**: 3.12 (managed natively via `uv`)
- **uv**: Fast Python package manager ([docs.astral.sh/uv](https://docs.astral.sh/uv/))
- **Docker**: Docker Desktop or Docker Engine with Docker Compose v2+

---

## 🚀 Local Development Setup

### 1. Clone the Repository
```bash
git clone https://github.com/sandilya27/Pills.git
cd Pills
```

### 2. Start PostgreSQL & Redis Infrastructure
Launch PostgreSQL 16 (with `pgvector`) and Redis 7 in the background:
```bash
docker compose up -d
```
Verify container health:
```bash
docker compose ps
```

### 3. Install Python Dependencies & Workspace Packages
Install dependencies into the root virtual environment using `uv`:
```bash
uv sync --python 3.12
```

### 4. Install Node Dependencies
Install frontend and monorepo dependencies using `pnpm`:
```bash
pnpm install
```

### 5. Seed the Development Database
Seed the demo organization (`Acme Cybernetics`) and demo user (`Alex Vance`):
```bash
pnpm db:seed
# Alternatively:
uv run --directory apps/api python -m api.db.seed
```

### 6. Run the Application

You can start both services independently or concurrently:

#### Start API Backend (FastAPI on `:8000`)
```bash
pnpm dev:api
# Alternatively:
uv run --directory apps/api uvicorn api.main:app --reload --port 8000
```
- API root: `http://localhost:8000`
- Interactive OpenAPI Docs: `http://localhost:8000/docs`

#### Start Web Frontend (Next.js 15 on `:3000`)
```bash
pnpm dev:web
# Alternatively:
pnpm --filter @pills/web dev
```
- Web Application: `http://localhost:3000`

---

## 🧪 Testing Guidelines

We enforce rigorous test coverage verifying observable behavior at public seams rather than private implementation details.

### Running Backend Tests (Pytest)
```bash
pnpm test:api
# Alternatively:
uv run --directory apps/api pytest -v
```
Tests assert:
- Service connectivity (PostgreSQL 16 + Redis 7).
- Unauthenticated rejection (`401 Unauthorized`).
- Cross-tenant boundary breach rejection (`403 Forbidden`).
- Correct scoped `TenantContext` emission via JWT and database session tokens.

### Running Frontend Tests (Vitest)
```bash
pnpm test:web
# Alternatively:
pnpm --filter @pills/web test
```
Tests assert:
- Multi-tenant workspace rendering.
- End-to-end authenticated healthcheck ping from client to API.
- Error handling during simulated tenant boundary breaches.

### Running All Tests
```bash
pnpm test
# Alternatively:
pnpm test:api && pnpm test:web
```

---

## 🌿 Git & Contribution Workflow

### 1. Branch Naming Convention
Create a branch named after the initiative or ticket:
- `feat/<ticket-number>-<short-description>` (e.g. `feat/02-capsule-avatar-component`)
- `fix/<ticket-number>-<short-description>` (e.g. `fix/tenant-query-col-types`)
- `docs/<topic>` (e.g. `docs/update-run-guide`)

### 2. Issue Tracking & Triage
All tasks are tracked on GitHub Issues at `sandilya27/Pills`. We follow 5 canonical roles:
- `needs-triage`: Awaiting evaluation.
- `needs-info`: Waiting on the reporter.
- `ready-for-agent`: Fully specified and ready for autonomous agent execution.
- `ready-for-human`: Requires human implementation.
- `wontfix`: Will not be actioned.

Before beginning work on a ticket, assign yourself:
```bash
gh issue edit <issue-number> --add-assignee "@me"
```

### 3. Commit Style
Follow Conventional Commits:
- `feat: ...` for new features or capabilities
- `fix: ...` for bug fixes
- `refactor: ...` for structural code improvements without behavioral changes
- `test: ...` for new or modified test suites
- `docs: ...` for documentation updates
- `chore: ...` for tool or dependency updates

### 4. Pull Requests
1. Push your branch to GitHub:
   ```bash
   git push origin feat/your-feature-branch
   ```
2. Open a Pull Request referencing the parent ticket:
   ```bash
   gh pr create --title "feat: <description>" --body "Closes #<issue-number>"
   ```
3. Ensure CI passes:
   - Backend pytest suite passes.
   - Frontend vitest suite passes.
   - Next.js production build (`pnpm build:web`) compiles with zero errors.

---

## 🔒 Security & Code Standards

- **Never bypass TenantContext**: Every route accepting tenant input must inject `TenantContextDep`.
- **No dynamic eval in Generative UI**: Client-side generative widgets must be selected strictly from typed, pre-registered catalog schemas. Arbitrary dynamic JavaScript evaluation is strictly forbidden.
- **Secrets Management**: Never commit `.env` or production secrets. Use `.env.example` for configurable variables.

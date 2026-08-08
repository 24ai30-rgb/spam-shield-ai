# Spam Shield AI
### Multi-Agent Cyber Threat Detection & Scam Intelligence Platform

Production-grade full-stack implementation of the approved architecture: a FastAPI backend
running 13 specialized AI agents behind an orchestrator, and a Next.js 14 frontend covering
the full consumer product surface (dashboard, upload center, history, community, analytics,
AI chatbot, premium, settings).

---

## 1. Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 14 (App Router), TypeScript, TailwindCSS, React Query, Zustand, Recharts |
| Backend | FastAPI (async), SQLAlchemy 2.0, Pydantic v2, structlog |
| Database | PostgreSQL 16 (+ pgvector-ready image) |
| Cache/Rate-limit | Redis 7 |
| AI | Google Gemini API (`google-generativeai`) |
| OCR | Tesseract (OpenCV pre-processing) |
| QR decode | pyzbar + OpenCV |
| PDF reports | WeasyPrint + Jinja2 |
| Auth | JWT (access + refresh), bcrypt password hashing, RBAC |
| Containerization | Docker + docker-compose |

---

## 2. Quick Start (Docker — recommended)

```bash
cp backend/.env.example backend/.env
# edit backend/.env and set GEMINI_API_KEY (required for AI-powered reasoning agents;
# the platform still runs and scores without it, just without Tier-2 LLM escalation)

docker-compose up --build
```

- Backend API: http://localhost:8000/api/v1
- Interactive API docs (Swagger): http://localhost:8000/api/docs
- Frontend: http://localhost:3000

The backend container runs `alembic upgrade head` automatically on startup.

## 3. Manual Local Setup

### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # edit values
alembic revision --autogenerate -m "init schema"
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
cp .env.local.example .env.local
npm install
npm run dev
```

---

## 4. Architecture Overview

```
Client (Next.js) -> FastAPI API layer -> Orchestrator -> 13 Specialist Agents
                                              |
                          Risk Aggregator -> Explainability Agent -> Recommendation Agent
                                              |
                          PostgreSQL (persist verdict) + PDF report + Notification
```

### 4.1 The 13 Agents (`backend/app/agents/`)

| Agent | File | Role |
|---|---|---|
| URL Analysis Agent | `url_agent.py` | Phishing/typosquat/domain-reputation scoring |
| Email Analysis Agent | `email_agent.py` | Header spoofing, urgency language, link density |
| Phone Reputation Agent | `phone_agent.py` | Spam-number lookup, premium-rate prefix detection |
| Message Analysis Agent | `message_agent.py` | SMS/WhatsApp smishing detection (delegates URLs to URL Agent) |
| OCR Agent | `ocr_agent.py` | Screenshot text extraction + fake-UI language detection |
| QR Agent | `qr_agent.py` | QR payload decode + recursive routing |
| Job Scam Agent | `domain_agents.py` | Advance-fee/fake-recruiter pattern detection |
| Banking Fraud Agent | `domain_agents.py` | OTP/PIN solicitation, fake bank-alert detection |
| Shopping Scam Agent | `domain_agents.py` | Fake storefront heuristics |
| Investment Fraud Agent | `domain_agents.py` | Ponzi/pyramid linguistic markers, unrealistic ROI |
| Risk Aggregator Agent | `risk_aggregator_agent.py` | Weighted fusion of all findings into one score |
| Explainability Agent | `explainability_agent.py` | Evidence-grounded, human-readable reasoning |
| Recommendation Agent | `recommendation_agent.py` | Deterministic, safety-critical next-step actions |

**Orchestrator** (`orchestrator.py`) routes each `InputType` to the right agent(s), runs them
in parallel via `asyncio.gather`, then pipes the results through the aggregator, explainer, and
recommender chain and returns one unified `OrchestrationResult`.

### 4.2 Tiered AI Strategy
Every specialist agent runs cheap deterministic checks first (regex/heuristics/threat-intel
lookup). Gemini is only called when that signal is ambiguous (score 25-75), keeping latency
and cost predictable. The `GeminiService` wraps every LLM call with a prompt-injection
guardrail: submitted content is always treated as untrusted `<data>`, never as instructions.

### 4.3 Risk Scoring
Implemented per the approved formula:
```
RiskScore = clamp(0,100, sum(AgentScore * Weight * Confidence) + ThreatIntelBoost + CommunityBoost - TrustDiscount)
```
See `risk_aggregator_agent.py` for the versioned weight table and verdict bands.

---

## 5. API Surface

All routes are prefixed with `/api/v1`. Full interactive docs at `/api/docs`.

| Method | Route | Purpose |
|---|---|---|
| POST | `/auth/register` | Create account, returns JWT pair |
| POST | `/auth/login` | Authenticate, returns JWT pair |
| POST | `/auth/refresh` | Rotate access token |
| GET | `/auth/me` | Current user profile |
| POST | `/scans` | Submit text-based scan (URL/email/phone/sms/job/banking/shopping/investment) |
| POST | `/scans/upload` | Submit file-based scan (screenshot/QR/document) |
| GET | `/scans/{id}` | Get scan status + verdict + full agent breakdown |
| GET | `/scans` | Scan history for current user |
| GET | `/scans/{id}/report.pdf` | Download forensic PDF report |
| POST | `/community/reports` | Submit a community scam report |
| POST | `/community/reports/{id}/upvote` | Corroborate a report (auto-promotes to threat intel at 3+ upvotes) |
| POST | `/community/reports/{id}/verify` | Moderator approve/reject (requires `moderator` role) |
| GET | `/community/trending` | Trending scams feed |
| GET | `/dashboard/stats` | Aggregated stats for the dashboard |
| POST | `/chatbot/message` | AI cyber-safety assistant |
| GET | `/notifications` | In-app notifications |

---

## 6. Security Notes

- Passwords hashed with bcrypt; JWTs are short-lived (15 min access / 7 day refresh).
- RBAC enforced via `require_role()` dependency factory (`Role.USER` up to `Role.ADMIN` hierarchy).
- All uploads are size-capped (`MAX_UPLOAD_MB`) before processing.
- Every LLM call wraps user content in an explicit untrusted-data boundary to resist prompt injection.
- Structured JSON logging with request-correlation IDs (`RequestContextMiddleware`) for audit trails.
- Rate limiting is Redis-backed, tiered by plan (`free` / `premium` / `business`).

## 7. What's Illustrative vs. Production-Ready

This is a complete, coherent, runnable full-stack scaffold implementing every requirement in
the approved architecture. A few pieces are intentionally simplified and flagged for a real
production rollout:

- **Threat-intel feeds**: `ThreatIntelIOC` table + lookup service is fully wired, but the
  scheduled sync jobs pulling from Safe Browsing/PhishTank/AbuseIPDB are not included — add a
  `threat_intel_sync.py` Celery task per the architecture doc's Section 15.
- **Email/SMS/Push notification delivery**: `NotificationService` persists in-app notifications
  and has clear extension points for SES/Twilio/FCM adapters — wire real credentials per deployment.
- **WHOIS domain-age lookups** in the URL agent are structurally ready but not calling a live
  WHOIS provider — add `python-whois` calls where noted.
- **Alembic migrations**: `env.py` is fully configured; run `alembic revision --autogenerate`
  once against a live Postgres instance to generate the initial migration file.
- **Tests**: `backend/tests/` directory scaffolded but not populated — recommend `pytest` +
  `httpx.AsyncClient` for endpoint tests and per-agent unit tests using the `AgentFinding` contract.

## 8. Folder Structure

```
spam-shield-ai/
├── backend/
│   ├── app/
│   │   ├── agents/          # 13 specialist agents + orchestrator
│   │   ├── api/v1/routers/  # auth, scans, community, dashboard, chatbot, notifications
│   │   ├── core/            # config, security, logging, exceptions
│   │   ├── db/               # session, declarative base
│   │   ├── middleware/       # rate limiting, request context
│   │   ├── models/           # SQLAlchemy ORM models
│   │   ├── schemas/          # Pydantic request/response schemas
│   │   └── services/         # gemini, ocr, pdf, cache, threat-intel, notifications
│   ├── alembic/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── app/                  # Next.js App Router pages
│   ├── components/           # layout + chart components
│   ├── lib/                  # api client, store, utils
│   └── package.json
├── docker-compose.yml
└── README.md
```

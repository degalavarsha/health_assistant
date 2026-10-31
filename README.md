# AI Health Assistant

Health information assistant: guideline-based lab interpretation, risk screening,
RAG answers with citations, wellness check-ins, English voice entry, and a
research-only chest X-ray demo. Educational use only; not a medical device.

## Layout

```
backend/            FastAPI service
  app/              api/v1 (routes) · core (config, auth) · schemas · services (rules, llm, imaging)
  tests/            pytest suite
frontend/           Next.js 16 + Tailwind (App Router, src/)
ml/
  ingest/           data download + RAG ingestion scripts
  training/         model training and evaluation (training/legacy = old notebooks)
data/               nhanes/ (P_ and L cycles) · knowledge/ (RAG documents)   [gitignored]
models/             trained weights                                          [gitignored]
docs/               reports/ and research_notes/ (data-source research)
.env                all backend secrets (one file at the repo root)          [gitignored]
```

## Run

```bash
# one-time
python -m venv venv                         # Python 3.11
venv/Scripts/python -m pip install -r backend/requirements-dev.txt
cp .env.example .env                        # then fill in keys
cp frontend/.env.example frontend/.env.local
cd frontend && npm install

# backend (from /backend)
cd backend && ../venv/Scripts/python -m uvicorn app.main:app --reload
../venv/Scripts/python -m pytest

# frontend (from /frontend)
npm run dev

# data
venv/Scripts/python ml/ingest/download_nhanes.py
venv/Scripts/python ml/ingest/download_medlineplus.py
```

## Keys (see `.env.example`)

| Variable | Where to get it |
|---|---|
| `SUPABASE_*`, `DATABASE_URL` | Supabase dashboard > Project Settings > API / Database |
| `LLM_API_KEY` | console.groq.com > API Keys |
| `GEMINI_API_KEY` (optional) | aistudio.google.com > Get API key |
| `USDA_FDC_API_KEY` | fdc.nal.usda.gov/api-key-signup |
| `OPENFDA_API_KEY` | open.fda.gov/apis/authentication |
| `NCBI_API_KEY`, `NCBI_EMAIL` | ncbi.nlm.nih.gov > Account settings > API Key |

Frontend variables (`NEXT_PUBLIC_*`) live only in `frontend/.env.local`. Never put the
service-role key, JWT secret, database URL or LLM keys there.

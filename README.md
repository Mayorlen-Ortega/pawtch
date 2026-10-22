# Pawtch

Pawtch is a local proof of concept for lost and found pets in Coquimbo, Chile. People can create lost or found pet reports, then review explainable possible matches surfaced by the system.

The project is intentionally a small local demo, not a production service. It uses Angular and TypeScript for the browser experience and a small FastAPI service for local persistence and matching.

## What The Demo Shows

1. Open the app and choose `I lost a pet`.
2. Create a report with a photo, species, color, markings, a curated location, and date. Optional details can be added for lost reports.
3. Choose `I found a pet` and create a second report with its own observed details.
4. The found report is compared with existing lost reports.
5. Open the lost report detail page and review the `Possible match` card.
6. Select `Compare reports` to inspect both reports, their photos, and the evidence side by side.

The result is always described as a possible match, not a confirmation or probability.

## Prerequisites

- Node.js compatible with Angular CLI 21. This project was created and verified with Node 24.14.0 and Angular CLI 21.2.24.
- Python 3.14 or another version supported by the installed PyTorch wheel.
- Git.

The first matching request downloads the public `openai/clip-vit-base-patch32` model from Hugging Face. The model is cached locally and is not stored in this repository. The first request may take longer than later requests.

## Run Locally

Open two PowerShell terminals from the repository root.

### FastAPI backend

```powershell
Set-Location backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

The API runs at `http://localhost:8000` and its interactive documentation is at `http://localhost:8000/docs`.

### Angular frontend

```powershell
Set-Location frontend
npm install
npm start -- --port 4200
```

Open `http://localhost:4200`.

For a production build:

```powershell
Set-Location frontend
npm run build
```

## How Matching Works

When a found report is created, the backend compares it with existing lost reports using four visible signals:

- **Visual similarity:** a local CLIP model converts each photo into an embedding, then the backend compares the embeddings. This is a visual similarity signal, not a probability that the animals are the same.
- **Physical characteristics:** species, color, markings, descriptions, and available size information contribute a transparent score.
- **Geographic proximity:** curated Coquimbo sectors and communes have fixed coordinates, so nearby locations can be compared without a maps or geocoding service.
- **Date compatibility:** a found date before the lost date is incompatible. Later dates receive decreasing support based on the time gap.

The starting policy combines the signals as follows:

```text
visual similarity:       40%
physical characteristics: 30%
geographic proximity:     15%
date compatibility:       15%
```

The configured threshold is `55.0`, defined in `backend/app/config.py`. It is an adjustable POC policy, not a calibrated confidence score. A possible match also requires compatible dates and non-zero physical evidence.

The interface shows the individual scores and plain-language explanations so a person can decide for themselves.

## Local Data And Privacy

Reports and uploaded images are stored locally under `backend/data/` for this demo:

- `reports.json` stores report data.
- `matches.json` stores calculated match explanations.
- `images/` stores uploaded photos.

Reports can be marked resolved, which keeps their details and photos but excludes them from possible matches. Permanent deletion is a separate confirmed action that removes the report, its photo, and related matches. Since the POC has no accounts, anyone with access to the local app can use these actions; this is not an authorization model for a public deployment.

These runtime files are ignored by Git. The repository also ignores the Python virtual environment, Angular dependencies and build output, Python bytecode, model caches, `.env` files, and the personal `devpost/learner-profile.md` file. A secret-free `.env.example` remains allowed.

Do not add real personal reports or private pet photos to Git. Before publishing, inspect `git status` and the staged file list.

## Project Layout

```text
frontend/       Angular application and responsive UI
backend/app/    FastAPI routes, storage, embeddings, and matching
backend/tests/  Focused matching policy tests
backend/data/   Local runtime data, ignored by Git
devpost/        Approved scope, PRD, spec, and build checklist
```

## Verification

Backend matching tests:

```powershell
Set-Location backend
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Frontend build:

```powershell
Set-Location frontend
npm run build
```

The backend tests cover matching policy, report lifecycle behavior, and safe image/match cleanup using temporary test data.

## Intentionally Outside The POC

This project does not include accounts, production notifications, contact workflows, report-resolution follow-ups, native mobile apps, deployment, a dashboard, a chatbot, or production-scale infrastructure. Ollama is also not required because deterministic image and contextual evidence is more useful for this demonstration.

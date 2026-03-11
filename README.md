# Expert Enigma

AI-powered going-out assistant. Tell it what you're planning — pool, dinner, drinks — and it finds real places in your city, checks the weather, and tells you what to wear.

## What it does

- Searches the web for real venues (restaurants, bars, pool halls, clubs) in your city
- Fetches live weather to tailor place and outfit suggestions
- Suggests 3–5 options with a reason for each
- Recommends a specific outfit that works for the weather and venues
- Multi-turn chat — say "I don't like that one" and it finds alternatives
- Click any place card in the UI to ask the agent for more details

## Tech stack

**Backend** — Python, FastAPI, Clean Architecture, Anthropic SDK (Claude), Open-Meteo (weather), DuckDuckGo + BeautifulSoup (scraping), JSON file persistence

**Frontend** — React, Vite, TypeScript, Tailwind CSS

## Prerequisites

- Python 3.11+
- Node.js 18+
- A Claude API key from [console.anthropic.com](https://console.anthropic.com)

## Setup

### 1. Clone and configure environment

```bash
cd expert-enigma
cp .env.example .env
```

Edit `.env` and add your Claude API key:

```
CLAUDE_API_KEY=sk-ant-...
```

### 2. Backend

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Frontend

```bash
cd frontend
npm install
```

## Running

Open **two terminals**.

**Terminal 1 — Backend** (from `expert-enigma/`):

```bash
source venv/bin/activate
uvicorn app.main:app --reload
```

Runs at `http://localhost:8000`. Swagger docs at `http://localhost:8000/docs`.

**Terminal 2 — Frontend** (from `expert-enigma/frontend/`):

```bash
npm run dev
```

Runs at `http://localhost:5173`. Open this in your browser.

## First use

1. Open `http://localhost:5173`
2. Fill in the profile form (name, city, style preferences, budget)
3. Start chatting — example:

> *"I want to play pool at 19:00 in Chisinau for an hour, then go to a nice restaurant for dinner. Help me plan the evening."*

The agent will search for real places, check the weather, and come back with recommendations + outfit suggestion. Expect **30–60 seconds** on first response — it's doing multiple web searches.

## Example follow-ups

- *"I don't like the first restaurant, show me something else"*
- *"What's the dress code at [place name]?"*
- *"What if it rains?"*
- Click any place card → **"Ask for more details"** button appears

## API endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/chat` | Main conversational endpoint |
| `POST` | `/api/v1/profile` | Create user profile |
| `GET` | `/api/v1/profile/{user_id}` | Get user profile |
| `PATCH` | `/api/v1/profile/{user_id}` | Update profile |
| `GET` | `/api/v1/weather/{city}` | Test weather for a city |
| `GET` | `/api/v1/health` | Health check |

## Project structure

```
expert-enigma/
├── app/
│   ├── domain/          # Entities, service interfaces, exceptions (no dependencies)
│   ├── application/     # Use cases (orchestration logic)
│   ├── infrastructure/  # Claude agent, Open-Meteo, web scraper, JSON repositories
│   └── api/             # FastAPI routes, schemas, DI wiring
├── frontend/            # React + Vite frontend
├── data/                # JSON storage (gitignored, auto-created)
├── .env.example
└── requirements.txt
```

## Running tests

```bash
source venv/bin/activate
pytest
```

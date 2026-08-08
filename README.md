# Python Engine Flappy Bird

A Flappy Bird architecture experiment that separates authoritative game simulation from browser presentation.

Python owns the game loop, physics, pipe simulation, collision, scoring, and game state. A lightweight FastAPI WebSocket layer streams authoritative snapshots to a TypeScript and HTML5 Canvas frontend, which handles only rendering and player input.

The project explores engine architecture, real-time client/server communication, state ownership, and separation of game logic from presentation rather than attempting to build a production-grade general-purpose game engine.

## Architecture

```text
TypeScript + HTML5 Canvas
    Presentation / Input
            |
            | START / FLAP / RESTART
            v
        WebSocket
            |
            v
         FastAPI
     Transport Layer
            |
            v
       GameManager
   Authoritative State
            |
       +----+----+
       v         v
   Game Logic   Lightweight
   |- Bird      Engine Layer
   |- Pipes     |- Clock
   |- Scoring   |- GameLoop
   '- Collision '- Physics
            |
            v
     State Snapshot
            |
            v
       WebSocket
            |
            v
    Canvas Renderer
```

Responsibilities:

- `frontend/`
  - canvas rendering
  - local image assets
  - input capture
  - snapshot display
- `server/`
  - websocket transport
  - health endpoint
  - snapshot delivery
- `game/`
  - Bird rules
  - pipe spawning and movement
  - collision
  - scoring
  - restart/game-over orchestration
- `engine/`
  - generic clock
  - game loop
  - vector/body/gravity primitives

## Local Setup

Clone the repository and work from the repository root:

```bash
git clone git@github.com:kyawhtetyang/python-engine-flappy-bird.git
cd python-engine-flappy-bird
```

### Python

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
```

### Frontend

From the repository root:

```bash
cd frontend
npm install
```

## Run

### Backend

```bash
source .venv/bin/activate
python -m uvicorn server.main:app --host 127.0.0.1 --port 8000
```

### Frontend

From the repository root:

```bash
cd frontend
npm run dev -- --host 127.0.0.1 --port 3000
```

Open:

- `http://127.0.0.1:3000`

## Controls

- `START` button: begin the simulation
- `FLAP` button: apply upward impulse
- `RESTART` button: reset the game state
- `Space`: flap
- canvas click: flap

## Current Capabilities

- authoritative Python Bird physics
- authoritative Python pipe spawning and movement
- authoritative collision with ground and pipes
- authoritative single-pass scoring
- authoritative `GAME_OVER`
- authoritative `RESTART`
- local frontend rendering with copied local Flappy Bird assets
- Python test suite and frontend build verified

## Current Non-Goals

- no deployment
- no multiplayer
- no audio system
- no AI features
- no visual polish pass

## Verify

### Python tests

```bash
source .venv/bin/activate
python -m pytest tests
```

### Frontend build

From the repository root:

```bash
cd frontend
npm run build
```

### Health check

```bash
curl http://127.0.0.1:8000/health
```

## Assets

Presentation assets are stored locally in:

- `frontend/assets/images/`

Attribution is recorded in:

- `frontend/assets/images/ATTRIBUTION.md`

These assets are local copies only.
There is no runtime dependency on external asset-hosting repositories or GitHub raw URLs.

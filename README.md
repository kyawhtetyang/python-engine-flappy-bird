# Python Flappy Bird v0

Runnable localhost Flappy Bird architecture experiment:

- Python owns authoritative game state, simulation, physics, collision, and scoring
- TypeScript owns browser rendering and input only
- FastAPI + WebSocket connect the browser client to the Python simulation

## Architecture

```text
TypeScript Frontend :3000
        ↕ WebSocket
FastAPI Server :8000
        ↓
GameManager
        ↓
Flappy Bird Game
        ↓
Generic Python Engine
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

### Python

```bash
cd ~/execution/09_Game/03_Python_Flappy_Bird/v0
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
```

### Frontend

```bash
cd ~/execution/09_Game/03_Python_Flappy_Bird/v0/frontend
npm install
```

## Run

### Backend

```bash
cd ~/execution/09_Game/03_Python_Flappy_Bird/v0
source .venv/bin/activate
python -m uvicorn server.main:app --host 127.0.0.1 --port 8000
```

### Frontend

```bash
cd ~/execution/09_Game/03_Python_Flappy_Bird/v0/frontend
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

## Current v0 Capabilities

- authoritative Python Bird physics
- authoritative Python pipe spawning and movement
- authoritative collision with ground and pipes
- authoritative single-pass scoring
- authoritative `GAME_OVER`
- authoritative `RESTART`
- local frontend rendering with copied local Flappy Bird assets
- Python test suite and frontend build verified

## Current v0 Non-Goals

- no deployment
- no multiplayer
- no audio system
- no AI features
- no visual polish pass

## Verify

### Python tests

```bash
cd ~/execution/09_Game/03_Python_Flappy_Bird/v0
source .venv/bin/activate
python -m pytest tests
```

### Frontend build

```bash
cd ~/execution/09_Game/03_Python_Flappy_Bird/v0/frontend
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
There is no runtime dependency on `02_Web_Flappy_Bird` or GitHub raw URLs.

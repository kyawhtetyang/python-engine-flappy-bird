from copy import deepcopy
from typing import Literal, TypedDict

from game.config.game_config import (
    BIRD_HEIGHT,
    BIRD_WIDTH,
    FLAP_STRENGTH,
    GAME_HEIGHT,
    GAME_WIDTH,
    GRAVITY,
    GROUND_HEIGHT,
    INITIAL_BIRD_X,
    INITIAL_BIRD_Y,
    PIPE_GAP_SIZE,
    PIPE_SPEED,
    PIPE_SPAWN_INTERVAL,
    PIPE_VERTICAL_MARGIN,
    PIPE_WIDTH,
)
from game.core.collision import CollisionSystem
from game.pipes.pipe import PipePair
from game.pipes.pipe_mover import PipeMover
from game.pipes.pipe_spawner import PipeSpawner
from game.player.bird_controller import BirdController
from game.scoring.score_system import ScoreSystem


GameStatus = Literal["START", "PLAYING", "GAME_OVER"]
ClientAction = Literal["START", "FLAP", "RESTART"]


class BirdState(TypedDict):
    x: float
    y: float
    velocityY: float


class PipeState(TypedDict):
    id: int
    x: float
    gapY: float
    gapSize: float
    width: float


class GameState(TypedDict):
    type: Literal["STATE"]
    status: GameStatus
    score: int
    bird: BirdState
    pipes: list[PipeState]


class GameManager:
    def __init__(self) -> None:
        self._bird = BirdController(
            initial_x=INITIAL_BIRD_X,
            initial_y=INITIAL_BIRD_Y,
            gravity_strength=GRAVITY,
            flap_strength=FLAP_STRENGTH,
        )
        self._pipe_spawner = PipeSpawner(
            game_width=GAME_WIDTH,
            game_height=GAME_HEIGHT,
            ground_height=GROUND_HEIGHT,
            pipe_width=PIPE_WIDTH,
            gap_size=PIPE_GAP_SIZE,
            spawn_interval=PIPE_SPAWN_INTERVAL,
            vertical_margin=PIPE_VERTICAL_MARGIN,
        )
        self._pipe_mover = PipeMover(speed=PIPE_SPEED)
        self._collision_system = CollisionSystem(
            game_height=GAME_HEIGHT,
            ground_height=GROUND_HEIGHT,
            bird_width=BIRD_WIDTH,
            bird_height=BIRD_HEIGHT,
        )
        self._score_system = ScoreSystem()
        self._pipes: list[PipePair] = []
        self._initial_state: GameState = {
            "type": "STATE",
            "status": "START",
            "score": 0,
            "bird": self._bird.snapshot(),
            "pipes": [],
        }
        self._state: GameState = deepcopy(self._initial_state)

    def snapshot(self) -> GameState:
        self._sync_bird_state()
        return deepcopy(self._state)

    def handle_action(self, action_type: ClientAction) -> GameState:
        if action_type == "START":
            self._handle_start()
        elif action_type == "FLAP":
            self._handle_flap()
        elif action_type == "RESTART":
            self._reset()

        return self.snapshot()

    def update(self, dt: float) -> GameState:
        if self._state["status"] == "PLAYING":
            self._bird.update(dt)
            if self._bird.body.position.y < 0:
                self._bird.body.position.y = 0
                self._bird.body.velocity.y = 0
            self._pipes.extend(self._pipe_spawner.update(dt))
            self._pipe_mover.update(self._pipes, dt)
            self._state["score"] = self._score_system.update(
                self._pipes,
                self._bird.body.position.x,
                self._state["score"],
            )
            if self._collision_system.has_collision(
                bird_x=self._bird.body.position.x,
                bird_y=self._bird.body.position.y,
                pipes=self._pipes,
            ):
                self._state["status"] = "GAME_OVER"
            self._pipes = [pipe for pipe in self._pipes if pipe.x + pipe.width > 0]
            self._sync_bird_state()
            self._sync_pipe_state()
        return self.snapshot()

    def _handle_start(self) -> None:
        if self._state["status"] == "START":
            self._state["status"] = "PLAYING"
            self._sync_bird_state()

    def _handle_flap(self) -> None:
        if self._state["status"] == "PLAYING":
            self._bird.flap()
            self._sync_bird_state()

    def _reset(self) -> None:
        self._bird.reset()
        self._pipes = []
        self._pipe_spawner.reset()
        self._state = deepcopy(self._initial_state)
        self._sync_bird_state()
        self._sync_pipe_state()

    def _sync_bird_state(self) -> None:
        self._state["bird"] = self._bird.snapshot()

    def _sync_pipe_state(self) -> None:
        self._state["pipes"] = [pipe.snapshot() for pipe in self._pipes]

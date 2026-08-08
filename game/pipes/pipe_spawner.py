import random

from game.pipes.pipe import PipePair


class PipeSpawner:
    def __init__(
        self,
        *,
        game_width: float,
        game_height: float,
        ground_height: float,
        pipe_width: float,
        gap_size: float,
        spawn_interval: float,
        vertical_margin: float,
    ) -> None:
        self.game_width = game_width
        self.game_height = game_height
        self.ground_height = ground_height
        self.pipe_width = pipe_width
        self.gap_size = gap_size
        self.spawn_interval = spawn_interval
        self.vertical_margin = vertical_margin
        self._elapsed = 0.0
        self._next_pipe_id = 1

    def reset(self) -> None:
        self._elapsed = 0.0

    def update(self, dt: float) -> list[PipePair]:
        self._elapsed += dt
        spawned: list[PipePair] = []

        while self._elapsed >= self.spawn_interval:
            self._elapsed -= self.spawn_interval
            spawned.append(self._spawn_pipe())

        return spawned

    def _spawn_pipe(self) -> PipePair:
        playable_height = self.game_height - self.ground_height
        min_gap_y = self.vertical_margin
        max_gap_y = playable_height - self.vertical_margin - self.gap_size
        gap_y = random.uniform(min_gap_y, max_gap_y)

        pipe = PipePair(
            id=self._next_pipe_id,
            x=self.game_width + self.pipe_width,
            gap_y=gap_y,
            gap_size=self.gap_size,
            width=self.pipe_width,
        )
        self._next_pipe_id += 1
        return pipe

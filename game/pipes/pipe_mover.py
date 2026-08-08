from game.pipes.pipe import PipePair


class PipeMover:
    def __init__(self, speed: float) -> None:
        self.speed = speed

    def update(self, pipes: list[PipePair], dt: float) -> None:
        for pipe in pipes:
            pipe.x -= self.speed * dt

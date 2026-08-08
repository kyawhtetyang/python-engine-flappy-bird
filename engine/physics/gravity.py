from engine.physics.body import Body


class Gravity:
    def __init__(self, acceleration_y: float) -> None:
        self.acceleration_y = acceleration_y

    def apply(self, body: Body, dt: float) -> None:
        body.velocity.y += self.acceleration_y * dt

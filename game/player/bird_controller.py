from engine.math.vector2 import Vector2
from engine.physics.body import Body
from engine.physics.gravity import Gravity


class BirdController:
    def __init__(
        self,
        initial_x: float,
        initial_y: float,
        gravity_strength: float,
        flap_strength: float,
    ) -> None:
        self.initial_x = initial_x
        self.initial_y = initial_y
        self.flap_strength = flap_strength
        self.gravity = Gravity(gravity_strength)
        self.body = Body(position=Vector2(initial_x, initial_y), velocity=Vector2())

    def reset(self) -> None:
        self.body.position.x = self.initial_x
        self.body.position.y = self.initial_y
        self.body.velocity.x = 0.0
        self.body.velocity.y = 0.0

    def flap(self) -> None:
        self.body.velocity.y = self.flap_strength

    def update(self, dt: float) -> None:
        self.gravity.apply(self.body, dt)
        self.body.integrate(dt)

    def snapshot(self) -> dict[str, float]:
        return {
            "x": round(self.body.position.x, 2),
            "y": round(self.body.position.y, 2),
            "velocityY": round(self.body.velocity.y, 2),
        }

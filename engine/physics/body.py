from dataclasses import dataclass, field

from engine.math.vector2 import Vector2


@dataclass
class Body:
    position: Vector2 = field(default_factory=Vector2)
    velocity: Vector2 = field(default_factory=Vector2)

    def integrate(self, dt: float) -> None:
        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt

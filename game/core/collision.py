from game.pipes.pipe import PipePair


class CollisionSystem:
    def __init__(
        self,
        *,
        game_height: float,
        ground_height: float,
        bird_width: float,
        bird_height: float,
    ) -> None:
        self.game_height = game_height
        self.ground_height = ground_height
        self.bird_width = bird_width
        self.bird_height = bird_height

    def has_collision(self, *, bird_x: float, bird_y: float, pipes: list[PipePair]) -> bool:
        ground_y = self.game_height - self.ground_height
        bird_left = bird_x
        bird_right = bird_x + self.bird_width
        bird_top = max(0.0, bird_y)
        bird_bottom = bird_y + self.bird_height

        if bird_bottom >= ground_y:
            return True

        for pipe in pipes:
            pipe_left = pipe.x
            pipe_right = pipe.x + pipe.width
            if bird_right > pipe_left and bird_left < pipe_right:
                gap_top = pipe.gap_y
                gap_bottom = pipe.gap_y + pipe.gap_size
                if bird_top < gap_top or bird_bottom > gap_bottom:
                    return True

        return False

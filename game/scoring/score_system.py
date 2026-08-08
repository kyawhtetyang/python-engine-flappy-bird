from game.pipes.pipe import PipePair


class ScoreSystem:
    def update(self, pipes: list[PipePair], bird_x: float, score: int) -> int:
        updated_score = score
        for pipe in pipes:
            pipe_right = pipe.x + pipe.width
            if not pipe.passed and bird_x > pipe_right:
                pipe.passed = True
                updated_score += 1
        return updated_score

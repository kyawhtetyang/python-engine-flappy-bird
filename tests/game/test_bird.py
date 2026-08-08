from game.core.game_manager import GameManager
from game.pipes.pipe import PipePair


def test_bird_hits_ground_and_enters_game_over() -> None:
    manager = GameManager()
    manager.handle_action("START")
    manager._bird.body.position.y = 690.0  # type: ignore[attr-defined]

    snapshot = manager.update(0.0)

    assert snapshot["status"] == "GAME_OVER"


def test_bird_hits_pipe_and_enters_game_over() -> None:
    manager = GameManager()
    manager.handle_action("START")
    manager._pipes = [PipePair(id=1, x=100.0, gap_y=350.0, gap_size=120.0, width=52.0)]  # type: ignore[attr-defined]
    manager._bird.body.position.y = 200.0  # type: ignore[attr-defined]

    snapshot = manager.update(0.0)

    assert snapshot["status"] == "GAME_OVER"

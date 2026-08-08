from game.core.game_manager import GameManager
from game.pipes.pipe import PipePair


def test_score_increments_once_when_pipe_is_passed() -> None:
    manager = GameManager()
    manager.handle_action("START")
    manager._pipes = [PipePair(id=1, x=10.0, gap_y=200.0, gap_size=150.0, width=52.0)]  # type: ignore[attr-defined]

    snapshot = manager.update(0.0)
    snapshot_again = manager.update(0.0)

    assert snapshot["score"] == 1
    assert snapshot_again["score"] == 1


def test_restart_resets_score_and_pipes() -> None:
    manager = GameManager()
    manager.handle_action("START")
    manager._state["score"] = 3  # type: ignore[index]
    manager._pipes = [PipePair(id=1, x=10.0, gap_y=200.0, gap_size=150.0, width=52.0)]  # type: ignore[attr-defined]

    snapshot = manager.handle_action("RESTART")

    assert snapshot["status"] == "START"
    assert snapshot["score"] == 0
    assert snapshot["pipes"] == []

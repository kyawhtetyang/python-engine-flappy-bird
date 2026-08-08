from dataclasses import dataclass


@dataclass
class PipePair:
    id: int
    x: float
    gap_y: float
    gap_size: float
    width: float
    passed: bool = False

    def snapshot(self) -> dict[str, float | int]:
        return {
            "id": self.id,
            "x": round(self.x, 2),
            "gapY": round(self.gap_y, 2),
            "gapSize": round(self.gap_size, 2),
            "width": round(self.width, 2),
        }

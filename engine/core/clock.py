import asyncio


class Clock:
    def __init__(self, tick_rate: float) -> None:
        self.tick_rate = tick_rate
        self.fixed_dt = 1.0 / tick_rate

    async def wait_for_next_tick(self) -> float:
        await asyncio.sleep(self.fixed_dt)
        return self.fixed_dt

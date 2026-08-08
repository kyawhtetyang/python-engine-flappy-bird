from collections.abc import Awaitable, Callable

from engine.core.clock import Clock


class GameLoop:
    def __init__(self, clock: Clock) -> None:
        self.clock = clock

    async def run(self, update: Callable[[float], Awaitable[None]]) -> None:
        while True:
            dt = await self.clock.wait_for_next_tick()
            await update(dt)

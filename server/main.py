import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from engine.core.clock import Clock
from engine.core.game_loop import GameLoop
from game.config.game_config import TICK_RATE
from game.core.game_manager import GameManager
from server.protocol.messages import parse_client_message
from server.protocol.serializer import snapshot_payload

app = FastAPI(title="Python Flappy Bird")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    manager = GameManager()
    lock = asyncio.Lock()
    loop = GameLoop(Clock(TICK_RATE))
    last_streamed_status = manager.snapshot()["status"]

    async def stream_snapshots() -> None:
        nonlocal last_streamed_status

        async def tick(dt: float) -> None:
            nonlocal last_streamed_status
            async with lock:
                snapshot = manager.update(dt)
            should_send = snapshot["status"] == "PLAYING" or (
                last_streamed_status == "PLAYING" and snapshot["status"] == "GAME_OVER"
            )
            last_streamed_status = snapshot["status"]
            if should_send:
                await websocket.send_json(snapshot_payload(snapshot))

        await loop.run(tick)

    await websocket.accept()
    await websocket.send_json(snapshot_payload(manager.snapshot()))
    stream_task = asyncio.create_task(stream_snapshots())

    try:
        while True:
            raw_message = await websocket.receive_json()
            message = parse_client_message(raw_message)
            async with lock:
                updated_snapshot = manager.handle_action(message["type"])
            last_streamed_status = updated_snapshot["status"]
            await websocket.send_json(snapshot_payload(updated_snapshot))
    except WebSocketDisconnect:
        return
    finally:
        stream_task.cancel()
        try:
            await stream_task
        except asyncio.CancelledError:
            pass

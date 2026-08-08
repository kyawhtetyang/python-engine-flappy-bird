from typing import Literal, TypedDict, cast

from game.core.game_manager import ClientAction


class ClientMessage(TypedDict):
    type: ClientAction


def parse_client_message(raw_message: dict) -> ClientMessage:
    message_type = raw_message.get("type")
    allowed_types: tuple[ClientAction, ...] = ("START", "FLAP", "RESTART")

    if message_type not in allowed_types:
        raise ValueError(f"Unsupported message type: {message_type}")

    return {"type": cast(ClientAction, message_type)}

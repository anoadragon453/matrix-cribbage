import logging
from nio import (
    SendRetryError
)

logger = logging.getLogger(__name__)


async def send_text_to_room(client, room_id, message):
    """Send text to a matrix room"""
    try:
        await client.room_send(
            room_id,
            "m.room.message",
            {
                "msgtype": "m.text",
                "body": message,
            }
        )
    except SendRetryError:
        logger.exception(f"Unable to send message response to {room_id}")

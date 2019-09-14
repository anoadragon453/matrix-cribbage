from chat_functions import (
    send_text_to_room,
)
from bot_commands import process_command
from nio import (
    JoinError,
)

import logging
logger = logging.getLogger(__name__)


class Callbacks(object):

    def __init__(self, client, command_prefix):
        """
        Args:
            client (nio.AsyncClient): nio client used to interact with matrix

            command_prefix (str): The prefix for bot commands
        """
        self.client = client
        self.command_prefix = command_prefix

    async def message(self, room, event):
        """Callback for when a message event is received

        Args:
            room (nio.rooms.MatrixRoom): The room the event came from

            event (nio.events.room_events.RoomMessageText): The event defining the message

        """
        # Extract the message text
        msg = event.body

        # Ignore messages from ourself
        if event.sender == self.client.user_id:
            return

        logger.debug(
            f"Bot message received for room {room.display_name} | "
            f"{room.user_name(event.sender)}: {msg}"
        )

        # Ignore message if in a public room without command prefix
        has_command_prefix = msg.startswith(self.command_prefix)
        if not has_command_prefix and not room.is_group:
            return

        if has_command_prefix:
            # Remove the command prefix
            msg = msg[len(self.command_prefix):]

        await process_command(self.client, msg, room, event)

    async def invite(self, room, event):
        """Callback for when an invite is received. Join the room specified in the invite"""
        logger.debug(f"Got invite to {room.room_id} from {event.sender}.")

        # Attempt to join 3 times before giving up
        for attempt in range(3):
            result = await self.client.join(room.room_id)
            if type(result) == JoinError:
                logger.error(
                    f"Error joining room {room.room_id} (attempt %d): %s",
                    attempt, result.message,
                )
            else:
                logger.info(f"Joined {room.room_id}")
                break


#!/usr/bin/env python3

import asyncio
from nio import (
    AsyncClient,
    RoomMessageText,
    InviteEvent,
    SendRetryError,
)

client = None
command_prefix = "!c"


async def send_text_to_room(room_id, message):
    """Send text to a matrix room"""
    await client.room_send(
        room_id,
        "m.room.message",
        {
            "msgtype": "m.text",
            "body": message,
        }
    )


async def message_cb(room, event):
    """Callback for when a message event is received"""
    # Ignore messages not meant for us
    if not event.body.startswith(command_prefix):
        return

    msg = event.body[len(command_prefix):]

    print(
        f"Bot message received for room {room.display_name} | "
        f"{room.user_name(event.sender)}: {msg}"
    )

    try:
        # Send a response to the room
        await send_text_to_room(room.room_id, f"Received command: {msg}")
    except SendRetryError:
        print(f"Unable to send message response to {room.room_id}")


async def invite_cb(room, event):
    """Callback for when an invite is received. Join the room specified in the invite"""
    print(f"Got invite to {room.room_id} from {event.sender}.")
    await client.join(room.room_id)
    print(f"Joined {room.room_id}")


async def main():
    global client
    global command_prefix

    command_prefix += " "

    client = AsyncClient("http://localhost:8008", "@cribbagebot:localhost")

    # Set up event callbacks
    client.add_event_callback(message_cb, RoomMessageText)
    client.add_event_callback(invite_cb, InviteEvent)

    await client.login("thisisstupid123")
    print("Logged in")

    await client.sync_forever(timeout=30000)

asyncio.get_event_loop().run_until_complete(main())


#!/usr/bin/env python3

import logging
import asyncio
from nio import (
    AsyncClient,
    RoomMessageText,
    InviteEvent,
)
from callbacks import Callbacks

logger = logging.getLogger(__name__)

client = None
command_prefix = "!c"


async def main():
    global client
    global command_prefix

    # TODO: Move to config file
    logger.setLevel(logging.DEBUG)

    command_prefix += " "

    client = AsyncClient("http://localhost:8008", "@cribbagebot:localhost")
    callbacks = Callbacks(client, command_prefix)

    # Set up event callbacks
    client.add_event_callback(callbacks.message, (RoomMessageText,))
    client.add_event_callback(callbacks.invite, (InviteEvent,))

    await client.login("thisisstupid123")
    logger.info("Logged in")

    await client.sync_forever(timeout=30000)

asyncio.get_event_loop().run_until_complete(main())


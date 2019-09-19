#!/usr/bin/env python3

import logging
import asyncio
from nio import (
    AsyncClient,
    RoomMessageText,
    InviteEvent,
)
from callbacks import Callbacks
from config import Config
from storage import Storage

logger = logging.getLogger(__name__)


async def main():
    # Read config file
    config = Config("config.yaml")

    # Configure the database
    store = Storage(config.database_filepath)

    # Initialize the matrix client
    client = AsyncClient(config.homeserver_url, config.user_id, device_id=config.device_id)

    # Assign an access token to the bot instead of logging in and creating a new device
    client.access_token = config.access_token

    logger.info("Logged in")

    # Set up event callbacks
    callbacks = Callbacks(client, store, config.command_prefix)
    client.add_event_callback(callbacks.message, (RoomMessageText,))
    client.add_event_callback(callbacks.invite, (InviteEvent,))

    await client.sync_forever(timeout=30000)

asyncio.get_event_loop().run_until_complete(main())

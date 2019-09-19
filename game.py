# Game functions

import logging
from chat_functions import send_text_to_room

logger = logging.getLogger(__name__)


class Game(object):

    def __init__(self, client, room, starter):
        """
        Args:
            client (nio.AsyncClient): nio client used to interact with matrix

            room (nio.rooms.MatrixRoom): The room the game runs in

            starter (str): User ID of the user who initiated the game
        """
        self.client = client
        self.room = room

        # Player User IDs
        # The first player in the list manages the game
        self.players = [starter]

        # Whether a game has been proposed but not yet started
        self.game_proposed = False

    async def start_game(self, user_id):
        """Start a new game

        Args:
            user_id (str): User ID of the user who initiated the game
        """
        text = f"""
{self.players[0]} has proposed to start a game! Players who wish to join should use the `join`
command. The game manager (that's {self.players[0]}) can use the `ready` command when either
two or four players have joined in total, or they can use the `cancel` command to cancel
starting the game.
"""
        self.game_proposed = True
        await send_text_to_room(self.client, self.room.room_id, text)

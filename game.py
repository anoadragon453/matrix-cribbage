# Game functions

import logging

logger = logging.getLogger(__name__)


class Game(object):

    def __init__(self, client):
        """
        Args:
            client (nio.AsyncClient): nio client used to interact with matrix
        """
        self.client = client

    def start_game(self, room):
        """Start a new game

        Args:
            room (nio.rooms.MatrixRoom): The room to start the game in
        """

import sqlite3
import os.path

latest_db_version = 0


class Storage(object):
    def __init__(self, db_path):
        """
        Args:
            db_path (str): The name of the database file
        """
        self.db_path = db_path

    def setup(self):
        """Setup the database on first run.

        Runs an initial setup or migrations depending on whether a database file has already
        been created
        """
        # Initialize a connection to the database
        conn = sqlite3.connect(self.db_path)
        self.cursor = conn.cursor()

        # Check if a database has already been connected
        if os.path.isfile(self.db_path):
            self._run_migrations()
        else:
            self._initial_setup()

    def _initial_setup(self):
        """Initial setup of the database"""
        # Games table
        self.cursor.execute("CREATE TABLE games ("
                            "room_id TEXT PRIMARY KEY,"
                            "data TEXT NOT NULL"
                            ")")

    def _run_migrations(self):
        """Execute database migrations"""
        pass

    def game_exists(self, room_id):
        """Check if a game exists for a room

        Args:
            room_id (str): The ID of the room to check
        Returns:
            True or False based on whether a game exists in the room
        """
        self.cursor.execute("SELECT room_id FROM games WHERE room_id = ?", (room_id,))
        rows = self.cursor.fetchone()

        return True if rows else False

    def save_game(self, game):
        """Save a game object to the database

        Args:
            game (Game): The game to save
        """
        # TODO: Pickle the game object
        # TODO: Save the game to the db
        pass

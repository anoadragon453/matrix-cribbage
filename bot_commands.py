from chat_functions import send_text_to_room
from game import Game


class Command(object):
    def __init__(self, client, store, command, room, event):
        """A command made by a user

        Args:
            client (nio.AsyncClient): The client to communicate to matrix with

            store (Storage): Bot storage

            command (str): The command and arguments

            room (nio.rooms.MatrixRoom): The room the command was sent in

            event (nio.events.room_events.RoomMessageText): The event describing the command
        """
        self.client = client
        self.store = store
        self.command = command
        self.room = room
        self.event = event
        self.args = self.command.split()[1:]

    async def process(self):
        """Process the command"""
        if self.command.startswith("play"):
            await self._new_game()
        elif self.command.startswith("put"):
            await self._put_card()
        elif self.command.startswith("help"):
            await self._show_help()
        else:
            await self._unknown_command()

    async def _new_game(self):
        """Start a new game"""
        # Check if a game is already in progress in this room
        if self.store.game_exists(self.room.room_id):
            await send_text_to_room(
                self.client, self.room.room_id, "A game has already started in "
                                                "this room!")

        game = Game(self.client, self.room, self.event.sender)

        # Save the game object
        self.store.save_game(game)

    async def _put_card(self):
        """Put a card down on the playing board"""
        await send_text_to_room(self.client, self.room.room_id, "Not implemented: put card")

    async def _show_help(self):
        """Show the help text"""
        if not self.args:
            text = '''
Welcome to cribbage! Use `help rules` to view the rules of the game, and use `help commands` to 
view available commands.
    '''
            await send_text_to_room(self.client, self.room.room_id, text)
            return

        topic = self.args[0]
        if topic == "rules":
            text = '''
These are the rules!
            '''
        else:  # commands
            text = '''
Available commands:
    '''
        await send_text_to_room(self.client, self.room.room_id, text)

    async def _unknown_command(self):
        await send_text_to_room(
            self.client,
            self.room.room_id,
            f"Unknown command '{self.command}'. Send 'help' for available commands.",
        )

from threading import Thread

import configuration
from game.board import Board
from networking.socket_client import SocketClient


class Player(SocketClient):
    def __init__(self, arena, username, bot, game_count_limit):
        super().__init__(None)

        host, port = arena.split(':')
        self.connect(host, int(port))

        self._bot = bot
        self._game_count_limit = game_count_limit

        username = username.split('@')[0]
        self.send_json({'username': username})
        status = self.read_next_json().get("status", None)
        if status != "ok":
            raise ValueError("Connection was not successful.")

        print("PLAYER CONNECTED.")

        th = Thread(target=self._read_events, daemon=True)
        th.start()

    def _read_events(self):
        while True:
            evt = self.read_next_json()
            if evt == None:
                print("PLAYER DISCONNECTED.")
                return

            event_name = evt["event"]
            if event_name == "get_move":
                self._on_get_move(evt)

            elif event_name == "player_is_free":
                self._on_player_is_free()

            elif event_name == "lose":
                self._on_lose(evt)

            elif event_name == "win":
                self._on_win(evt)

            elif event_name == "invalid_move":
                self._on_invalid_move(evt)

            elif event_name == "starting_game":
                self._on_game_started(evt)

            else:
                raise ValueError("Unknown event %s" % evt)

    def _on_lose(self, evt):
        self._bot.on_board_result(Board.deserialize(evt["board"]), -1)

    def _on_win(self, evt):
        self._bot.on_board_result(Board.deserialize(evt["board"]), 1)

    def _on_invalid_move(self, evt):
        self._bot.on_invalid_move(Board.deserialize(evt["board"]))

    def _on_game_started(self, evt):
        self._bot.on_game_started(evt["against"])

    def _on_player_is_free(self):
        self._request_opponent()

    def _on_get_move(self, evt):
        from configuration import MOVE_TIMEOUT

        board = Board.deserialize(evt["board"])
        if configuration.PRINT_INTERMEDIATE_BOARDS:
            print(board.to_str())

        move_id = evt["id"]
        x, y = self._bot.get_move(board, MOVE_TIMEOUT)

        self.send_json({"event": "make_move", "id": move_id, "x": x, "y": y})

    def _request_opponent(self):
        if self._game_count_limit is not None:
            if self._game_count_limit <= 0:
                print("GAME LIMIT EXHAUSTED")
                self.disconnect()

            self._game_count_limit -= 1

        print("Searching opponent.")
        self.send_json({"event": "find_opponent"})

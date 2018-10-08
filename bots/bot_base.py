import configuration


class BotBase(object):

    def __init__(self):
        self._score = 0

    def get_move(self, board, timeout):
        raise NotImplementedError("must be implemented")

    def on_board_result(self, board, score):
        if configuration.PRINT_RESULT_BOARDS:
            print(board.to_str())

        self._score += max(0, score)
        result_description = "won" if score > 0 else "lost"
        print(f"\t {result_description}, total score: {self._score}")

    def on_invalid_move(self, board):
        print(f"\t INVALID MOVE / TIMEOUT DETECTED")

    def on_game_started(self, other_player):
        print(f"Game against {other_player} started.")

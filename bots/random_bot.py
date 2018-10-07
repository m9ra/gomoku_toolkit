import random

from bots.bot_base import BotBase


class RandomBot(BotBase):
    def get_move(self, board, timeout):
        # sample till free field is found

        while True:
            x = random.randint(0, board.size)
            y = random.randint(0, board.size)

            if board.get_color(x, y) == 0:
                # field is free for the move
                return x, y

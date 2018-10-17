import random

from bots.async_bot_base import AsyncBotBase


class MySearchBot(AsyncBotBase):
    def run_search(self, board):
        best_score = None

        while self.can_search:
            x = random.randint(0, board.size)
            y = random.randint(0, board.size)

            if board.get_color(x, y) == 0:
                score = self.get_score(x, y, board)
                if best_score is None or score > best_score:
                    self.report_actual_best(x, y)  # when timeout occurs, the best found solution will be used
                    best_score = score

    def get_score(self, x, y, board):
        score_acc = 0
        for direction in board.directions:
            segment = board.get_segment(x, y, direction, board.win_length)
            component = board.longest_component(segment)
            score_acc += component * component

        return score_acc



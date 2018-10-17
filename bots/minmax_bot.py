import itertools
import random
import time
from asyncio import sleep

from bots.bot_base import BotBase
from game.board import Board


class MinmaxBot(BotBase):
    def __init__(self):
        super(MinmaxBot, self).__init__()

        self._patterns = [
            (5,),
            (1, -4, 1),
            (-4, 1),
            (1, -4),

            (-2, 1, -2),
            (-1, 1, -3),
            (-3, 1, -1),

            (-2, 1, -1, 0),
            (0, -2, 1, -1),
            (-1, 1, -2, 0),
            (0, -1, 1, -2),

            (0, 4, 0),
            (0, 4, 0),

            (0, 1, 0, 3),
            (1, 0, 3, 0),
            (1, 0, 3),

            (1, -3),
            (-3, 1),

            (2, 0, 1, 0),
            (1, 0, 2, 0),
            (0, 2, 0, 1),
            (0, 1, 0, 2),

            (0, 3, 0),
            (0, 4),
            (4, 0),
            (0, -1, 1, -1, 0),
            (0, 1, -1, 1, 0),
            (0, 0, 1, -1, 1),
            (1, -1, 1, 0, 0),

            (1, -2),
            (-2, 1),

            (1, 0, 1),

            (1, -3, 1),

            (0, 2, 0),
        ]

        self._expanded_patterns = []
        for pattern in self._patterns:
            self._expanded_patterns.append(self.expand(pattern))

    def evaluate_move(self, board, move):
        board.push_move(move)
        # print(board.to_str())
        try:
            segments = list()
            for dir in Board.directions:
                segment = board.get_segment(move[0], move[1], dir, board.size)
                segment = [s * self.my_color if s else s for s in segment]
                condensed = board.condense_segment3(segment)
                if len(condensed) > 0 and (max(condensed) > 0 or min(condensed) < 0):
                    segment[board.size] = 0
                    condensed_missing = board.condense_segment3(segment)
                    segments.append((condensed, condensed_missing))

            patternClass = len(self._expanded_patterns)
            for pattern in self._expanded_patterns:
                occurence_count = 0
                for segment in segments:
                    if self.is_pattern_present(pattern, segment):
                        occurence_count += 1

                if occurence_count > 0:
                    return (patternClass, occurence_count)

                patternClass -= 1
            return 0, 0

        finally:
            board.pop_move()

    def is_pattern_present(self, pattern, target):
        segment, missing = target

        for i in range(len(segment) - len(pattern) + 1):
            is_contained = True
            was_difference = False
            for pi in range(len(pattern)):
                if segment[i + pi] != pattern[pi]:
                    is_contained = False
                    break

                if segment[i + pi] != missing[i + pi]:
                    was_difference = True

            if is_contained and was_difference:
                return True

        return False

    def expand(self, segment):
        result = []
        for s in segment:
            if s == 0 or s is None:
                result.append(0)

            elif s < 0:
                result.extend([-1] * abs(s))
            else:
                result.extend([1] * abs(s))

        return result

    def get_move(self, board, timeout):
        self.my_color = board.turn_color

        best = None
        bestValue = 0
        bestClass = 0
        for move in self.get_candidate_moves(board):
            cls, value = self.evaluate_move(board, move)

            if best is None or bestClass < cls or (bestClass == cls and bestValue < value):
                bestClass = cls
                bestValue = value
                best = move

        return best

    def get_candidate_moves(self, board):
        candidates = set()

        if len(board._moves) == 0:
            x = random.randint(0, board.size - 1)
            y = random.randint(0, board.size - 1)
            return [(x, y)]

        for move in board._moves:
            for direction in Board.directions:
                for i in [1, 2, 3]:
                    nmove = (move[0] + direction[0] * i, move[1] + direction[1] * i)
                    self._try_add(board, candidates, nmove)

                    nmove = (move[0] - direction[0] * i, move[1] - direction[1] * i)
                    self._try_add(board, candidates, nmove)

        return candidates

    def _try_add(self, board, candidates, nmove):
        if board.get_color(nmove[0], nmove[1]) == 0:
            candidates.add(nmove)

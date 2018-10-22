import itertools
import random
import time
from asyncio import sleep

from bots.bot_base import BotBase
from game.board import Board


class MinmaxBot6(BotBase):
    def __init__(self):
        super(MinmaxBot6, self).__init__()

        self._group_index = {}
        self._patterns = []
        self._composition_indexes = []

        self.group("win0",
                   (5,),
                   )

        self.group("lose1",
                   (1, -4, 1),
                   (1, -4),
                   (-2, 1, -2),
                   (-1, 1, -3),
                   )

        self.group("win1",
                   (0, 4, 0),
                   (1, 0, 3, 0, 1),
                   (3, 0, 1, 0, 3),
                   (2, 0, 2, 0, 2),
                   )

        self.group("lose2",
                   (-1, 1, -2, 0, 0, -1),
                   (-1, 0, 0, -2, 1, -1),
                   )

        self.group("defense2",
                   (0, 1, -3, 0),
                   (-2, 1, -1, 0),
                   (1, -3, 0, 0),
                   (-2, 1, -1, 0),
                   (0, -2, 1, -1),
                   )

        self.group("win2",
                   (1, 0, 1, 0, 1, 0, 1),
                   )

        self.group("1threat1",
                   (0, 4),
                   )

        self.group("2threat2",
                   (0, 3, 0),
                   )

        self.group("1threat2a",
                   (0, 0, 3),
                   (3, 0, 0),
                   )
        self.group("1threat2b",
                   (1, 0, 2, 0),
                   (0, 1, 0, 2),
                   )

        self.compose("win1", when=["1threat1", "1threat1"])
        self.compose("win2", when=["2threat2", "2threat2"])
        self.compose("win2", when=["1threat1", "2threat2"])

        self.separate(
            (1, -3, 1),

            (0, -1, 1, -1, 0),
            (-1, 1, -1, 0, 0),
            (0, 1, 0, 3),
            (1, 0, 3, 0),
            (1, 0, 3),

            (2, 0, 1, 0),
            (1, 0, 2, 0),
            (0, 2, 0, 1),
            (0, 1, 0, 2),

            (4,),
            (0, 0, 3),
            (3, 0, 0),

            (0, -1, 1, -1, 0),
            (0, 0, -1, 1, -1),
            (-1, 1, -1, 0, 0,),

            (1, -2),
            (-2, 1),

            (1, -2, 1),

            (0, 2, 0),

            (0, 1, -1, 1, 0),
            (0, 0, 1, -1, 1),
            (1, -1, 1, 0, 0),
        )

        self.group("2d3",
                   (0, 1, -2, 0),
                   (0, -1, 1, -1, 0),
                   (1, 0, -2, 0),
                   (0, 1, -3),
                   (1, -3, 0)
                   )

        self.group("2a3",
                   (0, 3, 0),
                   (0, 4),
                   (1, 0, 2, 0),
                   )

        self.group("2a3-2",
                   (0, 3, 0),
                   (0, 4),
                   (2, 0, 1, 0),
                   )

        self.compose("defense2", when=["2d3", "2d3"])
        self.compose("win2", when=["2a3", "2a3"])
        self.compose("win2", when=["2a3-2", "2a3-2"])

    def group(self, name, *examples):
        if name in self._group_index:
            raise ValueError("Cannot redefine pattern")

        expanded = set()
        for example in examples:
            expanded.add(tuple(self.expand(example)))
            expanded.add(tuple(reversed(self.expand(example))))

        self._group_index[name] = len(self._patterns)
        self._patterns.append(list(expanded))

    def separate(self, *examples):
        for example in examples:
            self.group(f"sep{len(self._patterns)}", example)

    def compose(self, target, when):
        target_index = self._group_index[target]
        criterions = {}

        for source in when:
            index = self._group_index[source]
            criterions[index] = criterions.get(index, 0) + 1
        self._composition_indexes.append((target_index, list(criterions.items())))

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

            evaluation = list()
            for group in self._patterns:
                occurence_count = 0
                for pattern in group:
                    for segment in segments:
                        if self.is_pattern_present(pattern, segment):
                            occurence_count += 1

                evaluation.append(occurence_count)

            self.transform(evaluation)
            return evaluation

        finally:
            board.pop_move()

    def transform(self, evaluation):
        for target_index, criterions in self._composition_indexes:
            succeeded = True
            for criterion_index, count in criterions:
                if evaluation[criterion_index] < count:
                    succeeded = False
                    break
            if succeeded:
                evaluation[target_index] += 1

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
        for move in self.get_candidate_moves(board):
            value = self.evaluate_move(board, move)

            if best is None or self.is_better(value, bestValue):
                bestValue = value
                best = move

        return best

    def is_better(self, vals1, vals2):
        for val1, val2 in zip(vals1, vals2):
            if val1 > val2:
                return True
            if val1 < val2:
                return False

        return False

    def get_candidate_moves(self, board):
        candidates = set()

        if len(board._moves) == 0:
            x = random.randint(4, board.size - 5)
            y = random.randint(4, board.size - 5)
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

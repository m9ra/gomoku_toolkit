import random
from copy import deepcopy

import numpy as np
import scipy as sc
from scipy import signal

from bots.bot_base import BotBase
from game.board import Board


class ConvBot(BotBase):
    def __init__(self):
        super(ConvBot, self).__init__()
        self.parameters = []

        self._filter_groups = [
            [
                self._param(3, 3), self._param(3, 3)
            ],
            [
                self._param(3, 3), self._param(3, 3)
            ],
            [
                self._param(3, 3), self._param(3, 3)
            ],
            [
                self._param(3, 3), self._param(3, 3)
            ]
        ]

        self._pooling = [self._param(15 * 15, 5), self._param(15 * 15, 5)]
        self._last_layer = self._param(10, 1)

    def clone(self):
        return deepcopy(self)

    def get_move(self, board, timeout):
        board_array = self._create_array(board)
        best_move = None
        best_value = 0
        for x, y in self.get_candidate_moves(board):
            board_array[x, y] = board.turn_color
            value = self.evaluate(board_array)
            board_array[x, y] = 0

            if best_move is None or best_value < value:
                best_move = x, y
                best_value = value

        return best_move

    def evaluate(self, board_array):
        previous_layer = [board_array] * len(self._filter_groups[0])
        for filters in self._filter_groups:
            next_layer = []
            for filter, value in zip(filters, previous_layer):
                convolved = signal.convolve2d(value, filter, boundary="wrap", mode="same")
                convolved = np.maximum(convolved, 0)
                next_layer.append(convolved)

            previous_layer = next_layer

        parts = []
        for convolved, pool in zip(previous_layer, self._pooling):
            parts.append(sc.dot(convolved.flatten(), pool))

        interm = sc.concatenate(parts)
        result = sc.dot(interm, self._last_layer)
        return result

    def get_candidate_moves(self, board):
        candidates = set()

        if len(board._moves) == 0:
            x = random.randint(4, board.size - 5)
            y = random.randint(4, board.size - 5)
            return [(x, y)]

        for move in board._moves:
            for direction in Board.directions:
                for i in [1]:
                    nmove = (move[0] + direction[0] * i, move[1] + direction[1] * i)
                    self._try_add(board, candidates, nmove)

                    nmove = (move[0] - direction[0] * i, move[1] - direction[1] * i)
                    self._try_add(board, candidates, nmove)

        return candidates

    def _create_array(self, board):
        array = np.zeros((15, 15))
        color = -1
        for mv in board._moves:
            array[mv[0]][mv[1]] = color
            color = color * -1

        return array

    def _try_add(self, board, candidates, nmove):
        if board.get_color(nmove[0], nmove[1]) == 0:
            candidates.add(nmove)

    def _param(self, w, h):
        p = np.random.rand(w, h)
        self.parameters.append(p)
        return p

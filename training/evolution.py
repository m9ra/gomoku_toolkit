import random

import numpy as np

from configuration import BOARD_SIZE, WIN_LENGTH
from game.board import Board


class Trainer(object):
    def __init__(self, bot, pop_size):
        self._base_bot = bot
        self._population = []

        self._game_cost = 100
        self._initial_energy = self._game_cost * 2

        for i in range(pop_size):
            new_bot = self._create_new_bot()
            self._population.append(new_bot)

    @property
    def population(self):
        return self._population

    def run(self, iteration_count):
        for i in range(iteration_count):
            op1, op2 = self.find_players(self._population)
            self.play_game(op1, op2)

            self._evolve(self._population)
            self.sort_population(self._population)

            best = self._population[0]
            worst = self._population[-1]
            print(f"EPOCH: {i}")
            print(f"BEST: age {best.age}, energy {int(best.energy)}")
            print(f"WORST: age {worst.age}, energy {int(worst.energy)}")

    def play_game(self, p1, p2):
        self._play_board(p1, p2)
        self._play_board(p2, p1)

    def find_players(self, population):
        p1, p2 = np.random.choice(population, 2, replace=False)
        if p1 == p2:
            raise NotImplementedError("selection")

        return p1, p2

    def sort_population(self, population):
        population.sort(key=lambda b: b.energy, reverse=True)

    def _play_board(self, bot1, bot2):
        board = Board(BOARD_SIZE, WIN_LENGTH)

        sc1 = bot1.score
        sc2 = bot2.score
        while not board.is_game_over:
            self._play_turn(bot1, board)
            self._play_turn(bot2, board)

        print(f"\t board: {board.turn_index} turns")
        print("\t " + board.to_str().replace("\n", "\n\t "))

        gain1 = bot1.score - sc1
        gain2 = bot2.score - sc2
        if gain1 > gain2:
            bot1.energy += self._game_cost
            bot2.energy -= self._game_cost
        if gain2 > gain1:
            bot1.energy -= self._game_cost
            bot2.energy += self._game_cost

    def _play_turn(self, bot, board):
        if board.is_game_over:
            return

        x, y = bot.get_move(board, None)

        board.try_make_move(x, y)

        if board.is_win:
            bot.score += 1

    def _evolve(self, population):
        for i in range(len(population)):
            population[i].age += 1
            if population[i].energy <= 0:
                new_bot = self._create_evoluted_bot(population)
                new_bot.energy += population[i].energy
                population[i] = new_bot

    def _initialize(self, p):
        for i in range(p.shape[0]):
            for j in range(p.shape[1]):
                p[i][j] = np.random.uniform(-1, 1)

    def _create_new_bot(self):
        new_bot = self._base_bot.clone()
        new_bot.energy = self._initial_energy
        new_bot.age = 0
        for p in new_bot.parameters:
            self._initialize(p)

        return new_bot

    def _create_evoluted_bot(self, population):
        self.sort_population(population)
        parent1 = self._select_from(population)
        parent2 = self._select_from(population)
        child = parent1.clone()

        for p1, p2, ch in zip(parent1.parameters, parent2.parameters, child.parameters):
            for i in range(p1.shape[0]):
                for j in range(p1.shape[1]):
                    v1 = p1[i][j]
                    v2 = p2[i][j]
                    avg = (v1 + v2) / 2
                    value = random.choice([v1, v2, v1, v2, avg, avg + random.uniform(-0.1, 0.1)])
                    ch[i][j] = value

        p1gain = max(self._game_cost, parent1.energy / 2)
        p2gain = max(self._game_cost, parent2.energy / 2)

        child.energy = p1gain + p2gain
        child.age = 0

        parent1.energy -= p1gain
        parent2.energy -= p2gain

        return child

    def _select_from(self, population):
        total_energy = len(population) * self._initial_energy
        while True:
            for i in range(len(population)):
                if random.uniform(0, 1) < population[i].energy / total_energy:
                    return population[i]

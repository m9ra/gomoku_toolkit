from time import sleep

from game.board import Board
from game.player import Player

MOVE_TIMEOUT = 5.0
BOARD_SIZE = 15
WIN_LENGTH = 5


def play_local_match(bot1, bot2, game_count, print_boards=False):
    bot1.score = 0
    bot2.score = 0
    for i in range(game_count):
        print(f"bot1: {bot1.score} | bot2: {bot2.score}")

        play_board(bot1, bot2, print_boards)
        play_board(bot2, bot1, print_boards)

    print(f"FINAL SCORE: bot1: {bot1.score} | bot2: {bot2.score}")


def play_in_arena(bot, game_count_limit, arena, username):
    if username is None:
        raise ValueError("Username has to be specified.")

    player = Player(arena, username, bot, game_count_limit)
    while player.is_connected:
        # todo console controlling
        sleep(1)


def play_board(bot1, bot2, print_boards):
    board = Board(BOARD_SIZE, WIN_LENGTH)
    while not board.is_game_over:
        play_turn(bot1, board)
        play_turn(bot2, board)

    print(f"\t board: {board.turn_index} turns")
    if print_boards:
        print("\t " + board.to_str().replace("\n", "\n\t "))


def play_turn(bot, board):
    if board.is_game_over:
        return

    x, y = bot.get_move(board, MOVE_TIMEOUT)
    board.try_make_move(x, y)

    if board.is_win:
        bot.score += 1

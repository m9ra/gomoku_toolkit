import sys
from threading import Thread
from time import sleep

import configuration
from configuration import BOARD_SIZE, WIN_LENGTH, MOVE_TIMEOUT
from game.board import Board
from game.player import Player


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

    if '@' not in username:
        raise ValueError("Email as a username is expected.")

    print("Interactive Arena Console. For help press 'h' followed by enter.")
    player = Player(arena, username, bot, game_count_limit)

    Thread(target=_interactive_console, args=[player], daemon=True, ).start()

    while player.is_connected:
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
    if x is None or y is None:
        print("MISSING MOVE DETECTED (maybe timeout - stopping for easier debugging)")
        sys.exit(2)

    board.try_make_move(x, y)

    if board.is_win:
        bot.score += 1


def _interactive_console(player):
    for cmd in sys.stdin:
        print("Recognized cmd: %s" % cmd)

        command = cmd.strip().lower() + " "
        command = command + " "
        c = command[0]
        if c == "s":
            player._game_count_limit = 0
            print("PLAYER WILL BE STOPPED AFTER NEXT GAME")
        elif c == "m":
            configuration.PRINT_INTERMEDIATE_BOARDS = not configuration.PRINT_INTERMEDIATE_BOARDS
        elif c == "n":
            configuration.PRINT_NETWORK_COMMUNICATION = not configuration.PRINT_NETWORK_COMMUNICATION
        elif c == "b":
            configuration.PRINT_RESULT_BOARDS = not configuration.PRINT_RESULT_BOARDS


        else:
            print("Console commands (after command press enter):")
            print("\t 's' - stops current game.")
            print("\t 'm' - toggle move before board printing.")
            print("\t 'b' - toggle finished board printing.")
            print("\t 'n' - toggle network communication printing.")

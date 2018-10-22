from bots.conv_bot import ConvBot
from bots.minmax_bot import MinmaxBot
from bots.minmax_bot2 import MinmaxBot2
from bots.minmax_bot3 import MinmaxBot3
from bots.minmax_bot4 import MinmaxBot4
from bots.minmax_bot5 import MinmaxBot5
from bots.minmax_bot6 import MinmaxBot6
from game.board import Board
from game.runtime import play_local_match

# import your bots
from bots.random_bot import RandomBot
from bots.random_search_bot import RandomSearchBot

# """

board = Board(15, 5,
              moves=[(6, 6), (6, 9), (5, 6), (7, 6), (4, 6), (3, 6), (5, 5), (5, 8), (4, 7), (4, 4), (6, 5), (7, 4), (6, 4), (6, 7), (3, 7), (7, 3), (2, 8)])

"""

print(board.to_str())
bot = MinmaxBot5()
move = bot.get_move(board, 0)

print(move)
board.make_move(move[0], move[1])
print(board.to_str())
exit(0)
# """

play_local_match(
    bot1=MinmaxBot5(),
    bot2=MinmaxBot6(),
    # bot2=RandomSearchBot(think_time_limit=0.1),
    game_count=100,
    print_boards=True
)

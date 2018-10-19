from bots.conv_bot import ConvBot
from bots.minmax_bot import MinmaxBot
from bots.minmax_bot2 import MinmaxBot2
from bots.minmax_bot3 import MinmaxBot3
from bots.minmax_bot4 import MinmaxBot4
from game.board import Board
from game.runtime import play_local_match

# import your bots
from bots.random_bot import RandomBot
from bots.random_search_bot import RandomSearchBot

# """

board = Board(15, 5,
              moves=[(10, 4), (13, 4), (9, 4), (8, 4), (10, 3), (11, 2), (10, 5), (10, 6), (10, 2), (10, 1), (12, 3)])

"""

print(board.to_str())
bot = MinmaxBot2()
move = bot.get_move(board, 0)

print(move)
board.make_move(move[0], move[1])
print(board.to_str())
exit(0)
# """

play_local_match(
    bot1=MinmaxBot4(),
    bot2=MinmaxBot(),
    # bot2=RandomSearchBot(think_time_limit=0.1),
    game_count=100,
    print_boards=True
)

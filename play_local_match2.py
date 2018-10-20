from bots.conv_bot import ConvBot
from bots.minmax_bot import MinmaxBot
from bots.minmax_bot2 import MinmaxBot2
from bots.minmax_bot3 import MinmaxBot3
from bots.minmax_bot4 import MinmaxBot4
from bots.minmax_bot5 import MinmaxBot5
from game.board import Board
from game.runtime import play_local_match

# import your bots
from bots.random_bot import RandomBot
from bots.random_search_bot import RandomSearchBot

# """

board = Board(15, 5,
              moves=[[4, 8], [4, 9], [5, 9], [6, 10], [3, 7], [2, 6], [5, 8], [5, 7], [6, 8], [3, 8], [7, 8], [8, 8], [7, 7], [8, 6], [4, 10], [3, 11], [7, 9], [7, 6], [7, 10], [7, 11], [6, 9], [4, 7], [8, 9], [9, 9], [8, 11], [9, 12]])

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
    bot2=MinmaxBot(),
    # bot2=RandomSearchBot(think_time_limit=0.1),
    game_count=100,
    print_boards=True
)

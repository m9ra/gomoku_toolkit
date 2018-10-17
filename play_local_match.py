from bots.minmax_bot import MinmaxBot
from game.board import Board
from game.runtime import play_local_match

# import your bots
from bots.random_bot import RandomBot
from bots.random_search_bot import RandomSearchBot



# """
board = Board(15, 5, moves=[[9, 2], [8, 1], [8, 3], [7, 4], [9, 3], [7, 3], [9, 1], [9, 4], [10, 2], [8, 4], [6, 4], [6, 2], [5, 1], [7, 2], [7, 1], [5, 2], [4, 2], [6, 3]])

print(board.to_str())
bot = MinmaxBot()
move = bot.get_move(board, 0)

print(move)
board.make_move(move[0], move[1])
print(board.to_str())
exit(0)
# """
play_local_match(
    bot1=MinmaxBot(),
    bot2=RandomSearchBot(think_time_limit=0.1),
    # bot2=RandomSearchBot(think_time_limit=0.1),
    game_count=100,
    print_boards=True
)

from game.runtime import play_local_match

# import your bots
from bots.random_bot import RandomBot
from bots.random_search_bot import RandomSearchBot

play_local_match(
    bot1=RandomSearchBot(think_time_limit=0.1),
    bot2=RandomBot(),
    # bot2=RandomSearchBot(think_time_limit=0.1),
    game_count=100,
    print_boards=True
)

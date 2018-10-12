from configuration import MAIN_ARENA
from game.runtime import play_in_arena

# import your bot
from bots.random_bot import RandomBot

# When launched - interactive console appears (allows to stop bot peacefully - without loosing points).

# NOTE: 's' followed by enter will stop asap without loosing points.
# Killing the process forcefully will cause loosing games in progress.

play_in_arena(

    # Change your details here as you wish.
    bot=RandomBot(),
    game_count_limit=None,  # unlimited game count - bot will play until stopped externally

    # permanent game settings - change once and forget
    arena=MAIN_ARENA,
    username=None,  # todo fill in your username (in form of myname@cz.ibm.com). Only one username per user is allowed!!
)

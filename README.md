# Gomoku Toolkit
Toolkit for gomoku bot development.

* Requires python 3.6 or higher.
* Two modes of operation:
    * local match between two given bots (run `play_local_match.py`)
    * remote match against opponents found in an arena (run `play_in_arena.py`)
        * when script is running following console commands are available:
        ```bash
            Console commands (after command press enter):
            's' - stops current game.
            'm' - toggle move before board printing.
            'b' - toggle finished board printing.
            'n' - toggle network communication printing.
        ```


## Preimplemented stuff
* Game rules (via `Board` from `game/board.py`)
* Baseline bots (see package `bots`)
    * Random bot 
        * basic intro into the game API
        * randomly selects an available move 
    * Random search bot 
        * basic intro into the prepared asynchronous API 
        * randomly tries available moves and evaluates against a trivial score function
        * search is limited by thinking time       
        
* Debugging tools
    * See `configuration.py` for various verbosity levels.
    
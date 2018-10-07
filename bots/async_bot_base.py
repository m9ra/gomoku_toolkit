import time
from multiprocessing import RLock
from threading import Thread, Condition

from bots.bot_base import BotBase


class AsyncBotBase(BotBase):

    def run_search(self, board):
        raise NotImplementedError("must be overriden")

    @property
    def can_search(self):
        with self._L_global:
            return self._can_search

    def __init__(self, think_time_limit=None):
        super().__init__()

        self._think_time_limit = think_time_limit

        self._C_search_run = Condition()
        self._L_global = RLock()
        # synchronized resources
        self._actual_best = None
        self._can_search = False
        self._is_search_running = False

    def report_actual_best(self, x, y):
        with self._L_global:
            self._actual_best = (x, y)

    def get_move(self, board, timeout):
        start_time = time.time()
        self._initialize_search()

        thread = Thread(target=self._run_search, daemon=True, args=[board])
        thread.start()

        # calculate timeout
        if self._think_time_limit:
            real_timeout = min(self._think_time_limit, timeout)
        else:
            real_timeout = timeout

        elapsed_time = time.time() - start_time
        remaining_time = max(0.001, real_timeout - elapsed_time)

        # wait until answer has to be provided
        thread.join(remaining_time)

        with self._L_global:
            self._can_search = False
            return self._actual_best

    def _initialize_search(self):
        # blocks until search can be run (ensures previous search ended)

        self.report_actual_best(None, None)
        with self._C_search_run:
            while self._is_search_running:
                # wait until previous search is complete
                self._C_search_run.wait()

            self._is_search_running = True

        with self._L_global:
            self._can_search = True

    def _run_search(self, board):
        try:
            self.run_search(board)
        finally:
            with self._C_search_run:
                self._is_search_running = False
                self._C_search_run.notify()

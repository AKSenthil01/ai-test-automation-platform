import time


class Timer:

    def __init__(self):

        self.start = {}

    def begin(self, name):

        self.start[name] = time.time()

    def end(self, name):

        if name not in self.start:
            return 0

        return round(
            time.time() - self.start[name],
            2
        )
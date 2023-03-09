import time


class Time:

    def __init__(self, interval):
        self.interval = interval
        self.equivalent = {"1m": 60, "4h": 14400, "1d": 86400, "1h":3600}

    @staticmethod
    def get_time():
        return time.time()

    @staticmethod
    def current_date():
        current_time = time.localtime()
        current_time = time.strftime("%d/%m/%Y %H:%M:%S", current_time)
        return current_time

    def time_to_wait(self, elapsed_time):
        return self.equivalent[self.interval] - elapsed_time

    def wait_next_interval(self, elapsed_time):
        time.sleep(self.time_to_wait(elapsed_time))

    @staticmethod
    def wait(secondes):
        time.sleep(secondes)

from datetime import datetime, timedelta
from time import time

start_time = time()


def get_time_passed():
    """Возвращает время пройденное со старта бота"""
    sec = timedelta(seconds=int(time() - start_time))
    d = datetime(1, 1, 1) + sec
    return "%d:%d:%d:%d" % (d.day-1, d.hour, d.minute, d.second)

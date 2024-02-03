import os
from logging.handlers import RotatingFileHandler


class MakeRotatingFileHandler(RotatingFileHandler):
    def __init__(self, filename, mode="a", maxBytes=1024 * 1024 * 10, backupCount=0, encoding=None, delay=0):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        RotatingFileHandler.__init__(self, filename, mode, maxBytes, backupCount, encoding, delay)

__author__ = 'Ralph'

import sys
import time


class DummyStream:
    def __init__(self):
        pass

    def write(self, data):
        pass

    def read(self, data):
        pass

    def flush(self):
        pass

    def close(self):
        pass


class ConsoleUtil:
    def __init__(self):
        self.old_printerators = [sys.stdout, sys.stderr, sys.stdin][:]

    def disable_console_output(self):
        sys.stdout = DummyStream()
        sys.stderr = DummyStream()
        sys.stdin = DummyStream()

    def enable_console_output(self):
        sys.stdout, sys.stderr, sys.stdin = self.old_printerators

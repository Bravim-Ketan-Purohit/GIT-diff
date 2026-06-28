"""Sample module used by extractor tests."""
import os


def helper(x):
    return os.path.basename(x)


class Greeter:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return helper(self.name)

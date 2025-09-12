from smart_home.core.base import Observer
from smart_home.core.base import Singleton


class ConsoleObserver(metaclass=Singleton, Observer):

    @staticmethod
    def update(message: str):
        print(message)

from smart_home.core.singleton import Singleton


class ConsoleObserver(Singleton):

    @staticmethod
    def update(message: str):
        print(message)

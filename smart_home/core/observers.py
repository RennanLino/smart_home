from smart_home.core.base import Observer


class ConsoleObserver(Observer):

    @staticmethod
    def update(message: str):
        print(message)

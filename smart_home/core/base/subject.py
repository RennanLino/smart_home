from typing import List


class Subject:
    def __init__(self):
        self.__observers: List["Observer"] = []

    def subscribe(self, observer):
        self.__observers.append(observer)

    def unsubscribe(self, observer):
        self.__observers.remove(observer)

    def notify(self, *args, **kwargs):
        for observer in self.__observers:
            observer.update(*args, **kwargs)
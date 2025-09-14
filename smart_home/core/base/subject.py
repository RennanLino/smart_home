from typing import List


class Subject:
    def __init__(self):
        self.observers: List["Observer"] = []

    def subscribe(self, observer):
        self.observers.append(observer)

    def unsubscribe(self, observer):
        self.observers.remove(observer)

    def notify(self, *args, **kwargs):
        for observer in self.observers:
            observer.update(self, *args, **kwargs)
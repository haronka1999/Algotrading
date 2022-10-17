from abc import abstractmethod


class Strategy:

    @abstractmethod
    def calculateStrategy(self):
        pass

    @abstractmethod
    def plot(self):
        pass



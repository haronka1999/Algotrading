from abc import abstractmethod


class Strategy:

    @abstractmethod
    def calculateValuesForDf(self, columns):
        pass

    @abstractmethod
    def plot(self):
        pass



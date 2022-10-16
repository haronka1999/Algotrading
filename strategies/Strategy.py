from abc import abstractmethod


class Strategy:

    @abstractmethod
    def retrieveData(self):
        pass

    @abstractmethod
    def createDF(self):
        pass

    @abstractmethod
    def plot(self):
        pass



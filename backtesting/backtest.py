import pandas as pd


def get_formatted_series(series: pd.Series) -> pd.Series:
    """
    The function will reformulate the given series for a  better visualization for displaying the profits
    :param series:  the series which will be formatted
    :return:  the formatted series
    """
    index_name = []
    for i in range(len(series)):
        # reformat index
        index_name.append("Return for Trade " + str(i) + ": ")
        # reformat value
        series.iloc[i] = str(round(series.iloc[i] * 100, 2)) + " %"

    series.index = index_name
    return series


class Backtest:
    """
    Video: https://www.youtube.com/watch?v=yTupVd6D9m8&ab_channel=Algovibes
    Version Number: 1.0 V
    Description:
        A class where performance measures and backtesting libraries are implemented

        The input parameter should be a sub instnace of strategy.py and
        selldates, buydates, sellprices buyprices  attributes should be filled
    """

    def __init__(self, strategy):
        self.buyprices = strategy.buyprices
        self.sellprices = strategy.sellprices
        self.relative_returns = pd.Series(
            [(self.sellprices - self.buyprices) / self.buyprices for self.sellprices, self.buyprices
             in zip(self.sellprices, self.buyprices)])

    def get_relative_returns(self):
        return get_formatted_series(self.relative_returns.copy())

    def get_cumulative_returns(self):
        cum_return = (self.relative_returns + 1).prod() - 1
        return str(round(cum_return * 100, 2)) + " %"

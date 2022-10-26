from strategies.MeanReversion import MeanReversion
from strategies.Strategy import Strategy

# Testing Backtesting library
meanReversion = MeanReversion('BTCUSDT', '30m', MeanReversion.COLUMN_LIST, startDate='2022-08-01',
                              endDate=Strategy.today)
print(meanReversion.mergeFearAndGreedWithDf())

# backtest_meanReversion = Backtest(meanReversion)
# print(backtest_meanReversion.get_relative_returns())
# print(backtest_meanReversion.get_cumulative_returns())
#
#
#
# bollingerBands = BollingerBand('BTCUSDT', '30m', BollingerBand.COLUMN_LIST, startDate='2022-08-01',
#                                endDate=Strategy.today)
# backtest_bollingerBands = Backtest(bollingerBands)
# print(backtest_bollingerBands.get_relative_returns())
# print(backtest_bollingerBands.get_cumulative_returns())

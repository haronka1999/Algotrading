from strategies.bollinger_band import BollingerBand
from strategies.mean_reversion import MeanReversion
from strategies.stoch_RSI_MACD import StochRSIMACD
from strategies.strategy import Strategy
from utils import constants
from utils.constants import no_end_date, no_start_date, no_lookback_time

# Testing Backtesting library
stochRSIMACD = BollingerBand('BTCUSDT', '15m', lookback_time=no_lookback_time, start_date="2022-11-18",
                            end_date="2022-12-11")

class Constants:
    """
    This class stores every constant what is used in the project
    """
    COLUMN_LIST = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    FULL_COLUMN_LIST = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume',
                        'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore']
    TRADE_OUTPUT_HEADER = ["Time", "Symbol", "Price", "Quantity", "USD", "Side"]
    MARKER_SIZE = 400
    NO_LOOKBACK_TIME = "-1"
    NO_START_DATE = "noStartDate"
    NO_END_DATE = "noEndDate"
    LOOKBACK_TIME_FOR_BOTS = "50m"
    DEFAULT_STRATEGY_STR = "Choose"
    DATE_FORMAT = '%Y-%m-%d'




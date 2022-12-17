"""
--------------------  Revision History: ----------------------------------------
# 2022-11-15    -   Class created: rss_feed_urls, item_attr_map added
* 2022-11-16    -   Added COLUMN_LIST
--------------------------------------------------------------------------------
Description:
    A classed used for storing general constants
---------------------------------------------------------------------------
"""
COLUMN_LIST = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']

FULL_COLUMN_LIST = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume',
                    'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore']

marker_size = 400
no_lookback_time = "-1"
no_start_date = "noStartDate"
no_end_date = "noEndDate"
lookback_time_for_bots = "5m"
default_strategy_str = "Choose"

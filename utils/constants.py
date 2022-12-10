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

no_lookback_time = "-1"
no_start_date = "noStartDate"
no_end_date = "noEndDate"
lookback_time_for_bots = "5m"
default_strategy_str = "Choose"

rss_feed_urls = ["https://www.coindesk.com/arc/outboundfeeds/rss/", "https://cointelegraph.com/rss",
                 "https://news.bitcoin.com/feed/",
                 "https://cryptopotato.com/feed/", "https://zycrypto.com/category/news/feed/",
                 "https://nulltx.com/feed/", "https://coinquora.com/news/feed/", "https://ambcrypto.com/feed/",
                 "https://cryptoslate.com/feed/",
                 "https://crypto.news/feed/"]

item_attr_map = {"https://www.coindesk.com/arc/outboundfeeds/rss/":
                     {"title": "title", "link": "link", "pub_date": "published",
                      "summary": "summary", "image": ("media_content", 0, "url")},

                 "https://cointelegraph.com/rss": {"title": "title",
                                                   "link": "link", "pub_date": "published",
                                                   "summary": {"summary": ("p", 1, "text")},
                                                   "image": {"summary": ("img", "src")}},

                 "https://news.bitcoin.com/feed/": {"title": "title",
                                                    "link": "link", "pub_date": "published",
                                                    "summary": "bnmedia_barker_title",
                                                    "image": "bnmedia_url"},

                 "https://cryptopotato.com/feed/": {"title": "title",
                                                    "link": "link", "pub_date": "published",
                                                    "summary": "summary",
                                                    "image": ("media_content", 0, "url")},

                 "https://zycrypto.com/category/news/feed/": {"title": "title",
                                                              "link": "link", "pub_date": "published",
                                                              "summary": {"summary": "text"},
                                                              "image": {"summary": ("img", "src")}},

                 "https://nulltx.com/feed/": {"title": "title",
                                              "link": "link", "pub_date": "published",
                                              "summary": {"summary": ("p", 0, "text")},
                                              "image": None},

                 "https://coinquora.com/news/feed/": {"title": "title",
                                                      "link": "link", "pub_date": "published",
                                                      "summary": {"summary": "text"},
                                                      "image": {"summary": ("img", "src")}},

                 "https://ambcrypto.com/feed/": {"title": "title",
                                                 "link": "link", "pub_date": "published",
                                                 "summary": {"summary": "text"},
                                                 "image": {"summary": ("img", "src")}},

                 "https://cryptoslate.com/feed/": {"title": "title",
                                                   "link": "link", "pub_date": "published",
                                                   "summary": {"summary": ("p", 0, "text")},
                                                   "image": None},

                 "https://crypto.news/feed/": {"title": "title",
                                               "link": "link", "pub_date": "published",
                                               "summary": "summary",
                                               "image": ("media_content", 0, "url")}
                 }

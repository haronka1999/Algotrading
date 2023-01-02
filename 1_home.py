import streamlit as st

from utils.utility_methods import add_articles, generate_articles, get_crypto_prices

class HomeUI:
    """
    This Class refers to the main page of the UI.
    Contains a news feed and the most recent crypto prices.
    Each method refer for one element of the UI.
    """

    def __init__(self):
        self.col1, self.col2 = st.columns(2, gap='Large')

    def generate_col1(self):
        with self.col1:
            st.header("Welcome ! ")
            st.subheader("Here are some news from the World:")
            my_articles = generate_articles()[:5]
            add_articles(my_articles)

    def generate_col2(self):
        with self.col2:
            crypto_prices_df = get_crypto_prices(["BTCUSDT", "ETHUSDT", "AXSUSDT"])
            last_updated = crypto_prices_df["Last Updated"].iloc[-1]
            crypto_prices_df = crypto_prices_df.iloc[:, :2]
            st.header("Latest crypto prices")
            st.write(f'last_updated: {last_updated}')
            st.dataframe(crypto_prices_df)


homeUI = HomeUI()
homeUI.generate_col1()
homeUI.generate_col2()

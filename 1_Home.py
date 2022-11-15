"""
--------------------  Revision History: ----------------------------------------
* 2022-10-15    -   Class Created, feed is implemented
--------------------------------------------------------------------------------
Version Number: 1.0 V
Description:

    The main page of the UI. Contains a news feed and crypt prices
"""

import streamlit as st
from bs4 import BeautifulSoup
from feedparser import parse

item_attr_map = {
    "https://cointelegraph.com/rss": {"title": "title",
                                      "link": "link", "pub_date": "published",
                                      "summary": {"summary": ("p", 1, "text")},
                                      "image": {"summary": ("img", "src")}},
}


def add_articles(articles):
    no_of_articles = len(articles)
    article_index = 0
    col_index = -1
    while True:
        article = articles[article_index]
        title = article["title"]
        link = article["link"]
        date = article["pub_date"]
        st.markdown(f"### [{title}]({link})")
        if article["image"] is None:
            if "nulltx" in link:
                st.image("https://nulltx.com/wp-content/uploads/2018/10/nulltx-logo-red.png")
            if "cryptoslate" in link:
                st.image("https://cryptoslate.com/wp-content/themes/cryptoslate-2020/images/cs-media-logo-dark.png",
                         width=320)
        else:
            st.image(article["image"])
        st.caption(f"{date}")
        st.write(article["summary"])

        if no_of_articles == article_index + 1:
            return

        article_index += 1
        col_index *= -1


def generate_articles():
    rss_articles = []
    for url in item_attr_map.keys():
        feed = parse(url)
        items = feed['entries']
        for item in items:
            attrs = item_attr_map[url]
            article = {}

            for key, val in attrs.items():
                if key == "pub_date":
                    article[key] = item[val][5:-5]
                elif type(val) == str:
                    article[key] = item[val]
                elif val is None:
                    article[key] = None

                elif type(val) == dict:
                    nested_key = list(val.keys())[0]
                    nested_val = val[nested_key]
                    soup = BeautifulSoup(item[nested_key], features="lxml")
                    if val[nested_key] == "text":
                        article[key] = soup.text
                    elif type(nested_val) == tuple:
                        if nested_key == "summary":
                            if len(nested_val) == 2:
                                article["summary"] = soup.text
                            elif len(nested_val) == 3:
                                article["summary"] = soup.find_all(
                                    [nested_val[0]])[nested_val[1]].text
                        if key == "image":
                            article["image"] = soup.find([nested_val[0]]).get(nested_val[1])
            rss_articles.append(article)
    return rss_articles


col1, col2 = st.columns(2)
with col1:
    st.header("Welcome ! ")
    st.subheader("Here are some news from the World:")
    my_articles = generate_articles()
    add_articles(my_articles)
with col2:
    st.header("Crypto proces")
    st.write("Crypto 1")
    st.write("Crypto 2")
    st.write("Crypto 3")

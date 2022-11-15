import re

import streamlit as st

def validateInputs(ticker_symbol, interval, lookBackHours,startDate,endDate):
    if ticker_symbol == "":
        return "Ticker  field is empty"
    if any(not c.isalnum() for c in ticker_symbol) and ticker_symbol.isnumeric():
        return "Ticker symbol contains unallowed characters"


    if interval == "":
        return "Interval  field is empty"

    if not re.match('^(\d*\d){1,2}[h,d,m]$', interval):
        return "The Interval is not in correct format"



    return ""

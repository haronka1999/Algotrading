__version__ = "1.0.0"

def validateInputs(ticker_symbol, interval, lookBackHours, startDate, endDate):
    if ticker_symbol == "":
        return "Ticker  field is empty"

    if interval == "":
        return "Interval  field is empty"

    if ticker_symbol == "":
        return "Ticker  field is empty"

    if lookBackHours == "" and (startDate == "" or endDate == ""):
        return "Choose or Look Back Hours or date interval"


    if lookBackHours != "" and startDate != "" and endDate != "":
        return "Please Choose or LookBackHorus or a date interval, not both"

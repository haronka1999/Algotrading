# Algotrading


## Introduction
The Algotrading platform provides an easy to use interface to Backtest trading strategies (based on technical indicators). There is the possibility to Backtest and Launch Trading Bots with simulation and also with real money. It uses the [python-binance](https://python-binance.readthedocs.io/en/latest/) unofficial Python wrapper for the Binance exchange REST API to access data and launch trades.

## Purpose
This platform is a learning project to be familiar with the Python programming language and to use it's advanced features, besides to gain experience  in Data Science by using diferent libraries like numpy, pandas, matplotlib and scikit-learn for applying several types of regression model.

IMPORTANT DISCLAIMER
<br>
These strategies are not  highly profitable. It is possible to make some profit, but I do not advice it to use it frequently with your real money.

## Using the Software

There are two possibilites to access the functionalities: 
<br/>
1. Web Application 
<br>
A simple web app was written to easily access every functionalities.
<br/>
It uses the https://streamlit.io python library.
<br/> 
For access the program please follow this link:TESTLINKTESTLINK
<br/>
<br/>

2. Command line interface
<br/>

If you run the main.py with the `python main.py` command it will launch the application and it will enable the user to start trading bots with simulation and with real money.
<br/>
Notes: Backtesting functionalities with data visualization is not available with this method

## Code usage

First, In your python environment, install all the packages by running the 
<br/>
`pip install -r requirements.txt`.
<br/>
Than you need to run the main page of the UI by using the streamlit library's `run` command: `streamlit run 1_home.py` . It will launch an instance of the web application.

## Contribution

I'm happily process any improvement idea, any bugfix or trading strategies to implement. You can Contact me at here, [LinkedIn](https://www.linkedin.com/in/aronhorvath-954b23188) or via email: aron.horvath1999@gmail.com

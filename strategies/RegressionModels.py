"""
--------------------  Revision History: ----------------------------------------
# 2022-11-11    -   Class created
--------------------------------------------------------------------------------
Video: https://www.youtube.com/watch?v=AXBhrLongC8&t=430s
Version Number: 1.0 V
Description

Taking past data to predict future return if the return is positive we hold,
otherwise the asset should be shorted
---------------------------------------------------------------------------
"""

from venv import create
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, RidgeCV, Lasso
import numpy as np
import time
import datetime  as dt
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

from strategies.Strategy import Strategy
from utils.Utilities import today


def _plot(X, y, y_pred, model):
    X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, stratify=None, train_size=0.8)
    plt.scatter(X_test, y_test, color="black")
    plt.plot(X_test, y_pred, color="blue", linewidth=3)
    plt.xticks(())
    plt.yticks(())
    plt.show()
    print("Coefficients: \n", model.coef_)
    print("Mean squared error: %.2f" % mean_squared_error(y_test, y_pred))
    # The coefficient of determination: 1 is perfect prediction
    print("Coefficient of determination: %.2f" % r2_score(y_test, y_pred))


class RegressionModels(Strategy):
    df = pd.DataFrame()
    COLUMN_LIST = ['Time', 'Open']

    def __init__(self, ticker, interval, columns, lookbackHours='-1', startDate='noStartDate', endDate=today):
        super(RegressionModels, self).__init__(ticker, interval, columns, lookbackHours, startDate, endDate)
        # clean the dataframe and set values for column
        self._calculateValuesForDf(columns)
        print(self.df.head(30))

    def plotLinearRegression(self):
        X = self.df.Time
        y = self.df.Open
        X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, stratify=None, train_size=0.8)
        X_train = X_train.values.reshape(-1, 1)
        y_train = y_train.values.reshape(-1, 1)
        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test.values.astype(float).reshape(-1, 1))
        df_pred = pd.concat([X_test, y_test], axis=1)
        df_pred['Pred'] = y_pred
        df_pred['Error'] = abs((df_pred.Pred / df_pred.Open) - 1)
        _plot(X,y,y_pred,model)
        return df_pred, model

    # TODO: check datei
    def _calculateValuesForDf(self, columns):
        pass
        #(self.df.Time.to_datetime())
        #self.df.Time.to_timestamp()

    def plot(self):
        pass

regressionModel = RegressionModels('BTCUSDT', '15m', RegressionModels.COLUMN_LIST, startDate='2022-04-01')
regressionModel.plotLinearRegression()

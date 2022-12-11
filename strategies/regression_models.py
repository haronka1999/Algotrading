"""
--------------------  Revision History: ----------------------------------------
# 2022-11-11    -   Class created
* 2022-11-16    -   Deleted default values for constructor's parameter list (it is handled in the UI side)
--------------------------------------------------------------------------------
Video: https://www.youtube.com/watch?v=AXBhrLongC8&t=430s
Description

Taking past data to predict future return is positive we hold,
otherwise the asset should be shorted
---------------------------------------------------------------------------return if the r
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from strategies.strategy import Strategy


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
    def __init__(self, ticker, interval, lookback_time, startDate, end_date, api_key="", api_secret=""):
        super(RegressionModels, self).__init__(ticker, interval, lookback_time, startDate, end_date, api_key, api_secret)
        # clean the dataframe and set values for column
        self.calculate_values_for_df()
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
    def calculate_values_for_df(self):
        pass
        # (self.df.Time.to_datetime())
        # self.df.Time.to_timestamp()

    def plot(self):
        pass

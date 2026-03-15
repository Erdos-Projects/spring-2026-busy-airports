import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error as mse
from sklearn.model_selection import TimeSeriesSplit
from statsmodels.tsa.api import ExponentialSmoothing

from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import mean_absolute_error as mae
from sklearn.metrics import mean_absolute_percentage_error as mape

#General function to measure different types of errors in predictions
def evaluate_forecast(actual, predicted, model_name):
    mae  = np.mean(np.abs(actual - predicted))
    mape = np.mean(np.abs((actual - predicted) / actual)) * 100
    rmse = np.sqrt(np.mean((actual - predicted) ** 2))
    print(f"\n{model_name}")
    print(f"  MAE:  {mae:,.0f}")
    print(f"  MAPE: {mape:.2f}%")
    print(f"  RMSE: {rmse:,.0f}")
    return {'mae': mae, 'mape': mape, 'rmse': rmse}

#Baseline model 1: Naive with Seasonal Drift
class NaiveSeasonalWithDrift:
    def __init__(self, season_length):
        self.season_length = season_length
        self.deltas = None
        self.last_value = None
    def fit(self, ts):
        if isinstance(ts, pd.Series):
            ts = ts.values
        s = self.season_length
        if len(ts) < s + 1:
            raise ValueError("Need more data than one season")
        self.deltas = ts[-s:] - ts[-s-1:-1]
        self.last_value = ts[-1]

    def forecast(self, h):
        s = self.season_length
        forecasts = np.zeros(h)
        forecasts[0] = self.last_value + self.deltas[0]
        for i in range(1, h):
            forecasts[i] = forecasts[i-1]+self.deltas[i%s]
        return forecasts
    
#Baseline model 2: Triple Exponential Smoothing
    
class TripleExponentialSmoothing:
    def __init__(self, season_length):
        self.season_length = season_length
        self.model = None
    def fit(self, ts):
        self.model = ExponentialSmoothing(ts, trend="add", seasonal="add", seasonal_periods=self.season_length, initialization_method="estimated" ).fit()
    def forecast(self, h):
        return self.model.forecast(h)
    

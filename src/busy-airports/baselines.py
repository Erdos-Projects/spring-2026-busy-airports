"""
baselines.py

Baseline models for Cross-Validation
"""

import numpy as np
import pandas as pd
from statsmodels.tsa.api import ExponentialSmoothing

# Baseline Model 1: Naive Seasonal with Drift
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

# Baseline Model 2: Triple Exponential Smoothing (Holt/Winters)
class TripleExponentialSmoothing:
    def __init__(self, season_length):
        self.season_length = season_length
        self.model = None
    def fit(self, ts):
        self.model = ExponentialSmoothing(ts, trend="add", seasonal="add", seasonal_periods=self.season_length, initialization_method="estimated" ).fit()
    def forecast(self, h):
        return self.model.forecast(h)

"""
models.py

Forecasting models for TSA data
"""

import numpy as np
import pandas as pd
from statsmodels.tsa.api import SARIMAX
from busy_airports.harmonic_model import fourier_features

# Harmonic Regression model with daily throughput data
class HarmonicARIMA:

    def __init__(self, season_length, n_freq, arima_order, seasonal_order, with_intercept=True):
        self.season_length = season_length
        self.n_freq = n_freq
        self.arima_order = arima_order
        self.seasonal_order = seasonal_order
        self.arima_trend = ('c' if with_intercept else 'n')
    
    def fit(self, ts_index, ts_data, maxiter=50):
        X_fourier = fourier_features(ts_index, m = self.season_length, k = self.n_freq)
        sarimax_model = SARIMAX(ts_data,
                                exog = X_fourier,
                                order = self.arima_order,
                                seasonal_order = self.seasonal_order,
                                trend = self.arima_trend)
        self.fitted_model = sarimax_model.fit(maxiter=maxiter)
    
    def forecast(self, ts_index):
        X_fourier = fourier_features(ts_index, m = self.season_length, k = self.n_freq)
        results = self.fitted_model.get_forecast(steps = len(ts_index), exog = X_fourier)
        return results.predicted_mean
    
    def conf_int(self, ts_index, alpha=0.05):
        X_fourier = fourier_features(ts_index, m = self.season_length, k = self.n_freq)
        results = self.fitted_model.get_forecast(steps = len(ts_index), exog = X_fourier)
        return results.conf_int(alpha=alpha)

# STL model with Daily Data
class STLDaily:
    def __init__(self, season_length):
        pass
    def fit(self, ts):
        pass
    def forecast(self, h):
        pass

# STL model with Weekly Data
class STLWeekly:
    def __init__(self, season_length):
        pass
    def fit(self, ts):
        pass
    def forecast(self, h):
        pass

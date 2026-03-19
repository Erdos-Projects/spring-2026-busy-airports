"""
models.py

Forecasting models for TSA data
"""

import numpy as np
import pandas as pd
from statsmodels.tsa.api import SARIMAX
from busy_airports.harmonic_model import fourier_features

class HarmonicARIMA:
    """
    Harmonic Regression model for forecasting time series data with up to two seasonalities.

    This class implements a SARIMAX model with exogenous Fourier features. This allows
    the user to model two different seasonalities, a 'long' seasonality modeled by the
    Fourier features, and a 'short' seasonality modeled by the SARIMA errors. This
    works especially well when the data contains very few seasons for the 'long'
    seasonality, since the SARIMA models struggles in that situation.
    """

    def __init__(self, harmonic_m, harmonic_k, arima_order, seasonal_order, with_intercept=True):
        """
        Initialize the Harmonic SARIMA model.

        Parameters
        ----------
        harmonic_m : int
            Seasonality of the harmonic part of the model ('long' seasonality).
        harmonic_k : int
            Number of Fourier frequencies to use for the harmonic model.
        arima_order : iterable
            The (p,d,q) order of the SARIMA model.
        seasonal_order : iterable
            The (P,D,Q,s) order of the seasonal component of the SARIMA model. 
        with_intercept : bool
            Whether to include a constant trend in the SARIMA model fit.
        """
        self.harmonic_m = harmonic_m
        self.harmonic_k = harmonic_k
        self.arima_order = arima_order
        self.seasonal_order = seasonal_order
        self.arima_trend = ('c' if with_intercept else 'n')
    
    def fit(self, ts_index, ts_data, maxiter=50):
        """
        Fit the Harmonic SARIMA model to the given time series data.

        Parameters
        ----------
        ts_index : array_like
            Time index information for the time series data, used to determine the Fourier features.
            This is typically specified as an index for each time modulo the 'long' seasonality.
            For example, for daily data with annual seasonality, index ranges from 1 -> 365 for each
            day of the year.
        ts_data : array_like
            Time series data used to fit the model.
        maxiter : int
            Maximum number of iterations to use in fitting statsmodels SARIMAX model

        Returns
        -------
        model_summary
            Summary table of the fitted SARIMAX model.
        """
        X_fourier = fourier_features(ts_index, m = self.harmonic_m, k = self.harmonic_k)
        sarimax_model = SARIMAX(ts_data,
                                exog = X_fourier,
                                order = self.arima_order,
                                seasonal_order = self.seasonal_order,
                                trend = self.arima_trend)
        self.fitted_model = sarimax_model.fit(maxiter=maxiter)
        return self.fitted_model.summary()
    
    def forecast(self, ts_index):
        """
        Forecast the model beyond the fitted dataset

        Parameters
        ----------
        ts_index : array_like
            Time index information for the forecasting window.

        Returns
        -------
        forecast
            Forecasted results, shape (len(ts_index), 1)
        """
        X_fourier = fourier_features(ts_index, m = self.harmonic_m, k = self.harmonic_k)
        results = self.fitted_model.get_forecast(steps = len(ts_index), exog = X_fourier)
        return results.predicted_mean
    
    def conf_int(self, ts_index, alpha=0.05):
        """
        Confidence interval for model forecast.

        Parameters
        ----------
        ts_index : array_like
            Time index information for the forecasting window.
        alpha : float
            The significance level for the confidence interval.

        Returns
        -------
        conf_int
            Confidence interval for forecast, shape (len(ts_index), 2)
        """
        X_fourier = fourier_features(ts_index, m = self.harmonic_m, k = self.harmonic_k)
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

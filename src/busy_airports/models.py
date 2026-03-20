"""
models.py

Forecasting models for TSA data
"""

from tkinter.filedialog import test

import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import STL
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
    
    def forecast(self, ts_index, alpha=0.05):
        """
        Forecast the model beyond the fitted dataset

        Parameters
        ----------
        ts_index : array_like
            Time index information for the forecasting window.
        alpha : float
            The significance level for the confidence interval.

        Returns
        -------
        forecasts : array_like
            Forecast, Upper bound, and lower bound associated with the confidence interval
            for the forecast, each of shape (len(ts_index),).
        """
        X_fourier = fourier_features(ts_index, m = self.harmonic_m, k = self.harmonic_k)
        results = self.fitted_model.get_forecast(steps = len(ts_index), exog = X_fourier)
        ci = results.conf_int(alpha=alpha)  # alpha=alpha → 100*(1-alpha)% CI
        lower_ci = ci.iloc[:, 0]
        upper_ci = ci.iloc[:, 1]
        return results.predicted_mean, lower_ci, upper_ci

class STLArima:
    def __init__(self, season_length, arima_order, seasonal_order):
        """
        Initialize the STL + ARIMA model.

        Parameters
        ----------
        season_length : int
            The length of the seasonal cycle.
        arima_order : iterable
            The (p,d,q) order of the SARIMA model.
        seasonal_order : iterable
            The (P,D,Q,s) order of the seasonal component of the SARIMA model. 
    
        """
        self.arima_order = arima_order
        self.seasonal_order = seasonal_order
        self.season_length = season_length
    def fit(self, ts):
        """Fit the STL + ARIMA model to the given time series data.
    
        Parameters        
        ----------
        ts : array_like
            Time series data used to fit the model.
        """
        stl = STL(ts, period=self.season_length, robust=True)
        stl_fit = stl.fit()
        self.seasonal = stl_fit.seasonal
        self.trend_resid = stl_fit.trend + stl_fit.resid 
        self.model = ARIMA(self.trend_resid, order=self.arima_order, seasonal_order=self.seasonal_order).fit()
    def forecast(self, h, alpha=0.05):
        """
        Forecast the model beyond the fitted dataset
        
        Parameters
        ----------
        h : int
            The number of time steps to forecast beyond the fitted dataset.
        alpha : float
            The significance level for the confidence interval.
        Returns
        -------
        forecasts : array_like
            Forecast, Upper bound, and lower bound associated with the confidence interval for the forecast, each of shape (h,).
        """
        arima_forecast = self.model.get_forecast(steps=h)
        trend_resid_forecast = arima_forecast.predicted_mean
        #confidence intervals for the ARIMA forecast
        ci = arima_forecast.conf_int(alpha=alpha)  # alpha=alpha → 100*(1-alpha)% CI
        lower_ci = ci.iloc[:, 0]
        upper_ci = ci.iloc[:, 1]
        #Tiling and adding seasonal component back to ARIMA forecast
        seasonal_cycle    = self.seasonal.values[-self.season_length:]
        seasonal_forecast = np.tile(seasonal_cycle, int(np.ceil(h / self.season_length)))[:h]
        #final forecasts
        forecasts = trend_resid_forecast + seasonal_forecast
        lower_bound = lower_ci.values + seasonal_forecast
        upper_bound = upper_ci.values + seasonal_forecast
        return forecasts, upper_bound, lower_bound

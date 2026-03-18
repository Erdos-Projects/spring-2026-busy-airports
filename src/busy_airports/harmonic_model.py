"""
harmonic_model.py

Functions for constructing design matrix for Harmonic regression
"""

import numpy as np

def fourier_features(time_seres, m, k=10):
    """
    Create matrix of Fourier features for modeling seasonality

    Parameters
    ----------
    time_series: object
        time series index over which to create Fourier features
    m: int
        seasonality (periodicity of Fourier features)
    k: int
        number of Fourier frequencies to use
    
    Returns
    -------
    X : object
        design matrix of shape (len(time_series), 2*k) containing Fourier features
    """
    X = []
    for i in range(1, k + 1):
        X.append(np.sin(2 * np.pi * i * time_seres / m))
        X.append(np.cos(2 * np.pi * i * time_seres / m))
    return np.column_stack(X)

# Create row matrix of time index feature
def time_index_feature(time_series):
    """
    Create row matrix of time index feature

    Parameters
    ----------
    time_series: object
        time series data over which to create time index feature
    
    Returns
    -------
    X : object
        design matrix of shape (len(time_series), 1) containing overall time index
    """
    return np.arange(len(time_series))

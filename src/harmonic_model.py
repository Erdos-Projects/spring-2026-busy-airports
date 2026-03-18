import numpy as np

# Create matrix of Fourier features for modeling seasonality
def fourier_features(time_seres, m, k=10):
    X = []
    for i in range(1, k + 1):
        X.append(np.sin(2 * np.pi * i * time_seres / m))
        X.append(np.cos(2 * np.pi * i * time_seres / m))
    return np.column_stack(X)

# Create row matrix of time index feature
def time_index_feature(time_series):
    return np.arange(len(time_series))

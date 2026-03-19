"""
metrics.py

Metrics for evaluating effectiveness of models
"""

import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_absolute_percentage_error

def evaluate_forecast(actual, predicted, model_name):
    """
    Evaluate effectiveness of the given forecasting model by calculating metrics

    Parameters
    ----------
    actual: object
        time series containing the actual future data
    predicted: object
        time series containing the forecasted future data
    model_name: str
        name of model used to make prediction
    
    Returns
    -------
    metrics : dict
        dict containing values for each relevant metric
    """
    mae = mean_absolute_error(actual, predicted)
    mape = mean_absolute_percentage_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    #print(f"\n{model_name}")
    #print(f"  MAE:  {mae:,.0f}")
    #print(f"  MAPE: {mape*100:.2f}%")
    #print(f"  RMSE: {rmse:,.0f}")
    return {'mae': mae, 'mape': mape, 'rmse': rmse}

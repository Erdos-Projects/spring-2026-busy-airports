import numpy as np
import pandas as pd

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


#General functions for the timeseries splits we will use for cross validation

def make_rolling_splits(df, date_col, n_splits, step_days):

    #df - pandas DataFrame containing the time series data
    #date_col - name of the column in df that contains the date information
    #n_splits - number of splits to create 
    #step_days - number of days to step by for each split

    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col).reset_index(drop=True)

    # Base is all of 2022 + 2023. Then expand by step_days per split.
    base_end = pd.Timestamp('2023-12-31')

    splits = []
    for i in range(n_splits):
        train_end  = base_end + pd.Timedelta(days=step_days * (i + 1))
        test_start = train_end + pd.Timedelta(days=1)
        test_end   = test_start + pd.Timedelta(days=step_days - 1)

        train_idx = df.index[df[date_col] <= train_end].tolist()
        test_idx  = df.index[
            (df[date_col] >= test_start) & (df[date_col] <= test_end)
        ].tolist()

        splits.append((train_idx, test_idx))

        print(f"Split {i+1}: train → {train_end.date()} | "
              f"test {test_start.date()} → {test_end.date()} "
              f"({len(test_idx)} days)")

    return splits
#Example use:  make_rolling_splits(ord_daily_data, date_col='DateTime', n_splits=5, step_days=90)

def make_rolling_splits_weekly(df, date_col, n_splits, step_weeks, base_weeks=104):
    # df         - pandas DataFrame containing the time series data
    # date_col   - name of the column with weekly period/date info
    # n_splits   - number of splits to create
    # step_weeks - weeks to step by per split (default 13 = 1 quarter)
    # base_weeks - size of the initial training window (default 104 = 2 years)

    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col).reset_index(drop=True)

    splits = []
    for i in range(n_splits):
        train_end_row  = base_weeks + step_weeks * (i + 1) - 1
        test_start_row = train_end_row + 1
        test_end_row   = test_start_row + step_weeks - 1

        train_idx = df.index[df.index <= train_end_row].tolist()
        test_idx  = df.index[
            (df.index >= test_start_row) & (df.index <= test_end_row)
        ].tolist()

        train_end_date  = df[date_col].iloc[train_end_row]  if train_end_row  < len(df) else None
        test_start_date = df[date_col].iloc[test_start_row] if test_start_row < len(df) else None
        test_end_date   = df[date_col].iloc[test_end_row]   if test_end_row   < len(df) else None

        splits.append((train_idx, test_idx))
        print(f"Split {i+1}: train → row {train_end_row} ({train_end_date.date() if train_end_date is not None else 'OOB'}) | "
              f"test rows {test_start_row}–{test_end_row} "
              f"({test_start_date.date() if test_start_date is not None else 'OOB'} → "
              f"{test_end_date.date() if test_end_date is not None else 'OOB'}) "
              f"({len(test_idx)} weeks)")

    return splits

# Example use:
# make_rolling_splits_weekly(df, date_col='datetime', n_splits=5)
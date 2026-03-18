"""
data_splits.py

Functions for Time Series data splits for Cross-Validation
"""

import pandas as pd

def make_rolling_splits(df, date_col, n_splits, step_days):
    """
    Create rolling data splits over daily time series data starting with first two years

    Parameters
    ----------
    df : pd.DataFrame
        pandas DataFrame containing the daily time series data
    date_col : str
        name of the column in df that contains the date information
    n_splits : int
        number of splits to create 
    step_days : int
        number of days to step by for each split
    
    Returns
    -------
    splits : list
        list of train, test splits for each rolling window

    Examples
    --------
    >>> make_rolling_splits(ord_daily_data, date_col='datetime', n_splits=5, step_days=90)
    """

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

def make_rolling_splits_weekly(df, date_col, n_splits, step_weeks, base_weeks=104):
    """
    Create rolling data splits over weekly time series data starting with base number of weeks

    Parameters
    ----------
    df : pd.DataFrame
        pandas DataFrame containing the weekly time series data
    date_col : str
        name of the column in df that contains the weekly date information
    n_splits : int
        number of splits to create
    step_weeks : int
        number of weeks to step by per split
    base_weeks : int
        size of the initial training window (default 104 = 2 years)
    
    Returns
    -------
    splits : list
        list of train, test splits for each rolling window

    Examples
    --------
    >>> make_rolling_splits_weekly(ord_weekly_data, date_col='datetime', n_splits=5, step_weeks=13)
    """

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

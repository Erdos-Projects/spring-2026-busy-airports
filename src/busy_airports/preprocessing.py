"""
preprocessing.py

Functions for preprocessing the TSA throughput data before forecasting
"""

import pandas as pd

def load_data(path):
    """
    Load dataset from CSV file and parse timestamp column.
    
    Parameters
    ----------
    path: str
        path to CSV file containing TSA throughput time series data
    
    Returns
    -------
    df : pd.DataFrame
        pandas DataFrame containing the TSA throughput data with appropriately parsed columns
    """
    df = pd.read_csv(path)

    #cleaning up the column names
    df.columns = [t.partition('(')[0].strip().lower().replace(' ', '_') for t in df.columns]

    #Extracting date info
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['date'] = pd.to_datetime(df['datetime']).dt.date
    df['month'] = pd.to_datetime(df['datetime']).dt.month
    df['week'] = df['datetime'].dt.isocalendar().week.astype(int)

    df = df.drop_duplicates()
    return df

def retrieve_airport_data(df, airport="ORD", frequency='W'):
    """
    Extract time series TSA throughput data for a single airport
    
    Parameters
    ----------
    df : pd.DataFrame
        pandas DataFrame containing the TSA throughput data (obtained from load_data function)
    airport: str
        airport code of airport to extract time series data from (summed over all TSA checkpoints)
    frequency: str
        frequency at which to sample time series data (daily, weekly, or monthly data)
    
    Returns
    -------
    df : pd.DataFrame
        pandas DataFrame containing the TSA throughput time series data for the given airport
    """

    if frequency not in ['D', 'W', 'M']:
        raise ValueError("Invalid frequency. Use 'D' for daily, 'W' for weekly, or 'M' for monthly.")

    #Keep only dataframe of working airport
    df.drop(df[df['airport_code'] != airport].index, inplace=True)

    #Drop cases of zero passengers
    df.drop(df[df['total_passenger_throughput'] == 0].index, inplace=True)

    df['date'] = pd.to_datetime(df['datetime']).dt.date
    df['month'] = pd.to_datetime(df['datetime']).dt.month

    #df = df[['datetime','total_passenger_throughput']]
    #df = df.groupby(by=['date'],as_index=False).sum()
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.groupby(pd.Grouper(key='datetime', freq=frequency))['total_passenger_throughput'].sum().iloc[1:-1].reset_index() 

    #df['week'] = pd.to_datetime(df['datetime']).dt.strftime('%U').astype(int)
    if frequency == 'W':
        df['week'] = df['datetime'].dt.isocalendar().week.astype(int)
    elif frequency == 'M':
        df['month'] = df['datetime'].dt.month.astype(int)
    elif frequency == 'D':
        df['day'] = df['datetime'].dt.dayofyear.astype(int)
    
    return df

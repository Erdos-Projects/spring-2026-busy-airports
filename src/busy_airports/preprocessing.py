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
    df_airport = df[df['airport_code'] == airport]    
    #Drop cases of zero passengers
    df_airport.drop(df_airport[df_airport['total_passenger_throughput'] == 0].index, inplace=True)

    df_airport['date'] = pd.to_datetime(df_airport['datetime']).dt.date
    df_airport['month'] = pd.to_datetime(df_airport['datetime']).dt.month

    #df_airport = df_airport[['datetime','total_passenger_throughput']]
    #df_airport = df_airport.groupby(by=['date'],as_index=False).sum()
    df_airport['datetime'] = pd.to_datetime(df_airport['datetime'])
    df_airport = df_airport.groupby(pd.Grouper(key='datetime', freq=frequency))['total_passenger_throughput'].sum().iloc[1:-1].reset_index() 

    #df_airport['week'] = pd.to_datetime(df_airport['datetime']).dt.strftime('%U').astype(int)
    if frequency == 'W':
        df_airport['week'] = df_airport['datetime'].dt.isocalendar().week.astype(int)
    elif frequency == 'M':
        df_airport['month'] = df_airport['datetime'].dt.month.astype(int)
    elif frequency == 'D':
        df_airport['day'] = df_airport['datetime'].dt.dayofyear.astype(int)
    
    return df_airport

"""
eda.py

Plotting methods for the exploratory data analysis
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#['datetime', 'airport_code', 'airport_name', 'city', 'state','checkpoint', 'total_passenger_throughput', 'date', 'month', 'week']

def plot_airport_data(df, airport="ORD", frequency='D', checkpoint="all"):
    """
    Plot the total passenger throughput data for the given airport(s).

    Parameters
    ----------
    df : pd.DataFrame
        pandas DataFrame containing the TSA throughput time series data
    airport : object
        name of airport or list of airports to plot
    frequency : str
        frequency at which to sample time series data (daily, weekly, or monthly data).
        If multiple frequencies are given, these are plotted together
    checkpoint : str
        name of airport checkpoint or list of checkpoints to plot
    """

    if frequency not in ['H', 'D', 'W', 'M']:
        raise ValueError("Invalid frequency. Use 'H' for hourly, 'D' for daily, 'W' for weekly, or 'M' for monthly.")
    if frequency == 'M':
        frequency = 'MS'

    # Normalize inputs
    if isinstance(airport, str):
        airports = [airport]
    else:
        airports = airport

    freq_names = {'H': 'Hourly', 'D': 'Daily', 'W': 'Weekly', 'MS': 'Monthly'}

    plt.figure(figsize=(15, 6))

    for ap in airports:
        df_airport = df[df['airport_code'] == ap]
        if checkpoint == "all":
            df_query = df_airport.groupby(['datetime'], as_index=False).total_passenger_throughput.sum()
        else:
            df_query = df_airport[df_airport['checkpoint'] == checkpoint]
        if frequency != 'H':
            df_query = (
                df_query
                .groupby(pd.Grouper(key='datetime', freq=frequency))['total_passenger_throughput']
                .sum()
                .reset_index()
            )
        if frequency == 'W':
            df_query = df_query[1:-1].reset_index(drop=True)
        plt.plot(
            df_query['datetime'],
            df_query['total_passenger_throughput'],
            label=ap
        )
    plt.title(
        f'{freq_names[frequency]} TSA Throughput - ' +
        (f'{ap}, ' if len(airports) == 1 else '') +
        (f'Checkpoint {checkpoint}' if checkpoint != "all" else 'All Checkpoints')
    )
    plt.xlabel('Date/Time')
    plt.ylabel('Passenger Throughput')
    plt.legend()
    plt.show()

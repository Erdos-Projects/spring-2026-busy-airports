import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#['datetime', 'airport_code', 'airport_name', 'city', 'state','checkpoint', 'total_passenger_throughput', 'date', 'month', 'week']

def plot_hourly_by_airport_checkpoint(df, checkpoint="10", airport="ORD"):
    df_query = df.query(f'airport_code == "{airport}" and checkpoint == "{checkpoint}"')
    plt.figure(figsize=(15, 6))
    plt.plot(df_query['datetime'], df_query['total_passenger_throughput'])
    plt.title(f'Hourly TSA Throughput - {airport} Checkpoint {checkpoint}')
    plt.xlabel('Date/Time')
    plt.ylabel('Passenger Throughput')
    plt.show()

def plot_daily_by_airport_checkpoint(df, checkpoint="10", airport="ORD"):
    df_query = df.query(f'airport_code == "{airport}" and checkpoint == "{checkpoint}"')
    df_grouped = df_query.groupby(pd.Grouper(key='datetime', freq='D'))['total_passenger_throughput'].sum()
    plt.figure(figsize=(15, 6))
    plt.plot(df_grouped.index, df_grouped)
    plt.title(f'Daily TSA Throughput - {airport} Checkpoint {checkpoint}')
    plt.xlabel('Date/Time')
    plt.ylabel('Passenger Throughput')
    plt.show()
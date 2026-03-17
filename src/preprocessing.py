import pandas as pd


def load_data(path):
    """
    Load dataset from CSV file and parse timestamp column.
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

def retrieve_airport_data(df, airport="ORD"):
    #Keep only dataframe of working airport
    df.drop(df[df['airport_code'] != airport].index, inplace=True)

    #Drop cases of zero passangers
    df.drop(df[df['total_passenger_throughput'] == 0].index, inplace=True)

    df['date'] = pd.to_datetime(df['datetime']).dt.date
    df['month'] = pd.to_datetime(df['datetime']).dt.month

    #df = df[['datetime','total_passenger_throughput']]
    #df = df.groupby(by=['date'],as_index=False).sum()
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.groupby(pd.Grouper(key='datetime', freq='W'))['total_passenger_throughput'].sum().iloc[1:-1].reset_index() 

    #df['week'] = pd.to_datetime(df['datetime']).dt.strftime('%U').astype(int)
    df['week'] = df['datetime'].dt.isocalendar().week.astype(int)
    
    return df


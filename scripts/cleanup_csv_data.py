#!/usr/bin/env python3
"""
cleanup_csv_data.py

Clean up TSA throughput data after extraction from PDF files
"""

import glob
import os
import csv
import numpy as np
import pandas as pd
from pandas.errors import ParserError

# Directory containing all CSV files to post-process
DATA_DIRECTORY = 'tsa-throughput-raw-data'
# Path to output file to write cleaned data
OUTPUT_FILEPATH = 'tsa-throughput-data-complete.csv'

def clean_csv_data(csv_path):
    """
    Read CSV data from the given file, clean up data and return as a DataFrame

    Parameters
    ----------
    csv_path : str
        Path to the csv file to read data from

    Returns
    -------
    df : pd.DataFrame
        DataFrame containing the cleaned up TSA throughput data
    """
    print(f"Cleaning data from {csv_path}")

    # Read raw csv file data
    try:
        df = pd.read_csv(csv_path)
    except ParserError:
        df = normalize_to_9_columns(csv_path)
    
    # Remove the extra NaN column in files which have 9 columns instead of 8
    if len(df.columns) == 9:
        df = remove_extra_column(df)

    # Remove any extra rows containing header info
    if df.iloc[:,0].value_counts().get('Date', 0) > 0:
        df = df[df.iloc[:,0] != 'Date']
    
    # Rename headers appropriately
    df.columns = ['Date', 'Hour', 'Airport Code', 'Airport Name', 'City', 'State', 'Checkpoint', 'Total Passenger Throughput']

    # Delete columns where checkpoint and passenger volume are NaN (pdf conversion artifacts)
    df = df.dropna(subset=['Checkpoint', 'Total Passenger Throughput'], how='any')
    # Forward fill the NaN values in Date and Hour columns
    df[['Date', 'Hour']] = df[['Date', 'Hour']].ffill()
    # Forward fill the NaN values in Airport Information
    df[['Airport Code', 'Airport Name', 'City', 'State']] = df[['Airport Code', 'Airport Name', 'City', 'State']].ffill()

    # Replace line breaks with spaces
    df = df.replace('\n', ' ', regex=True)

    # Return the cleaned data
    return df

def remove_extra_column(df):
    """
    When TSA data has 9 columns instead of 8, identify the extra column and remove it

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with 9 columns instead of 8

    Returns
    -------
    df_fixed : pd.DataFrame
        DataFrame containing the TSA data with 8 columns (extra column removed)
    """
    # Shift data so that NaN column is always the last one
    df_fixed = fix_extra_column_fast(df)
    if not df.iloc[:, -1].isna().all():
        print(f"Unexpected non-NaN value found")
        return None
    # Drop last column of NaNs
    df_fixed = df_fixed.iloc[:, :-1]
    return df_fixed

def fix_extra_column_fast(df):
    """
    Go through rows of DataFrame and shift NaN values into the 9th column

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with 9 columns

    Returns
    -------
    df_fixed : pd.DataFrame
        DataFrame with data shifted so that last column is NaN
    """
    df = df.copy()
    values = df.values
    n_cols = values.shape[1]

    for i in range(values.shape[0]):
        if pd.isna(values[i, -1]):
            continue

        nan_positions = np.where(pd.isna(values[i]))[0]
        if len(nan_positions) == 0:
            continue

        rightmost_nan = nan_positions.max()

        values[i, rightmost_nan:n_cols-1] = values[i, rightmost_nan+1:n_cols]
        values[i, -1] = np.nan

    return pd.DataFrame(values, columns=df.columns)


def normalize_to_9_columns(csv_path):
    """
    When CSV data has rows with inconsistent number of columns (8 and 9), fill in bad rows with NaN

    Parameters
    ----------
    csv_path : str
        Path to the csv file to containing rows with inconsistent number of columns

    Returns
    -------
    df : pd.DataFrame
        DataFrame containing the CSV data with 9 columns in every row
    """
    rows = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if len(row) == 0:
                continue
            # Convert empty strings to NaN
            row = [col.strip() if col.strip() != "" else np.nan for col in row]
            # Append NaN values to rows with only 8 entries
            if len(row) == 8:
                row.append(np.nan)
            elif len(row) == 9:
                pass
            else:
                print(f"Unexpected column count ({len(row)}) at line {i}: {row}")
                continue
            rows.append(row)
    # Place the consistent rows into the DataFrame (ignoring header row)
    df = pd.DataFrame(rows[1:])
    return df

def main():
    """
    Main execution function.
    """
    df_list = []

    # Clean TSA data from all CSV files in the specified directory
    for csv_path in glob.glob(os.path.join(DATA_DIRECTORY, '*.csv')):
        clean_df = clean_csv_data(csv_path)
        if clean_df:
            df_list.append(clean_df)
    # Combine all tables into a single table for the entire TSA dataset
    combined_df = pd.concat(df_list, ignore_index=True)
    # Convert Date column from string to datetime object
    combined_df['Date'] = pd.to_datetime(combined_df['Date'].replace(r"\s+", "", regex=True))
    # Sort data by time and airport
    combined_df.sort_values(by=['Date', 'Hour', 'Airport Code'], inplace=True)
    # Write to output file
    combined_df.to_csv(OUTPUT_FILEPATH, index=None, header=True)
    
    print(f"Finished cleaning and combining all CSV files in {DATA_DIRECTORY}.")

if __name__ == "__main__":
    main()
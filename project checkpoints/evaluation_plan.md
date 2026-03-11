# Model Evaluation Plan

## Unit of Analysis

For this project, we will be using [TSA Passenger Throughput Data](https://catalog.data.gov/dataset/tsa-foia-reading-room-weekly-passenger-throughput-data) provided by the Transportation Security Administration. The data were extracted from a series of PDFs and post-processed to remove formatting inconsistencies and anomalies.

The raw dataset reports the number of passengers passing through *each TSA checkpoint* at *every U.S. airport* on an *hourly* basis. Across four years of data (2022–2025), this results in approximately 11 million rows.

To simplify the prediction task, we aggregate the data by airport and day. Specifically, we sum passenger counts across all checkpoints within each airport and across all hours within each day. The resulting dataset contains the **total daily passenger throughput for each U.S. airport**.

For the initial phase of modeling, we focus on a single airport: **Chicago O’Hare International Airport (ORD)**. ORD is one of the largest aviation hubs in the United States and exhibits relatively stable passenger throughput during the period of interest. Our objective is to predict the **total daily passenger throughput at ORD for future dates**.

## Data Splitting

Because the dataset is a time series, care must be taken to prevent information leakage from the future into the training data. We therefore use a standard time series split:

- **Training Set**: 2022-2024
- **Testing Set**: 2025

Using multiple years of training data allows the model to learn annual seasonal patterns while preserving a full year of unseen data for evaluation.

For cross-validation, we will use rolling time-series splits that train on two to three years of data at a time. This approach allows us to evaluate model stability while preserving temporal ordering. If the model primarily captures short-term structure (e.g., daily or monthly patterns), smaller rolling windows can also be explored.

## Stress Tests

When the analysis is later extended to additional U.S. airports, we will check for extreme observations that could bias model predictions. These may include airport closures, severe weather disruptions, or emergency events that produce abnormal spikes or drops in TSA passenger counts.

We will also remove *February 29, 2024*, since leap days disrupt the yearly seasonality assumed by several forecasting models.

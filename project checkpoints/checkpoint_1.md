# Problem Definition, Data Gathering, and Stakeholders

## Problem Definition

Airports in the United States serve as critical transportation hubs. handling hundreds of millions of travelers each year. One of the most significant bottlenecks in air travel is the TSA security checkpoint. For TSA directors, accurately forecasting passenger volume is essential for effective staffing and resource allocation. Reliable predictions of hourly throughput can also help travelers anticipate longer-than-usual wait times and plan accordingly.

The goal of this project is to develop a predictive model for passenger throughput at TSA security checkpoints. We will begin by building and validating the model for a single airport to establish feasibility and performance. The model will forecast total passenger volume over selected future timescales (e.g. daily, weekly totals) with the flexibility to evaluate which forecasting window (days, weeks, or potentially months) yields the most reliable results. In addition to point forecasts, the model will provide uncertainty estimates to quantify confidence in its predictions.

If the single-airport model performs well, we plan to extend the framework to multiple US airports using a combined time series and regression approach. This expanded model will incorporate both temporal features and static airport characteristics (e.g., geographic location, airport size, regional demographics) to generalize predictions across locations.

This project focuses exclusively on forecasting passenger throughput at TSA checkpoints within the United States. It does not aim to predict flight delays, overall airport congestion beyond security lines, or traffic at airports outside the US.

## Data Gathering and Assessment

The data for this project comes from the following publicly available data sets:
1. [TSA Hourly Passenger Throughput](https://catalog.data.gov/dataset/tsa-foia-reading-room-weekly-passenger-throughput-data)

Contains the total number of passengers passing through TSA checkpoints each hour at every US airport (TSA).

This data is separated into PDF files for each week of the given year. In order to use this data, all of the PDF files for the years of interest need to be downloaded and processed into CSV column data. For the years of data which we will use (2022-2025), this requires processing about 200 PDF files, each with about 1000 pages of tabulated data.

2. [General airport information (US Airports only)](https://geodata.bts.gov/datasets/usdot::aviation-facilities/about)

Contains general information about US airports such as geographic location, altitude, and size information (US Bureau of Transportation Statistics).

This data set can be used to assign static (time-independent) features to the airports, which may help determine how trends in passenger volume change with airport location. This is relevant for the second phase of the project dealing with the combined model for all airports.

3. [City and Towns Population totals](https://www.census.gov/data/tables/time-series/demo/popest/2020s-total-cities-and-towns.html)

Contains estimated population totals of every city and town in the United States (US Census).

This data set can be used along with the previous data set to supply more information for training the larger model across different airports. The city or town population near the airport is likely correlated with passenger volume through that airport.

## Key Performance Indicators (KPIS)

**Primary KPI**
- Root-Mean-Square Error (RMSE): Project success will be measured based on how well the model is able to predict future passenger volume in the given airport. This is calculated as the RMSE between the predicted passenger volume and the actual passenger volume in the testing dataset. This error will be averaged over the entire year of test data.

**Secondary KPIs**
- Mean Absolute Percentage Error (MAPE): Less sensitive to large outliers and evaluates prediction error as a percentage of actual passenger volume. This allows performance comparisons across airports of different sizes (e.g., regional vs. major hubs).
- Prediction Interval Coverage Probability (PICP): Measures the percentage of actual passenger volumes that fall within our model’s predicted confidence intervals. This assesses whether the model’s stated uncertainty levels are well-calibrated.
- Generalization Performance Across Airports: If expanded nationally, we should evaluate how well a model trained on one set of airports performs on previously unseen airports.
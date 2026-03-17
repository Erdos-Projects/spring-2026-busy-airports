# spring-2026-busy-airports
## Air Traffic Imbalances: Identifying Airports That Are Busier Than Expected

**Team members**: [David Friedenberg](https://github.com/), [Agniva Dasgupta](https://github.com/), [Charuhas Shiveshwarkar](https://github.com/), [Ivan Caro Terrazas](https://github.com/icaromx), [Ahmad Shamloumehr](https://github.com/)

# Table of Contents
1. [Introduction](#Introduction)
2. [Dataset Generation](#Dataset-Generation)
3. [Exploratory Data Analysis](#Exploratory-Data-Analysis)
4. [Modeling Approach](#Modeling-Approach)
5. [Results](#Results)
6. [Future Work](#Future-Work)
7. [Description of Repository](#Description-of-Repository)

## Introduction
Airports in the United States serve as critical transportation hubs. handling hundreds of millions of travelers each year. One of the most significant bottlenecks in air travel is the TSA security checkpoint. For TSA directors, accurately forecasting passenger volume is essential for effective staffing and resource allocation. Reliable predictions of hourly throughput can also help travelers anticipate longer-than-usual wait times and plan accordingly.

**Objective**: The goal of this project is to develop a predictive model for passenger throughput at TSA security checkpoints. We will begin by building and validating the model for a single airport to establish feasibility and performance. The model will forecast total passenger volume over selected future timescales (e.g. daily, weekly totals) with the flexibility to evaluate which forecasting window (days, weeks, or potentially months) yields the most reliable results. In addition to point forecasts, the model will provide uncertainty estimates to quantify confidence in its predictions.

If the single-airport model performs well, we plan to extend the framework to multiple US airports using a combined time series and regression approach. This expanded model will incorporate both temporal features and static airport characteristics (e.g., geographic location, airport size, regional demographics) to generalize predictions across locations.

## Dataset Generation
Dataset Source: [TSA Hourly Passenger Throughput](https://catalog.data.gov/dataset/tsa-foia-reading-room-weekly-passenger-throughput-data)

## Exploratory Data Analysis

## Modeling Approach

## Results

## Future Work

## Description of Repository
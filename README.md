# Busy Airports: Predicting TSA Traffic at Major U.S. Airports

![ohare](./images/ohare.jpg "Chicago O'Hare International Airport")

**Team members**: [David Friedenberg](https://github.com/friedenberg12), [Agniva Dasgupta](https://github.com/), [Charuhas Shiveshwarkar](https://github.com/), [Ivan Caro Terrazas](https://github.com/icaromx), [Ahmad Shamloumehr](https://github.com/)

---
# Table of Contents
1. [Introduction](#Introduction)
2. [Dataset Generation](#Dataset-Generation)
3. [Exploratory Data Analysis](#Exploratory-Data-Analysis)
4. [Modeling Approach](#Modeling-Approach)
5. [Results](#Results)
6. [Future Work](#Future-Work)
7. [Description of Repository](#Description-of-Repository)
8. [Repository Structure](#Repository-Structure)
9. [How To Run The Project](#How-To-Run-The-Project)

---
## Introduction
Airports in the United States serve as critical transportation hubs. handling hundreds of millions of travelers each year. One of the most significant bottlenecks in air travel is the TSA security checkpoint. For TSA directors, accurately forecasting passenger volume is essential for effective staffing and resource allocation. Reliable predictions of daily throughput can also help travelers anticipate longer-than-usual wait times and plan accordingly.

**Objective**: The goal of this project is to develop a predictive model for passenger throughput at TSA security checkpoints. We will begin by building and validating the model for a single airport to establish feasibility and performance. The model will forecast total passenger volume over selected future timescales (e.g. daily, weekly totals) with the flexibility to evaluate which forecasting window (days, weeks, or potentially months) yields the most reliable results. Once the single-airport model performs well, we can extend the framework to multiple US airports to test robustness of the modeling methods.

---
## Dataset Generation
Dataset Source: [TSA Hourly Passenger Throughput](https://catalog.data.gov/dataset/tsa-foia-reading-room-weekly-passenger-throughput-data)

The data for this project comes from the publically available dataset listed above. This data is separated into PDF files containing data for each individual week over the past 4 years. In order to use this data, all of these PDF files need to be downloaded and processed into tabulated CSV data. For the years of data which we use in our analysis (2022-2025), this requires processing about 200 PDF files, each with about 1000 pages of tabulated data.

The scripts for reading the PDF files, identifying tabulated data, processing these tables into CSV files, and cleaning up the resulting data are provided in the `scripts/` directory. Note that the original PDF files are not included in this repository due to storage limitations. These can be found at the public webpage above.

---
## Exploratory Data Analysis

---
## Modeling Approach

---
## Results

---
## Future Work

---
## Description of Repository

---
## Repository Structure

```
spring-2026-busy-airports/
│
├── data/
│   └── tsa-throughput-data-complete.csv
│
├── src/
│   └── preprocessing.py
│   └── other.py
|
├── scripts/
│   └── cleanup_csv_data.py
│   └── extract_pdf_data.py
│
├── busy_airports.ipynb
│
├── README.md
└── environment.yml
```

---

## How To Run The Project

1. **Clone the repository**

```bash
git clone https://github.com/Erdos-Projects/spring-2026-busy-airports.git
cd spring-2026-busy-airports
```

2. **Install the required dependencies**

Using Anaconda
```bash
conda env create -f environment.yml
conda activate busy_airports
```

3. **Open the notebook and run the cells sequentially**

Open the file `busy_airports.ipynb` and execute the cells from top to bottom.

---

# spring-2026-busy-airports
## Air Traffic Imbalances: Identifying Airports That Are Busier Than Expected

**Team members**: *David Friedenberg, Agniva Dasgupta, Charuhas Shiveshwarkar, Ivan Caro Terrazas, Ahmad Shamloumehr*

**Problem**: Airports in the United States serve as critical transportation hubs. handling hundreds of millions of travelers each year. One of the most significant bottlenecks in air travel is the TSA security checkpoint. For TSA directors, accurately forecasting passenger volume is essential for effective staffing and resource allocation. Reliable predictions of hourly throughput can also help travelers anticipate longer-than-usual wait times and plan accordingly.

**Objective**: The goal of this project is to develop a predictive model for passenger throughput at TSA security checkpoints. We will begin by building and validating the model for a single airport to establish feasibility and performance. The model will forecast total passenger volume over selected future timescales (e.g. daily, weekly totals) with the flexibility to evaluate which forecasting window (days, weeks, or potentially months) yields the most reliable results. In addition to point forecasts, the model will provide uncertainty estimates to quantify confidence in its predictions.

If the single-airport model performs well, we plan to extend the framework to multiple US airports using a combined time series and regression approach. This expanded model will incorporate both temporal features and static airport characteristics (e.g., geographic location, airport size, regional demographics) to generalize predictions across locations.

**Data Sources**:
1. [TSA Hourly Passenger Throughput](https://catalog.data.gov/dataset/tsa-foia-reading-room-weekly-passenger-throughput-data)
2. [General airport information (US Airports only)](https://geodata.bts.gov/datasets/usdot::aviation-facilities/about)
3. [City and Towns Population totals](https://www.census.gov/data/tables/time-series/demo/popest/2020s-total-cities-and-towns.html)
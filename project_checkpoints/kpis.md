# Key Performance Indicators (KPIS)

## Primary KPI
- Root-Mean-Square Error (RMSE): Project success will be measured based on how well the model is able to predict future passenger volume in the given airport. This is calculated as the RMSE between the predicted passenger volume and the actual passenger volume in the testing dataset. This error will be averaged over the entire year of test data.

## Secondary KPIs
- Mean Absolute Percentage Error (MAPE): Less sensitive to large outliers and evaluates prediction error as a percentage of actual passenger volume. This allows performance comparisons across airports of different sizes (e.g., regional vs. major hubs).
- Prediction Interval Coverage Probability (PICP): Measures the percentage of actual passenger volumes that fall within our model’s predicted confidence intervals. This assesses whether the model’s stated uncertainty levels are well-calibrated.
- Generalization Performance Across Airports: If expanded nationally, we should evaluate how well a model trained on one set of airports performs on previously unseen airports.
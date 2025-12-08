# Air Quality Prediction Model Results (2020)

## Model Configuration

- **Model Type:** Lasso Regression (L1 Regularization)
- **Cross-Validation:** 5-fold
- **Test Set Size:** 20%
- **Random Seed:** 3963998377

## Features Used

- total_population
- hispanic_percentage
- poverty_rate
- diploma_rate
- median_income
- black_or_african_american_percentage

---

## PM2.5 (Parameter Code: 88101)

**Dataset Size:** 619 records

### Model Training

- **Optimal alpha (CV):** 0.017525
- **Non-zero coefficients:** 6 / 6

### Performance Metrics

**Target Variable Statistics:**
- Mean: 7.6950
- Std Dev: 2.5918
- Range: [2.4825, 26.4368]

| Metric | Training Set | Test Set |
|--------|--------------|----------|
| MSE    | 5.645888      | 3.174828   |
| RMSE   | 2.3761      | 1.7818   |
| NRMSE (% of mean) | 30.88%      | 23.16%   |
| R²     | 0.1578      | 0.0678   |

### Feature Coefficients

| Feature | Coefficient |
|---------|-------------|
| total_population | 0.456644 |
| hispanic_percentage | 0.404597 |
| poverty_rate | -0.085977 |
| diploma_rate | -0.791661 |
| median_income | 0.244248 |
| black_or_african_american_percentage | 0.099777 |

**Model saved to:** `models/2020/lasso_model_PM2.5_2020.pkl`

---

## Ozone (Parameter Code: 44201)

**Dataset Size:** 756 records

### Model Training

- **Optimal alpha (CV):** 0.000412
- **Non-zero coefficients:** 1 / 6

### Performance Metrics

**Target Variable Statistics:**
- Mean: 0.0288
- Std Dev: 0.0055
- Range: [0.0076, 0.0539]

| Metric | Training Set | Test Set |
|--------|--------------|----------|
| MSE    | 0.000027      | 0.000041   |
| RMSE   | 0.0052      | 0.0064   |
| NRMSE (% of mean) | 18.21%      | 22.30%   |
| R²     | 0.0754      | 0.0342   |

### Feature Coefficients

| Feature | Coefficient |
|---------|-------------|
| total_population | 0 (eliminated) |
| hispanic_percentage | 0 (eliminated) |
| poverty_rate | 0 (eliminated) |
| diploma_rate | 0 (eliminated) |
| median_income | 0 (eliminated) |
| black_or_african_american_percentage | -0.001140 |

**Model saved to:** `models/2020/lasso_model_Ozone_2020.pkl`

---

## NO2 (Parameter Code: 42602)

**Dataset Size:** 259 records

### Model Training

- **Optimal alpha (CV):** 0.207872
- **Non-zero coefficients:** 4 / 6

### Performance Metrics

**Target Variable Statistics:**
- Mean: 6.2224
- Std Dev: 3.9655
- Range: [0.5552, 19.0905]

| Metric | Training Set | Test Set |
|--------|--------------|----------|
| MSE    | 8.873828      | 10.942027   |
| RMSE   | 2.9789      | 3.3079   |
| NRMSE (% of mean) | 47.87%      | 53.16%   |
| R²     | 0.4330      | 0.3700   |

### Feature Coefficients

| Feature | Coefficient |
|---------|-------------|
| total_population | 1.117671 |
| hispanic_percentage | 1.300508 |
| poverty_rate | 0 (eliminated) |
| diploma_rate | 0.966641 |
| median_income | 0 (eliminated) |
| black_or_african_american_percentage | 0.828692 |

**Model saved to:** `models/2020/lasso_model_NO2_2020.pkl`

---


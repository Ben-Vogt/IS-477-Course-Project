import plotly.express as px
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LassoCV
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import joblib

def train_multilinear_predictor(year):
    """
    Train a multilinear regression model to predict air quality based on ACS data.
    
    Parameters:
    -----------
    year : int
        Year to train the model for
    
    Returns:
    None
    """
    
    # Load integrated data
    integrated_path = f"data/integrated_data/integrated_data_{year}.csv"
    
    if not os.path.exists(integrated_path):
        raise FileNotFoundError(f"Integrated data file not found: {integrated_path}")
    
    data = pd.read_csv(integrated_path)

    # Create derived features
    data['total_population'] = data['B01003 - Estimate!!Total']
    data['hispanic_percentage'] = data["B03003 - Estimate!!Total:!!Hispanic or Latino"] / data['B03003 - Estimate!!Total:']
    data['poverty_rate'] = data['B17001 - Estimate!!Total:!!Income in the past 12 months below poverty level:'] / data['B17001 - Estimate!!Total:']
    data['diploma_rate'] = (data['B15003 - Estimate!!Total:!!Regular high school diploma'] + 
                         data['B15003 - Estimate!!Total:!!Bachelor\'s degree'] + 
                         data['B15003 - Estimate!!Total:!!Master\'s degree'] + data['B15003 - Estimate!!Total:!!Doctorate degree'] + data['B15003 - Estimate!!Total:!!Professional school degree']) / data['B15003 - Estimate!!Total:']
    data['median_income'] = data['B19013 - Estimate!!Median household income in the past 12 months (in 2020 inflation-adjusted dollars)']
    data['black_or_african_american_percentage'] = data['B02001 - Estimate!!Total:!!Black or African American alone'] / data['B02001 - Estimate!!Total:']

    feature_cols = [
        'total_population', 'hispanic_percentage', 'poverty_rate', 'diploma_rate',
        'median_income', 'black_or_african_american_percentage']
    
    # Parameter codes and names
    parameters = {
        '88101': 'PM2.5',
        '44201': 'Ozone',
        '42602': 'NO2'
    }
    
    if not os.path.exists(f"models/{year}"):
        os.makedirs(f"models/{year}")
    
    # Open results file for writing
    results_file = open(f"artifacts/results_{year}.md", "w", encoding="utf-8")
    results_file.write(f"# Air Quality Prediction Model Results ({year})\n\n")
    results_file.write("## Model Configuration\n\n")
    results_file.write("- **Model Type:** Lasso Regression (L1 Regularization)\n")
    results_file.write("- **Cross-Validation:** 5-fold\n")
    results_file.write("- **Test Set Size:** 20%\n")
    results_file.write(f"- **Random Seed:** 3963998377\n\n")
    results_file.write("## Features Used\n\n")
    for feature in feature_cols:
        results_file.write(f"- {feature}\n")
    results_file.write("\n---\n\n")
    
    # Train one model for each pollutant
    for param_code, param_name in parameters.items():
        print(f"Training model for {param_name}...")
        
        param_data = data[data['parameter_code'] == int(param_code)].copy()
        
        if len(param_data) == 0:
            results_file.write(f"## {param_name} (Parameter Code: {param_code})\n\n")
            results_file.write("**No data found for this parameter. Skipped.**\n\n---\n\n")
            continue
        
        results_file.write(f"## {param_name} (Parameter Code: {param_code})\n\n")
        results_file.write(f"**Dataset Size:** {len(param_data)} records\n\n")
        
        X = param_data[feature_cols]
        y = param_data['mean']
        
        # Test train split with random seed. Test size is 20%
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=3963998377)
        
        # Standardize features for regularized regression
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train Lasso regression model with cross-validation
        model = LassoCV(cv=5, random_state=3963998377, n_jobs=-1)
        model.fit(X_train_scaled, y_train)
        
        results_file.write(f"### Model Training\n\n")
        results_file.write(f"- **Optimal alpha (CV):** {model.alpha_:.6f}\n")
        results_file.write(f"- **Non-zero coefficients:** {(model.coef_ != 0).sum()} / {len(model.coef_)}\n\n")
        
        y_train_pred = model.predict(X_train_scaled)
        y_test_pred = model.predict(X_test_scaled)
        train_mse = mean_squared_error(y_train, y_train_pred)
        train_rmse = train_mse ** 0.5
        train_r2 = r2_score(y_train, y_train_pred)
        test_mse = mean_squared_error(y_test, y_test_pred)
        test_rmse = test_mse ** 0.5
        test_r2 = r2_score(y_test, y_test_pred)
        
        # Calculate relative metrics for context
        y_mean = y_train.mean()
        y_std = y_train.std()
        train_nrmse = (train_rmse / y_mean) * 100  # Normalized RMSE as percentage of mean
        test_nrmse = (test_rmse / y_mean) * 100
        
        results_file.write("### Performance Metrics\n\n")
        results_file.write(f"**Target Variable Statistics:**\n")
        results_file.write(f"- Mean: {y_mean:.4f}\n")
        results_file.write(f"- Std Dev: {y_std:.4f}\n")
        results_file.write(f"- Range: [{y_train.min():.4f}, {y_train.max():.4f}]\n\n")
        
        results_file.write("| Metric | Training Set | Test Set |\n")
        results_file.write("|--------|--------------|----------|\n")
        results_file.write(f"| MSE    | {train_mse:.6f}      | {test_mse:.6f}   |\n")
        results_file.write(f"| RMSE   | {train_rmse:.4f}      | {test_rmse:.4f}   |\n")
        results_file.write(f"| NRMSE (% of mean) | {train_nrmse:.2f}%      | {test_nrmse:.2f}%   |\n")
        results_file.write(f"| R²     | {train_r2:.4f}      | {test_r2:.4f}   |\n\n")
        
        # Write feature coefficients
        results_file.write("### Feature Coefficients\n\n")
        results_file.write("| Feature | Coefficient |\n")
        results_file.write("|---------|-------------|\n")
        for feature, coef in zip(feature_cols, model.coef_):
            if coef != 0:
                results_file.write(f"| {feature} | {coef:.6f} |\n")
            else:
                results_file.write(f"| {feature} | 0 (eliminated) |\n")
        results_file.write("\n")
        
        # Save the model
        joblib.dump(model, f"models/{year}/lasso_model_{param_name}_{year}.pkl")
        results_file.write(f"**Model saved to:** `models/{year}/lasso_model_{param_name}_{year}.pkl`\n\n")
        results_file.write("---\n\n")
    
    results_file.close()
    print(f"\nResults saved to artifacts/results_{year}.md")

def draw_maps(year):
    """
    Generate choropleth maps showing predicted vs actual air quality levels.
    
    Parameters:
    -----------
    year : int
        Year to generate maps for
    
    Returns:
    None
    """
    
    # Load integrated data
    integrated_path = f"data/integrated_data/integrated_data_{year}.csv"
    
    if not os.path.exists(integrated_path):
        raise FileNotFoundError(f"Integrated data file not found: {integrated_path}")
    
    data = pd.read_csv(integrated_path)

    # Create derived features
    data['total_population'] = data['B01003 - Estimate!!Total']
    data['hispanic_percentage'] = data["B03003 - Estimate!!Total:!!Hispanic or Latino"] / data['B03003 - Estimate!!Total:']
    data['poverty_rate'] = data['B17001 - Estimate!!Total:!!Income in the past 12 months below poverty level:'] / data['B17001 - Estimate!!Total:']
    data['diploma_rate'] = (data['B15003 - Estimate!!Total:!!Regular high school diploma'] + 
                         data['B15003 - Estimate!!Total:!!Bachelor\'s degree'] + 
                         data['B15003 - Estimate!!Total:!!Master\'s degree'] + data['B15003 - Estimate!!Total:!!Doctorate degree'] + data['B15003 - Estimate!!Total:!!Professional school degree']) / data['B15003 - Estimate!!Total:']
    data['median_income'] = data['B19013 - Estimate!!Median household income in the past 12 months (in 2020 inflation-adjusted dollars)']
    data['black_or_african_american_percentage'] = data['B02001 - Estimate!!Total:!!Black or African American alone'] / data['B02001 - Estimate!!Total:']

    # Define features
    feature_cols = [
        'total_population', 'hispanic_percentage', 'poverty_rate', 'diploma_rate',
        'median_income', 'black_or_african_american_percentage']
    
    # Parameter codes and names
    parameters = {
        '88101': 'PM2.5',
        '44201': 'Ozone',
        '42602': 'NO2'
    }
    
    for param_code, param_name in parameters.items():
        print(f"Generating maps for {param_name}...")
        
        # Load model and scaler
        model_path = f"models/{year}/lasso_model_{param_name}_{year}.pkl"
        scaler_path = f"models/{year}/scaler_{param_name}_{year}.pkl"
        
        if not os.path.exists(model_path) or not os.path.exists(scaler_path):
            print(f"Model or scaler not found for {param_name}. Skipping map generation.")
            continue
        
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        
        # Filter data for this specific parameter
        param_data = data[data['parameter_code'] == int(param_code)].copy()
        
        if len(param_data) == 0:
            print(f"No data found for {param_name}. Skipping map generation.")
            continue
        
        # Create FIPS code from state and county codes
        param_data['fips'] = param_data['state_code'].astype(str).str.zfill(2) + param_data['county_code'].astype(str).str.zfill(3)
        
        # Prepare features
        X = param_data[feature_cols]
        X_scaled = scaler.transform(X)
        
        # Make predictions
        param_data['predicted_mean'] = model.predict(X_scaled)
        
        # Create maps directory
        if not os.path.exists(f"maps/{year}"):
            os.makedirs(f"maps/{year}")
        
        # Create choropleth maps
        fig_actual = px.choropleth(param_data,
                                   geojson="https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json",
                                   locations='fips',
                                   color='mean',
                                   color_continuous_scale="Viridis",
                                   scope="usa",
                                   title=f'Actual {param_name} Levels ({year})')
        fig_actual.write_html(f"maps/{year}/actual_{param_name}_{year}.html")
        
        fig_predicted = px.choropleth(param_data,
                                      geojson="https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json",
                                      locations='fips',
                                      color='predicted_mean',
                                      color_continuous_scale="Viridis",
                                      scope="usa",
                                      title=f'Predicted {param_name} Levels ({year})')
        fig_predicted.write_html(f"maps/{year}/predicted_{param_name}_{year}.html")
        
        print(f"Maps saved to maps/{year}/")

if __name__ == "__main__":
    train_multilinear_predictor(2020)
    draw_maps(2020)
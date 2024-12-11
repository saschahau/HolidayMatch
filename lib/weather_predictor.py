import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import root_mean_squared_error

@st.cache_data
def get_weather_data():
    """
    Get weather data from the CSV file.
    
    returns: A DataFrame containing the weather data.
    """
    return pd.read_csv("data/hist-weather-zrh.csv")

def prepare_data(df):
    """
    Prepare the weather data for training a model.

    :param df: The DataFrame containing the weather data.

    returns: The cleaned and prepared DataFrame.
    """
    # Rename columns to lowercase
    df.columns = df.columns.str.lower()

    # Convert date column to datetime
    df.date = pd.to_datetime(df.date)
    df.set_index("date", inplace=True)
    df.sort_index(inplace=True)

    # Drop columns that are not needed
    df.drop(columns=["name", "station", "latitude", "longitude", "elevation"], inplace=True)

    # Fill missing values with the previous value
    # This is a simple way to fill missing values in time series data.
    # In practice, more sophisticated methods like interpolation or using a model to predict missing values can be used.
    # For simplicity, we will use forward fill (ffill) here.
    df = df.ffill()

    return df

def create_features(df):
    """
    Create features for the weather data.

    This function adds additional features to the DataFrame that can help the model make better predictions
    based on the cyclical nature of some features like month and day of year. This is a common technique used in time series forecasting.

    :param df: The DataFrame containing the weather data.

    returns: The DataFrame with additional features.
    """
    # Add features for day of year, day of month, month, and year
    # These features can help the model capture seasonal patterns in the data.
    # For example, the average temperature may vary based on the month or day of the year.
    df["day_of_year"] = df.index.dayofyear
    df["day_of_month"] = df.index.day
    df["month"] = df.index.month
    df["year"] = df.index.year

    # Add sine and cosine features for month and day of year
    # This is a common technique to encode cyclical features.
    # It allows the model to capture the periodic nature of the data.
    # For example, the month of the year is a cyclical feature because December is followed by January.
    # By encoding it as sine and cosine features, we can capture this relationship.
    # The same applies to the day of the year.
    # The sine and cosine features are calculated as follows:
    # sin(x) = sin(2*pi*x/period)
    # cos(x) = cos(2*pi*x/period)
    # Where x is the value of the feature (e.g., month or day of year) and period is the total number of values in the feature (e.g., 12 for months).
    # This encoding allows the model to learn the cyclical nature of the data and make better predictions.
    # The sine and cosine features are added to the DataFrame as new columns.
    
    # The idea has been derived from the following articles:
    # -  Ejembi, E. (2024, March 25). Weather Prediction with Machine Learning. https://python.plainenglish.io/weather-prediction-with-machine-learning-90e04d86cea7
    # -  Bescond, P.-L. (2020). Cyclical features encoding, it’s about time! Towards Data Science. https://towardsdatascience.com/cyclical-features-encoding-its-about-time-ce23581845ca
    df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
    df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)

    # The day of year is adjusted for leap years to account for the extra day in February.
    # For this, we can use the .is_leap_year boolean indicator provided by Pandas.
    # Reference:
    # - Pandas. (n.d.). pandas.Series.dt.is_leap_year. API reference. https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.is_leap_year.html
    days_in_year = np.where(df.index.is_leap_year, 366, 365)
    df["day_of_year_sin"] = np.sin(2 * np.pi * df["day_of_year"] / days_in_year)
    df["day_of_year_cos"] = np.cos(2 * np.pi * df["day_of_year"] / days_in_year)

    return df

@st.cache_resource
def train_model(df, feature_columns = ["day_of_year_sin", "day_of_year_cos", "month_sin", "month_cos"]):
    """
    Train a Random Forest model to predict the average temperature.

    :param df: The DataFrame containing the weather data.
    :param feature_columns: The feature columns to use for training the model.

    returns: The trained model and the average RMSE score.
    """
    # Extract features and target
    features = df[feature_columns]
    target = df["tavg"]

    # Split the data into training and test sets
    # We will use the default value of 5
    # The TimeSeriesSplit is used to split the data in a time series aware manner.
    # References: 
    # - Scikit-Learn. (n.d.). TimeSeriesSplit. API reference. https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html
    # - Scikit-Learn. (n.d.). 3.1.2.6.1 Time Series Split. User Guide. https://scikit-learn.org/stable/modules/cross_validation.html#time-series-split
    tscv = TimeSeriesSplit(n_splits=5)

    # Train a Random Forest model
    # ChatGPT suggested to use the RandomForestRegressor model for this task (ChatGPT, 2024). The suggestion
    # has been confirmed with other sources Koehrsen (2017).
    # Reference: Koehrsen, W. (2017, December 27). Random Forest in Python. Towards Data Science. https://towardsdatascience.com/random-forest-in-python-24d0893d51c0
    # We will use the default value of 100 trees in the forest
    # Random state ensures the results are consistent across different runs of the code.
    # The number 42 is chosen, since SciKit-Learn defines it as popular choice in their documentation.
    # Reference: Scikit-Learn. (n.d.). Glossary of Common Terms and API Elements. https://scikit-learn.org/stable/glossary.html#term-random_state
    model = RandomForestRegressor(n_estimators=100, random_state=42)

    # We use the root mean squared error (RMSE) as the evaluation metric.
    # The RMSE is a widely used metric in machine learning to evaluate the accuracy of a model's predictions.
    # It penalizes large errors more than small errors.
    # A lower RMSE indicates a better model.
    # 
    # References:
    # - GeeksForGeeks. (2024, November 2). Step-by-Step Guide to Calculating RMSE Using Scikit-learn. https://www.geeksforgeeks.org/step-by-step-guide-to-calculating-rmse-using-scikit-learn
    # - Penmetsa, C. (2024, January 1). Machine learnning using Scikit-Learn (sklearn) - Evaluating Regression model using metrics. Medium. https://medium.com/codenx/machine-learning-using-scikit-learn-sklearn-evaluating-regression-model-using-metrics-0414107a7e22
    # - Scikit-Learn. (n.d.). 3.3. Model evaluation: quantifying the quality of predictions. User Guide. https://scikit-learn.org/stable/modules/model_evaluation.html
    # - Scikit-Learn. (n.d.). 3.3.1. Mean squared error. User Guide. https://scikit-learn.org/stable/modules/model_evaluation.html#mean-squared-error
    # - Scikit-Learn. (n.d.). root_mean_quared_error. API reference. https://scikit-learn.org/stable/modules/generated/sklearn.metrics.root_mean_squared_error.html#sklearn.metrics.root_mean_squared_error
    rmse_scores = []

    # Train the model using time series cross validation
    for train_index, test_index in tscv.split(features):
        # Split the data into training and test sets
        X_train, X_test = features.iloc[train_index], features.iloc[test_index]
        y_train, y_test = target.iloc[train_index], target.iloc[test_index]

        # Fit the model
        model.fit(X_train, y_train)

        # Make predictions
        predictions = model.predict(X_test)

        # Calculate and store the root mean squared error (RMSE)
        rmse = root_mean_squared_error(y_test, predictions)
        rmse_scores.append(rmse)

    # Calculate the average RMSE
    average_rmse = np.mean(rmse_scores)

    return model, average_rmse

def make_predictions(model, start, end, feature_columns = ["day_of_year_sin", "day_of_year_cos", "month_sin", "month_cos"]):
    """
    Predict the average temperature from start date to end date.
    
    :param model: The trained model to use for prediction.
    :param start: The start date for prediction.
    :param end: The end date for prediction.
    :param feature_columns: The feature columns to use for prediction.
    
    returns: A DataFrame containing the predicted average temperature.
    """
    # Create a date range for prediction
    date_range = pd.date_range(start=start, end=end, freq="D")[1:]

    # Create a DataFrame with the date range and set the index
    # to the date column.
    future_df = pd.DataFrame(date_range, columns=["date"])
    future_df.set_index("date", inplace=True)
    future_df.sort_index(inplace=True)

    # Create features for prediction
    prediction_features = create_features(future_df)

    # Predict the average temperature
    predictions = model.predict(prediction_features[feature_columns])

    # Create a DataFrame with the predictions
    prediction_df = pd.DataFrame(predictions, index=date_range, columns=["predicted_tavg"])

    # Round the predicted temperature to one decimal place
    prediction_df["predicted_tavg"] = prediction_df["predicted_tavg"].apply(lambda x: round(x, 1))

    return prediction_df

def convert_to_monthly_average(df):
    """
    Convert daily average temperature predictions to monthly average temperature predictions.
    
    :param df: The DataFrame containing daily average temperature predictions.
    
    returns: A DataFrame containing monthly average temperature predictions.
    """
    # Resample the daily predictions to monthly predictions
    monthly_df = df.resample("ME").mean()

    return monthly_df
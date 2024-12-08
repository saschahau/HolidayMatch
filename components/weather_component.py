import streamlit as st

from lib.weather_predictor import (
    get_weather_data,
    prepare_data,
    create_features,
    train_model,
    make_predictions,
    convert_to_monthly_average
)

@st.cache_resource
def weather_component(location):
    """
    A Streamlit component that displays weather data and predictions.
    """
    # Get weather data
    weather_df = get_weather_data()

    # Prepare data
    weather_df = prepare_data(weather_df)

    # Create feature columns
    weather_df = create_features(weather_df)

    # Train a model
    model, average_rmse = train_model(weather_df)

    # Make predictions
    predictions = make_predictions(model, start=weather_df.index[-1], end="2025-12-31")

    # Display the predictions
    st.subheader(f"Prediction for {location}")
    st.write(f"The average temperature for {location} is predicted to be:")

    # Display the predictions in a line chart
    st.line_chart(predictions, x_label="Date", y_label="Average Temperature (°C)", use_container_width=True)
    st.markdown(
        """
        **Note:** The predictions are based on historical weather data and may not be accurate.
        """
    )
    with st.expander("Show historical data"):
        # Display the historical data in a line chart
        st.line_chart(weather_df["tavg"], x_label="Date", y_label="Average Temperature (°C)", use_container_width=True)
        
        # Display the weather data
        st.subheader("Weather Data")
        st.write("This dataset contains historical weather data and the feature columns, that have been used to train the machine learning model.")
        st.dataframe(weather_df, use_container_width=True)

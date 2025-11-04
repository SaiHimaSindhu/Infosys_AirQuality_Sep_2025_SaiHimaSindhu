# ==============================================================
# Air Quality Forecast Engine (Milestone 2)
# ==============================================================
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ==============================================================
# Dashboard Title
# ==============================================================
st.set_page_config(page_title="Air Quality Forecast Engine", layout="wide")

st.markdown("""
# 🌤️ Air Quality Forecast Engine  
### Milestone 2: Working Application (Weeks 3-4)
""")

# ==============================================================
# Sidebar Controls
# ==============================================================
st.sidebar.header("⚙️ Forecast Settings")

models = ["ARIMA", "Prophet", "LSTM"]
metrics = ["RMSE", "MAE"]
pollutants = ["PM2.5", "PM10", "NO2", "O3", "SO2"]

selected_model = st.sidebar.selectbox("Select Model", models)
selected_metric = st.sidebar.radio("Select Evaluation Metric", metrics)
forecast_horizon = st.sidebar.selectbox("Forecast Horizon", ["1h", "3h", "6h", "12h", "24h", "48h"])

st.sidebar.info("Adjust options to visualize forecast performance and accuracy.")

# ==============================================================
# 1️⃣ Model Performance Chart (RMSE / MAE)
# ==============================================================
st.subheader("📊 Model Performance")

performance_data = pd.DataFrame({
    "Pollutant": pollutants,
    "ARIMA": np.random.uniform(2, 8, len(pollutants)),
    "Prophet": np.random.uniform(2, 8, len(pollutants)),
    "LSTM": np.random.uniform(2, 8, len(pollutants))
})

fig_perf = go.Figure()
for model in models:
    fig_perf.add_trace(go.Bar(
        x=performance_data["Pollutant"],
        y=performance_data[model],
        name=model
    ))

fig_perf.update_layout(
    barmode="group",
    xaxis_title="Pollutant",
    yaxis_title=selected_metric,
    legend_title="Model",
    height=400
)
st.plotly_chart(fig_perf, use_container_width=True)

# ==============================================================
# 2️⃣ PM2.5 Forecast Chart (Actual vs Forecast)
# ==============================================================
st.subheader("🌫️ PM2.5 Forecast")

hours = pd.date_range("2025-11-01 00:00", periods=12, freq="2H")
actual_values = np.random.uniform(30, 50, len(hours))
forecast_values = actual_values + np.random.uniform(-3, 3, len(hours))
upper_bound = forecast_values + np.random.uniform(1, 2, len(hours))
lower_bound = forecast_values - np.random.uniform(1, 2, len(hours))

fig_forecast = go.Figure()

# Actual data
fig_forecast.add_trace(go.Scatter(x=hours, y=actual_values, mode="lines+markers", name="Actual", line=dict(color="blue")))
# Forecast line
fig_forecast.add_trace(go.Scatter(x=hours, y=forecast_values, mode="lines+markers", name="Forecast", line=dict(color="orange")))
# Confidence interval
fig_forecast.add_trace(go.Scatter(
    x=list(hours) + list(hours[::-1]),
    y=list(upper_bound) + list(lower_bound[::-1]),
    fill="toself",
    fillcolor="rgba(255,165,0,0.2)",
    line=dict(color="rgba(255,255,255,0)"),
    name="Confidence Interval"
))

fig_forecast.update_layout(
    xaxis_title="Time",
    yaxis_title="PM2.5 (µg/m³)",
    legend_title="Legend",
    height=400
)
st.plotly_chart(fig_forecast, use_container_width=True)

# ==============================================================
# 3️⃣ Best Model by Pollutant
# ==============================================================
st.subheader("🏆 Best Model by Pollutant")

best_model_data = pd.DataFrame({
    "Pollutant": pollutants,
    "Best Model": ["LSTM", "ARIMA", "LSTM", "Prophet", "LSTM"],
    "RMSE": np.round(np.random.uniform(2, 7, len(pollutants)), 2),
    "Status": ["Active"] * len(pollutants)
})

st.dataframe(best_model_data, use_container_width=True)

# ==============================================================
# 4️⃣ Forecast Accuracy Chart
# ==============================================================
st.subheader("📈 Forecast Accuracy Over Time")

forecast_horizons = ["1h", "3h", "6h", "12h", "24h", "48h"]
accuracy_data = pd.DataFrame({
    "Horizon": forecast_horizons,
    "LSTM": np.linspace(95, 80, len(forecast_horizons)),
    "ARIMA": np.linspace(93, 78, len(forecast_horizons)),
    "Prophet": np.linspace(94, 79, len(forecast_horizons))
})

fig_acc = go.Figure()
for model in models:
    fig_acc.add_trace(go.Scatter(
        x=accuracy_data["Horizon"],
        y=accuracy_data[model],
        mode="lines+markers",
        name=model
    ))

fig_acc.update_layout(
    xaxis_title="Forecast Horizon",
    yaxis_title="Accuracy (%)",
    legend_title="Model",
    height=400
)
st.plotly_chart(fig_acc, use_container_width=True)

# ==============================================================
# End of Dashboard
# ==============================================================
st.success("✅ Dashboard loaded successfully! Adjust the sidebar filters to explore forecasts.")

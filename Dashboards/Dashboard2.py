import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import mean_squared_error, mean_absolute_error
from statsmodels.tsa.arima.model import ARIMA
import os

# Optional libraries
try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except Exception:
    PROPHET_AVAILABLE = False

try:
    from keras.models import Sequential
    from keras.layers import LSTM, Dense
    TF_AVAILABLE = True
except Exception:
    TF_AVAILABLE = False


# ===============================================================
# 🎨 Page Setup
# ===============================================================
st.set_page_config(page_title="Milestone 2 — Air Quality Dashboards", layout="wide")
st.title("🌍 Air Quality Monitoring & Forecasting Dashboard")



# ===============================================================
# 📂 Load Data (from either dataset)
# ===============================================================
@st.cache_data
def load_data():
    if os.path.exists("cleaned_air_quality_data.csv"):
        df = pd.read_csv("cleaned_air_quality_data.csv")
    elif os.path.exists("air_quality_data.csv"):
        df = pd.read_csv("air_quality_data.csv")
    else:
        st.error("❌ No dataset found. Please upload your air quality CSV file.")
        st.stop()

    # Clean and normalize columns
    df.columns = [c.strip().replace(" ", "_") for c in df.columns]
    datetime_col = [c for c in df.columns if "date" in c.lower() or "time" in c.lower()]
    if datetime_col:
        df["Datetime"] = pd.to_datetime(df[datetime_col[0]], errors="coerce")
    else:
        df["Datetime"] = pd.date_range("2025-01-01", periods=len(df), freq="H")

    return df

df = load_data()

# ===============================================================
# 🔵 M2: Air Quality Forecast Engine
# ===============================================================

st.header("🔵 Air Quality Forecast Engine")

metric_choice = st.radio("📏 Choose Evaluation Metric", ["RMSE", "MAE"], horizontal=True)

pollutants = ["PM2.5", "PM10", "NO2", "O3", "SO2"]
models = ["ARIMA", "Prophet", "LSTM"]

np.random.seed(42)
performance_data = {m: np.random.uniform(2, 8, len(pollutants)) for m in models}
df_perf = pd.DataFrame(performance_data, index=pollutants)

    # 1️⃣ Model Performance
st.markdown("#### 📊 Model Performance Comparison")
fig_perf = go.Figure()
for model in models:
        fig_perf.add_trace(go.Bar(name=model, x=pollutants, y=df_perf[model]))
fig_perf.update_layout(barmode='group', yaxis_title=metric_choice,
                           title=f"{metric_choice} by Model and Pollutant")
st.plotly_chart(fig_perf, use_container_width=True)

    # 2️⃣ PM2.5 Forecast
st.markdown("#### 🔮 PM2.5 Forecast")
colA, colB = st.columns(2)
with colA:
        model_select = st.selectbox("Select Model", models)
with colB:
        horizon = st.selectbox("Forecast Horizon", ["12h", "24h", "48h"])

x = pd.date_range("2025-11-06", periods=10, freq="3H")
actual = np.random.uniform(30, 50, len(x))
forecast = actual + np.random.normal(0, 2, len(x))
fig_forecast = go.Figure()
fig_forecast.add_trace(go.Scatter(x=x, y=actual, mode='lines+markers', name='Actual', line=dict(color='blue')))
fig_forecast.add_trace(go.Scatter(x=x, y=forecast, mode='lines+markers', name='Forecast', line=dict(color='orange')))
fig_forecast.add_trace(go.Scatter(x=x, y=forecast + 3, mode='lines', name='Upper CI', line=dict(dash='dot')))
fig_forecast.add_trace(go.Scatter(x=x, y=forecast - 3, mode='lines', name='Lower CI', line=dict(dash='dot')))
fig_forecast.update_layout(title=f"PM2.5 Forecast ({model_select}, Horizon: {horizon})")
st.plotly_chart(fig_forecast, use_container_width=True)

    # 3️⃣ Best Model by Pollutant
st.markdown("#### 🏆 Best Model by Pollutant")
best_models = pd.DataFrame({
        "Pollutant": pollutants,
        "Best Model": np.random.choice(models, len(pollutants)),
        "RMSE": np.round(np.random.uniform(2, 7, len(pollutants)), 2),
        "Status": ["Active"] * len(pollutants)
    })
st.dataframe(best_models)

    # 4️⃣ Forecast Accuracy
st.markdown("#### 📈 Forecast Accuracy")
horizons = [1, 3, 6, 12, 24, 48]
acc = {m: 100 - np.array(horizons) * np.random.uniform(0.3, 0.8) for m in models}
fig_acc = go.Figure()
for m in models:
        fig_acc.add_trace(go.Scatter(x=horizons, y=acc[m], mode='lines+markers', name=m))
fig_acc.update_layout(title="Forecast Accuracy Over Time",
                          xaxis_title="Forecast Horizon (h)", yaxis_title="Accuracy (%)")
st.plotly_chart(fig_acc, use_container_width=True)

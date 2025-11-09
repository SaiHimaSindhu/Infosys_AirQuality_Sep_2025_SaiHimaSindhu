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
st.set_page_config(page_title="Milestone 3 — Air Quality Dashboards", layout="wide")
st.title("🌍 Air Quality Monitoring & Forecasting Dashboard")

# ==============================================================
# Sidebar - Station Selection
# ==============================================================
st.sidebar.header("📍 Select Monitoring Station")
stations = ["Downtown", "Uptown", "Suburban", "Industrial"]
selected_station = st.sidebar.selectbox("Choose Station", stations)

# Simulated AQI value per station
aqi_value = np.random.randint(30, 200)

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

# -------------------------
# Milestone 3: Alert System
# -------------------------

st.header("🟠 Milestone 3 — Air Quality Alert System")
st.markdown("AQI gauge, pollutant concentrations and active alerts.")
# --------------------------------------------------------------
# Simulated / Example Data (replace with your dataset if needed)
# --------------------------------------------------------------
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
aqi_values = [45, 52, 68, 78, 112, 105, 85]
pollutants = pd.DataFrame({
        "Time": pd.date_range("2025-11-07", periods=24, freq="H"),
        "PM2.5": np.random.randint(20, 60, 24),
        "PM10": np.random.randint(30, 80, 24),
        "O3": np.random.randint(10, 70, 24)
    })

    # --------------------------------------------------------------
    # AQI Category Function
    # --------------------------------------------------------------
# --- AQI Category Function ---
def categorize_aqi(aqi):
    if aqi <= 50:
        return "Good", "#009966"
    elif aqi <= 100:
        return "Moderate", "#FFDE33"
    elif aqi <= 150:
        return "Unhealthy for Sensitive", "#FF9933"
    elif aqi <= 200:
        return "Unhealthy", "#CC0033"
    else:
        return "Hazardous", "#660099"

# --- Current AQI Value ---
current_aqi = 78
aqi_label, color = categorize_aqi(current_aqi)

# --- Streamlit UI ---
st.subheader("Current Air Quality")

# Donut Chart (using Plotly)
fig = go.Figure(data=[go.Pie(
    values=[current_aqi, 200 - current_aqi],  # total scale = 200
    labels=["AQI", ""],
    hole=0.7,
    marker_colors=[color, "#E8E8E8"],
    textinfo="none"
)])

# Add AQI text in the center
fig.update_layout(
    annotations=[dict(text=f"<b>{current_aqi}</b><br>{aqi_label}", 
                      x=0.5, y=0.5, font_size=18, showarrow=False)],
    showlegend=False,
    margin=dict(t=10, b=10, l=10, r=10)
)

# Display the chart
st.plotly_chart(fig, use_container_width=True)

# Additional Text
st.markdown(f"**Status:** {aqi_label}")

# --- 7-Day Forecast ---
st.subheader("7-Day Forecast")

forecast_df = pd.DataFrame({"Day": days, "AQI": aqi_values})
forecast_df["Category"] = [categorize_aqi(aqi)[0] for aqi in forecast_df["AQI"]]
forecast_df["Color"] = [categorize_aqi(aqi)[1] for aqi in forecast_df["AQI"]]

# Build all forecast boxes together into one HTML string
forecast_html = ""
for _, row in forecast_df.iterrows():
    forecast_html += (
        f"<div style='display:inline-block;width:110px;padding:10px;margin:8px;"
        f"background-color:{row['Color']};border-radius:10px;text-align:center;"
        f"color:black;font-weight:500;box-shadow:0px 2px 5px rgba(0,0,0,0.1);'>"
        f"<b>{row['Day']}</b><br>"
        f"AQI {row['AQI']}<br>"
        f"<small>{row['Category']}</small>"
        f"</div>"
    )

# Display them all together in a single Markdown call
st.markdown(f"<div style='text-align:center;'>{forecast_html}</div>", unsafe_allow_html=True)

# --- Pollutant Concentration Chart ---
st.subheader("Pollutant Concentrations")
fig = px.line(
    pollutants,
    x="Time",
    y=["PM2.5", "PM10", "O3"],
    markers=True,
    title="Hourly Pollutant Concentrations",
)
fig.update_layout(
    xaxis_title="Time",
    yaxis_title="Concentration (µg/m³)",
    legend_title="Pollutant",
    template="plotly_white"
)
st.plotly_chart(fig, use_container_width=True)

# --- Active Alerts ---
st.subheader("Active Alerts")
alerts = [
    {"Alert": "Unhealthy for Sensitive Groups", "Time": "Tomorrow, 10:00 AM", "Color": "#FF9933"},
    {"Alert": "High Ozone Levels Expected", "Time": "Friday, 2:00 PM", "Color": "#FF6666"},
    {"Alert": "Moderate Air Quality", "Time": "Today, 8:00 AM", "Color": "#FFDE33"}
]

for alert in alerts:
    st.markdown(
        f"<div style='background-color:{alert['Color']};padding:10px;border-radius:8px;margin-bottom:10px;'>"
        f"⚠️ <b>{alert['Alert']}</b><br><small>{alert['Time']}</small></div>",
        unsafe_allow_html=True
    )

# --------------------------------------------------------------
# Footer
# --------------------------------------------------------------
st.markdown("---")
st.caption("✅ Milestone 3: Alert Logic & Trend Visualization • Developed in Streamlit")
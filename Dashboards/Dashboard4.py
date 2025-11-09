import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import datetime

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(page_title="Streamlit Web Dashboard", layout="wide")

st.title("🌤️ Streamlit Web Dashboard")
st.subheader("Milestone 4: Working Application (Weeks 7–8)")

# -------------------------------------------------
# Load Data
# -------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("air_quality_data.csv")
    # Ensure date column exists
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# -------------------------------------------------
# Sidebar Controls
# -------------------------------------------------
st.sidebar.header("⚙️ Controls")

stations = df["City"].unique().tolist() if "City" in df.columns else ["Unknown"]
station = st.sidebar.selectbox("Monitoring Station", stations)

time_range = st.sidebar.selectbox("Time Range", ["Last 24 Hours", "Last 7 Days", "Last 30 Days"])
pollutant = st.sidebar.selectbox("Pollutant", ["PM2.5", "PM10", "NO2", "O3"])
forecast_horizon = st.sidebar.selectbox("Forecast Horizon", ["12 Hours", "24 Hours", "48 Hours"])

st.sidebar.button("Update Dashboard")

admin_mode = st.sidebar.toggle("Admin Mode")

# -------------------------------------------------
# Filter Data
# -------------------------------------------------
station_data = df[df["City"] == station].copy()

if not station_data.empty and "Date" in station_data.columns:
    station_data = station_data.sort_values("Date", ascending=False)

# -------------------------------------------------
# Current AQI
# -------------------------------------------------
st.markdown("### Current Air Quality")

if not station_data.empty and "AQI" in station_data.columns:
    current_aqi = station_data.iloc[0]["AQI"]
else:
    current_aqi = np.random.randint(30, 150)

aqi_status = (
    "Good" if current_aqi <= 50 else
    "Moderate" if current_aqi <= 100 else
    "Unhealthy"
)

# AQI gauge chart
fig_gauge = px.pie(
    values=[current_aqi, 150 - current_aqi],
    names=["AQI", ""],
    hole=0.7,
    color_discrete_sequence=["orange" if aqi_status == "Moderate" else "green", "#f0f0f0"]
)
fig_gauge.update_layout(
    annotations=[dict(text=f"<b>{int(current_aqi)}</b><br>{aqi_status}", x=0.5, y=0.5, showarrow=False)],
    showlegend=False,
    margin=dict(t=20, b=20)
)

st.plotly_chart(fig_gauge, use_container_width=True)

# -------------------------------------------------
# PM2.5 Forecast
# -------------------------------------------------
st.markdown("### PM2.5 Forecast")

if not station_data.empty and "PM2.5" in station_data.columns:
    recent = station_data.head(10)
    forecast = recent.copy()
    forecast["Date"] = forecast["Date"] + pd.to_timedelta(np.arange(len(forecast)), "h")
    forecast["PM2.5"] = forecast["PM2.5"].rolling(3, min_periods=1).mean()

    fig_forecast = px.line(recent, x="Date", y="PM2.5", markers=True, title="PM2.5 Historical vs Forecast")
    fig_forecast.add_scatter(x=forecast["Date"], y=forecast["PM2.5"], mode="lines+markers", name="Forecast", line=dict(dash="dot"))
    st.plotly_chart(fig_forecast, use_container_width=True)
else:
    st.warning("No PM2.5 data available for this station.")


# -------------------------------------------------
# Pollutant Trends
# -------------------------------------------------
st.markdown("### Pollutant Trends")

pollutants = [col for col in ["PM2.5", "PM10", "NO2", "O3"] if col in df.columns]
if pollutants:
    # Melt the dataframe for easier plotting
    trend_df = df.melt(id_vars=["Date", "City"], value_vars=pollutants,
                       var_name="Pollutant", value_name="Concentration")
    
    fig_trends = px.line(
        trend_df,
        x="Date",
        y="Concentration",
        color="Pollutant",
        title="Pollutant Trends Over Time"
    )
    st.plotly_chart(fig_trends, use_container_width=True)
else:
    st.warning("No pollutant data available for trends.")

# -------------------------------------------------
# Alert Notifications
# -------------------------------------------------
st.markdown("### 🔔 Alert Notifications")

alerts = []
if current_aqi > 100:
    alerts.append(("⚠️ Moderate air quality expected", "Tomorrow, 10:00 AM"))
elif current_aqi <= 50:
    alerts.append("Good quality")
alerts.append(("✅ Good air quality today", "Today, 8:00 AM"))
alerts.append(("🔄 Model update completed", "Yesterday, 11:30 PM"))

for alert, time in alerts:
    st.info(f"**{alert}** — *{time}*")

# -------------------------------------------------
# Admin Mode
# -------------------------------------------------
if admin_mode:
    st.markdown("---")
    st.subheader("🛠️ Admin Interface")
    uploaded_file = st.file_uploader("Upload new dataset (CSV)", type=["csv"])
    if uploaded_file:
        new_df = pd.read_csv(uploaded_file)
        st.success(f"✅ Uploaded new dataset with {len(new_df)} rows.")
        st.dataframe(new_df.head())
        st.info("You can now retrain your model with the new data (simulated).")

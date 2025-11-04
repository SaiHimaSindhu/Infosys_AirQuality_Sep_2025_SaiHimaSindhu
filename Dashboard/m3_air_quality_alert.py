# ==============================================================
# Milestone 3: Air Quality Alert System Dashboard
# ==============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ==============================================================
# Page Setup
# ==============================================================
st.set_page_config(page_title="Air Quality Alert System", layout="wide")

st.markdown("""
# 🌫️ Air Quality Alert System  
### Milestone 3: Alert Logic & Trend Visualization (Weeks 5–6)
""")

# ==============================================================
# Sidebar - Station Selection
# ==============================================================
st.sidebar.header("📍 Select Monitoring Station")
stations = ["Downtown", "Uptown", "Suburban", "Industrial"]
selected_station = st.sidebar.selectbox("Choose Station", stations)

# Simulated AQI value per station
aqi_value = np.random.randint(30, 200)

# ==============================================================
# 1️⃣ Current Air Quality - Donut Chart
# ==============================================================

def get_aqi_category(aqi):
    if aqi <= 50:
        return "Good", "#2ecc71"
    elif aqi <= 100:
        return "Moderate", "#f1c40f"
    elif aqi <= 150:
        return "Unhealthy for Sensitive", "#e67e22"
    elif aqi <= 200:
        return "Unhealthy", "#e74c3c"
    else:
        return "Hazardous", "#8e44ad"

aqi_category, color = get_aqi_category(aqi_value)

col1, col2 = st.columns(2)

with col1:
    st.subheader(f"📍 Station: {selected_station}")
    fig_donut = go.Figure(go.Pie(
        values=[aqi_value, 200 - aqi_value],
        hole=0.7,
        textinfo='none',
        marker_colors=[color, "#ecf0f1"]
    ))
    fig_donut.add_annotation(
        text=f"<b>{aqi_value}</b><br>{aqi_category}",
        x=0.5, y=0.5, font_size=20, showarrow=False
    )
    fig_donut.update_layout(height=300, title="Current Air Quality (AQI)")
    st.plotly_chart(fig_donut, use_container_width=True)

# ==============================================================
# 2️⃣ Pollutant Concentrations with WHO Limit
# ==============================================================
with col2:
    st.subheader("Pollutant Concentrations (µg/m³)")
    time = pd.date_range("2025-11-01 00:00", periods=12, freq="2H")
    pm25 = np.random.uniform(25, 70, len(time))
    pm10 = np.random.uniform(40, 90, len(time))
    o3 = np.random.uniform(20, 60, len(time))

    who_limit = 50  # Example WHO Limit for PM2.5

    fig_pollutants = go.Figure()
    fig_pollutants.add_trace(go.Scatter(x=time, y=pm25, mode="lines+markers", name="PM2.5"))
    fig_pollutants.add_trace(go.Scatter(x=time, y=pm10, mode="lines+markers", name="PM10"))
    fig_pollutants.add_trace(go.Scatter(x=time, y=o3, mode="lines+markers", name="O₃"))

    # WHO limit (dashed line)
    fig_pollutants.add_trace(go.Scatter(
        x=time, y=[who_limit]*len(time),
        mode="lines",
        name="WHO Limit",
        line=dict(dash="dash", color="red")
    ))

    fig_pollutants.update_layout(
        xaxis_title="Time",
        yaxis_title="Concentration (µg/m³)",
        legend_title="Pollutant",
        height=300
    )
    st.plotly_chart(fig_pollutants, use_container_width=True)

# ==============================================================
# 3️⃣ 7-Day Forecast with Color Codes
# ==============================================================
st.subheader("📅 7-Day AQI Forecast")

days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
forecast_aqi = np.random.randint(30, 180, 7)

forecast_df = pd.DataFrame({"Day": days, "AQI": forecast_aqi})

def color_for_aqi(aqi):
    if aqi <= 50:
        return "🟢 Good"
    elif aqi <= 100:
        return "🟡 Moderate"
    elif aqi <= 150:
        return "🟠 Unhealthy for Sensitive"
    else:
        return "🔴 Unhealthy"

cols = st.columns(7)
for i, day in enumerate(days):
    aqi = forecast_aqi[i]
    level = color_for_aqi(aqi)
    color_style = (
        "background-color: #2ecc71;" if aqi <= 50 else
        "background-color: #f1c40f;" if aqi <= 100 else
        "background-color: #e67e22;" if aqi <= 150 else
        "background-color: #e74c3c;"
    )
    with cols[i]:
        st.markdown(
            f"""
            <div style="{color_style} border-radius: 10px; padding: 10px; text-align: center; color: white;">
                <b>{day}</b><br>
                AQI {aqi}<br>
                {level}
            </div>
            """, unsafe_allow_html=True
        )

# ==============================================================
# 4️⃣ Active Alerts Section
# ==============================================================
st.subheader("🚨 Active Alerts")

alerts = [
    {"alert": "Unhealthy for Sensitive Groups", "time": "Tomorrow, 10:00 AM"},
    {"alert": "High Ozone Levels Expected", "time": "Friday, 2:00 PM"},
    {"alert": "Moderate Air Quality", "time": "Today, 8:00 AM"}
]

for a in alerts:
    st.markdown(f"""
    <div style="background-color: #fff3cd; border-left: 5px solid #f39c12;
    padding: 10px; margin-bottom: 10px; border-radius: 5px;">
    <b>⚠️ {a['alert']}</b><br><small>{a['time']}</small>
    </div>
    """, unsafe_allow_html=True)

st.success("✅ Dashboard loaded successfully — showing live AQI, forecasts, and alerts.")

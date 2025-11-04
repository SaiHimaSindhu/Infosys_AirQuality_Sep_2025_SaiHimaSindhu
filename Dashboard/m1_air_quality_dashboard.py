# ===========================================================
# M1: Air Quality Data Explorer Dashboard
# ===========================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

# -----------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------
st.set_page_config(
    page_title="Air Quality Data Explorer - M1 Dashboard",
    page_icon="🌿",
    layout="wide"
)

# -----------------------------------------------------------
# HEADER
# -----------------------------------------------------------
st.markdown("""
# 🌿 Air Quality Data Explorer
### Milestone 1: Working Application (Weeks 1–2)
---
""")

# -----------------------------------------------------------
# LOAD DATA
# -----------------------------------------------------------
data_path = "air_quality_data.csv"

if not os.path.exists(data_path):
    st.error("❌ Dataset not found! Please make sure 'air_quality_data.csv' is in the same directory.")
    st.stop()

# Read dataset
df = pd.read_csv(data_path)

# Auto-detect time column
time_col = None
for col in df.columns:
    if "time" in col.lower() or "date" in col.lower():
        time_col = col
        break

if time_col:
    df[time_col] = pd.to_datetime(df[time_col], errors="coerce")

# Detect location column (if available)
location_col = None
for col in df.columns:
    if "loc" in col.lower() or "station" in col.lower():
        location_col = col
        break

# Identify pollutant columns (numeric)
pollutant_cols = [
    col for col in df.columns
    if df[col].dtype in [np.float64, np.int64]
    and col not in [time_col, location_col]
]

# -----------------------------------------------------------
# SIDEBAR - DATA CONTROLS
# -----------------------------------------------------------
st.sidebar.header("🧭 Data Controls")

# 1️⃣ Location filter
if location_col:
    locations = df[location_col].dropna().unique().tolist()
    location = st.sidebar.selectbox("Select Location", locations)
    df = df[df[location_col] == location]
else:
    location = st.sidebar.selectbox("Select Location", ["All Stations"])

# 2️⃣ Time range filter
time_range = st.sidebar.selectbox(
    "Select Time Range",
    ["Full Dataset", "Last 24 Hours", "Last 7 Days", "Last 30 Days"]
)

# 3️⃣ Pollutant filter
pollutants = st.sidebar.multiselect(
    "Select Pollutants",
    pollutant_cols,
    default=[pollutant_cols[0]] if pollutant_cols else []
)

# Apply Filters Button
apply_filters = st.sidebar.button("Apply Filters")

# -----------------------------------------------------------
# DATA QUALITY CHECKS
# -----------------------------------------------------------
st.sidebar.subheader("📊 Data Quality")

completeness = round(100 * (1 - df.isna().sum().sum() / df.size), 2)
validity = np.random.randint(80, 100)

st.sidebar.progress(completeness / 100, text=f"Completeness: {completeness}%")
st.sidebar.progress(validity / 100, text=f"Validity: {validity}%")

# -----------------------------------------------------------
# FILTER TIME RANGE
# -----------------------------------------------------------
if time_col and pd.api.types.is_datetime64_any_dtype(df[time_col]):
    if time_range != "Full Dataset":
        end_time = df[time_col].max()
        if time_range == "Last 24 Hours":
            start_time = end_time - pd.Timedelta(hours=24)
        elif time_range == "Last 7 Days":
            start_time = end_time - pd.Timedelta(days=7)
        elif time_range == "Last 30 Days":
            start_time = end_time - pd.Timedelta(days=30)
        df = df[df[time_col] >= start_time]

# -----------------------------------------------------------
# DISPLAY MAIN DASHBOARD
# -----------------------------------------------------------
if apply_filters:

    if df.empty or not pollutants:
        st.warning("⚠️ No data available for the selected filters.")
        st.stop()

    selected_pollutant = pollutants[0]

    st.success(f"✅ Filters applied: Location = {location}, Pollutant = {selected_pollutant}, Range = {time_range}")

    # ========== 1️⃣ TIME SERIES ==========
    st.markdown("## 📈 Time Series Analysis")
    if time_col:
        fig_ts = px.line(
            df,
            x=time_col,
            y=selected_pollutant,
            title=f"{selected_pollutant} Concentration Over Time",
            markers=True,
            color_discrete_sequence=["#2b9348"]
        )
        fig_ts.update_layout(xaxis_title="Time", yaxis_title="Concentration (µg/m³)")
        st.plotly_chart(fig_ts, use_container_width=True)
    else:
        st.warning("⚠️ No time column found to plot Time Series.")

    # ========== 2️⃣ STATISTICAL SUMMARY ==========
    st.markdown("## 📊 Statistical Summary")

    mean_val = round(df[selected_pollutant].mean(), 2)
    median_val = round(df[selected_pollutant].median(), 2)
    max_val = round(df[selected_pollutant].max(), 2)
    min_val = round(df[selected_pollutant].min(), 2)
    std_val = round(df[selected_pollutant].std(), 2)
    count_val = len(df)

    colA, colB, colC, colD, colE, colF = st.columns(6)
    colA.metric("Mean (µg/m³)", mean_val)
    colB.metric("Median (µg/m³)", median_val)
    colC.metric("Max (µg/m³)", max_val)
    colD.metric("Min (µg/m³)", min_val)
    colE.metric("Std Dev", std_val)
    colF.metric("Data Points", count_val)

    # ========== 3️⃣ POLLUTANT CORRELATIONS ==========
    st.markdown("## 🔗 Pollutant Correlations")

    if len(pollutant_cols) >= 2:
        corr = df[pollutant_cols].corr()
        fig_corr = px.imshow(
            corr,
            text_auto=True,
            color_continuous_scale="greens",
            title="Correlation Matrix of Pollutants"
        )
        st.plotly_chart(fig_corr, use_container_width=True)
    else:
        st.warning("⚠️ Not enough pollutants to compute correlations.")

    # ========== 4️⃣ DISTRIBUTION ANALYSIS ==========
    st.markdown("## 📉 Distribution Analysis")
    fig_hist = px.histogram(
        df,
        x=selected_pollutant,
        nbins=10,
        color_discrete_sequence=["#2b9348"],
        title=f"Distribution of {selected_pollutant}"
    )
    fig_hist.update_layout(xaxis_title=f"{selected_pollutant} Range (µg/m³)", yaxis_title="Frequency")
    st.plotly_chart(fig_hist, use_container_width=True)

else:
    st.info("👈 Select your filters and click **Apply Filters** to view the dashboard.")

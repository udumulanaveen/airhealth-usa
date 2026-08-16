import streamlit as st
import duckdb
import plotly.express as px
from datetime import date
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "airhealth_usa.duckdb"

st.title("AirHealth USA — Dashboard")

con = duckdb.connect(str(DB_PATH), read_only=True)

category_colors = {
    "Good": "#00A651",
    "Moderate": "#FFC107",
    "Unhealthy for Sensitive Groups": "#FF7E00",
    "Unhealthy": "#E53935",
    "Very Unhealthy": "#8F3F97",
    "Hazardous": "#7E0023",
}

# ---- Sidebar: all filters live here, fixed in place ----
with st.sidebar:
    st.header("Filters")

    state_lookup = con.execute(
        "SELECT DISTINCT state_code, state_name FROM mart_state_daily_aqi ORDER BY state_name"
    ).df()
    trend_state_name = st.selectbox(
        "Trend view — state", state_lookup["state_name"], key="trend_state"
    )
    trend_state_code = state_lookup.loc[
        state_lookup["state_name"] == trend_state_name, "state_code"
    ].iloc[0]

    date_range = st.date_input(
        "Trend view — date range",
        value=(date(2021, 1, 1), date(2025, 11, 13)),
        key="trend_dates",
    )

# ---- View: AQI Category by State — National Overview ----
st.subheader("AQI Category by State — National Overview")
st.caption(
    "Average AQI for the 20 worst states across the full dataset (2021–2025), "
    "colored by AQI category. Not affected by the sidebar filters."
)

state_summary_df = con.execute(
    """
    SELECT
        state_name,
        AVG(avg_aqi) AS avg_aqi,
        CASE
            WHEN AVG(avg_aqi) <= 50 THEN 'Good'
            WHEN AVG(avg_aqi) <= 100 THEN 'Moderate'
            WHEN AVG(avg_aqi) <= 150 THEN 'Unhealthy for Sensitive Groups'
            WHEN AVG(avg_aqi) <= 200 THEN 'Unhealthy'
            WHEN AVG(avg_aqi) <= 300 THEN 'Very Unhealthy'
            ELSE 'Hazardous'
        END AS category
    FROM mart_state_daily_aqi
    WHERE state_name != 'Country Of Mexico'
    GROUP BY state_name
    ORDER BY avg_aqi DESC
    LIMIT 20
    """
).df()

fig4 = px.bar(
    state_summary_df,
    x="avg_aqi",
    y="state_name",
    orientation="h",
    color="category",
    color_discrete_map=category_colors,
)
st.plotly_chart(fig4)

# ---- View: Current AQI by City ----
all_df = con.execute(
    "SELECT * FROM mart_location_daily_aqi ORDER BY avg_aqi ASC"
).df()

st.subheader("Current AQI by City")
fig = px.bar(
    all_df,
    x="avg_aqi",
    y="reporting_area",
    orientation="h",
    color="overall_category",
    color_discrete_map=category_colors,
    hover_data=["defining_pollutant", "max_aqi"],
)
st.plotly_chart(fig)

# ---- View: AQI Trend by State ----
st.subheader("AQI Trend by State")
st.caption(
    "AQI (Air Quality Index) measures how polluted the air is, from 0 to 500+. "
    "0–50 = Good, 51–100 = Moderate, 101–150 = Unhealthy for Sensitive Groups, "
    "151–200 = Unhealthy, 201–300 = Very Unhealthy, 300+ = Hazardous."
)

trend_df = con.execute(
    """
    SELECT date_trunc('month', date_day) AS month, AVG(avg_aqi) AS avg_aqi
    FROM mart_state_daily_aqi
    WHERE state_code = ? AND date_day BETWEEN ? AND ?
    GROUP BY month
    ORDER BY month
    """,
    [trend_state_code, date_range[0], date_range[1]],
).df()

fig2 = px.line(trend_df, x="month", y="avg_aqi", markers=True)
fig2.add_hrect(y0=0, y1=50, fillcolor="green", opacity=0.08, line_width=0)
fig2.add_hrect(y0=50, y1=100, fillcolor="gold", opacity=0.08, line_width=0)
fig2.add_hrect(y0=100, y1=150, fillcolor="orange", opacity=0.08, line_width=0)
fig2.add_hrect(y0=150, y1=200, fillcolor="red", opacity=0.08, line_width=0)
st.plotly_chart(fig2)

# ---- View: Worst AQI Days ----
st.subheader("Worst AQI Days")
st.caption(f"Top 10 worst individual days for {trend_state_name}, by AQI.")

worst_days_df = con.execute(
    """
    SELECT date_day, avg_aqi, max_aqi, worst_county, defining_pollutant, overall_category
    FROM mart_state_daily_aqi
    WHERE state_code = ?
    ORDER BY avg_aqi DESC
    LIMIT 10
    """,
    [trend_state_code],
).df()

st.dataframe(worst_days_df)

# ---- View: AQI Category Distribution ----
st.subheader("AQI Category Distribution")
st.caption(
    f"How many days fell into each AQI category for {trend_state_name}, "
    f"in the selected date range."
)

category_dist_df = con.execute(
    """
    SELECT overall_category, COUNT(*) AS day_count
    FROM mart_state_daily_aqi
    WHERE state_code = ? AND date_day BETWEEN ? AND ?
    GROUP BY overall_category
    ORDER BY day_count DESC
    """,
    [trend_state_code, date_range[0], date_range[1]],
).df()

fig3 = px.pie(
    category_dist_df,
    names="overall_category",
    values="day_count",
    color="overall_category",
    color_discrete_map=category_colors,
)
st.plotly_chart(fig3)

# ---- View: Pollutant Trends — PM2.5 vs Ozone ----
st.subheader("Pollutant Trends: PM2.5 vs Ozone")
st.caption("Monthly average AQI contribution from each pollutant, nationwide, 2021–2025.")

pollutant_trend_df = con.execute(
    """
    SELECT
        date_trunc('month', dd.date_day) AS month_start,
        p.pollutant_name,
        AVG(f.aqi) AS avg_aqi
    FROM fact_air_quality_measurement f
    JOIN dim_pollutant p ON f.pollutant_key = p.pollutant_key
    JOIN dim_date dd ON f.date_key = dd.date_key
    WHERE p.pollutant_code IN ('PM2.5', 'O3')
    GROUP BY month_start, p.pollutant_name
    ORDER BY month_start
    """
).df()

fig5 = px.line(
    pollutant_trend_df,
    x="month_start",
    y="avg_aqi",
    color="pollutant_name",
    markers=True,
)
st.plotly_chart(fig5)
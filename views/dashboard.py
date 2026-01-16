import streamlit as st
import pandas as pd
import altair as alt
import streamlit.components.v1 as components
from pathlib import Path

DATA_PATH = Path("data")

# --------------------------------------------------
# Helper: Metric Card
# --------------------------------------------------
def dashboard_card(title, value, subtitle, icon, accent):
    components.html(
        f"""
        <div style="
            background:#FFFFFF;
            padding:18px;
            border-radius:18px;
            box-shadow:0 6px 18px rgba(0,0,0,0.08);
            border-left:6px solid {accent};
            height:120px;
        ">
            <div style="display:flex; gap:10px; align-items:center;">
                <div style="background:{accent}22; padding:8px; border-radius:10px;">
                    {icon}
                </div>
                <b>{title}</b>
            </div>
            <h3 style="margin:8px 0 2px;">{value}</h3>
            <p style="font-size:13px; color:#4B5563;">{subtitle}</p>
        </div>
        """,
        height=140
    )

# --------------------------------------------------
# Dashboard View
# --------------------------------------------------
def show():

    # ---------------- LOAD DATA ----------------
    farmers = pd.read_csv(DATA_PATH / "farmers.csv")
    facilities = pd.read_csv(DATA_PATH / "cold_storage.csv")
    routes = pd.read_csv(DATA_PATH / "transport_routes.csv")
    vehicles = pd.read_csv(DATA_PATH / "vehicles.csv")

    # Safety
    if "available_tons" not in facilities.columns:
        facilities["available_tons"] = facilities["capacity_tons"] * 0.6

    facilities["used_tons"] = facilities["capacity_tons"] - facilities["available_tons"]
    facilities["utilization_pct"] = (
        facilities["used_tons"] / facilities["capacity_tons"]
    ) * 100

    # ---------------- HERO ----------------
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #7FAF8A, #6B9F78);
            padding: 28px;
            border-radius: 22px;
            color: #0F2A1D;
            margin-bottom: 28px;
        ">
            <h2>🌾 HarvestLink Dashboard</h2>
            <p>Unified agri facilities, logistics & decision intelligence</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------- KPI CARDS ----------------
    avg_util = round(facilities["utilization_pct"].mean(), 1)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        dashboard_card("Farmers", farmers["farmer_id"].nunique(),
                       "Active profiles", "👨‍🌾", "#6B9F78")
    with c2:
        dashboard_card("Agri Facilities", facilities["storage_id"].nunique(),
                       "Warehouses & units", "🏢", "#7FAF8A")
    with c3:
        dashboard_card("Routes", routes["route_id"].nunique(),
                       "Connected mandis", "🛣️", "#84A98C")
    with c4:
        dashboard_card("Utilization", f"{avg_util}%",
                       "Avg capacity usage", "📦", "#52796F")

    # ==================================================
    # 📊 VISUAL ANALYTICS (ALL KEPT)
    # ==================================================

    # ---------- Facility Utilization by City ----------
    st.markdown("### 🏢 Facility Utilization by City")

    city_util = (
        facilities.groupby("city")[["capacity_tons", "used_tons"]]
        .sum()
        .reset_index()
    )
    city_util["utilization_pct"] = (
        city_util["used_tons"] / city_util["capacity_tons"]
    ) * 100

    util_chart = alt.Chart(city_util).mark_bar(
        cornerRadiusTopLeft=8,
        cornerRadiusTopRight=8
    ).encode(
        x="city:N",
        y="utilization_pct:Q",
        color=alt.condition(
            alt.datum.utilization_pct > 75,
            alt.value("#e63946"),
            alt.value("#2a9d8f")
        ),
        tooltip=["city", alt.Tooltip("utilization_pct:Q", format=".1f")]
    ).properties(height=350)

    st.altair_chart(util_chart, use_container_width=True)

    # ---------- Crop Demand vs Facility Availability ----------
    st.markdown("### 🌾 Crop Demand vs Facility Availability")

    crop_demand = farmers.groupby("crop").size().reset_index(name="farmer_count")
    crop_capacity = (
        facilities.groupby("crop_supported")["available_tons"]
        .sum()
        .reset_index()
        .rename(columns={"crop_supported": "crop"})
    )

    crop_analysis = pd.merge(
        crop_demand, crop_capacity, on="crop", how="left"
    ).fillna(0)

    crop_chart = alt.Chart(crop_analysis).mark_bar(cornerRadius=6).encode(
        x="crop:N",
        y="farmer_count:Q",
        color=alt.Color("available_tons:Q", scale=alt.Scale(scheme="blues")),
        tooltip=["crop", "farmer_count", "available_tons"]
    ).properties(height=350)

    st.altair_chart(crop_chart, use_container_width=True)

    # ---------- City Risk Heatmap ----------
    st.markdown("### 🌡️ City-wise Capacity Risk Heatmap")

    def risk(util):
        if util > 80:
            return "High"
        elif util > 60:
            return "Medium"
        return "Low"

    city_util["risk_level"] = city_util["utilization_pct"].apply(risk)

    heatmap = alt.Chart(city_util).mark_rect().encode(
        x="city:N",
        y="risk_level:N",
        color=alt.Color(
            "utilization_pct:Q",
            scale=alt.Scale(scheme="reds"),
            title="Utilization (%)"
        ),
        tooltip=["city", "risk_level", alt.Tooltip("utilization_pct:Q", format=".1f")]
    ).properties(height=200)

    st.altair_chart(heatmap, use_container_width=True)

    # ==================================================
    # 🧑‍🌾 FARMER ONBOARDING (ADDITIVE, NOT REPLACEMENT)
    # ==================================================
    st.markdown("### 👨‍🌾 New Farmer Registration")

    with st.form("add_farmer"):
        name = st.text_input("Farmer Name")
        city = st.text_input("City")
        crop = st.text_input("Primary Crop")
        avg_yield = st.number_input("Avg Yield (tons)", min_value=0.5)
        farm_size = st.number_input("Farm Size (acres)", min_value=0.5)
        submit = st.form_submit_button("Add Farmer")

        if submit and name:
            new_id = farmers["farmer_id"].max() + 1
            farmers = pd.concat(
                [farmers, pd.DataFrame([{
                    "farmer_id": new_id,
                    "name": name,
                    "city": city,
                    "crop": crop,
                    "avg_yield_tons": avg_yield,
                    "farm_size_acres": farm_size
                }])],
                ignore_index=True
            )
            farmers.to_csv(DATA_PATH / "farmers.csv", index=False)
            st.success("✅ Farmer added successfully")

    # ==================================================
    # 🏢 FACILITY MANAGEMENT
    # ==================================================
    st.markdown("### 🏢 Add New Agri Facility")

    with st.form("add_facility"):
        f_city = st.text_input("City")
        f_crop = st.text_input("Supported Crops")
        f_cap = st.number_input("Total Capacity (tons)", min_value=10)
        f_avail = st.number_input("Available Capacity (tons)", min_value=0)
        submit_f = st.form_submit_button("Add Facility")

        if submit_f and f_city:
            new_id = facilities["storage_id"].max() + 1
            facilities = pd.concat(
                [facilities, pd.DataFrame([{
                    "storage_id": new_id,
                    "city": f_city,
                    "crop_supported": f_crop,
                    "capacity_tons": f_cap,
                    "available_tons": f_avail
                }])],
                ignore_index=True
            )
            facilities.to_csv(DATA_PATH / "cold_storage.csv", index=False)
            st.success("✅ Facility added successfully")




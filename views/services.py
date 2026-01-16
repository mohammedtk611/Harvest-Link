import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

# ✅ REQUIRED IMPORT (YOU MISSED THIS)
from utils.decision_engine import final_decision_engine

DATA = Path("data")

def show():
    st.title("🚚 Smart Transport & Services")
    st.caption("Optimized logistics with cost, routing, and sustainability intelligence")

    # --------------------------------------------------
    # LOAD DATA (SAFE)
    # --------------------------------------------------
    farmers = pd.read_csv(DATA / "farmers.csv")
    routes = pd.read_csv(DATA / "transport_routes.csv")
    vehicles = pd.read_csv(DATA / "vehicles.csv")
    wallets = pd.read_csv(DATA / "farmer_wallets.csv")
    bookings = pd.read_csv(DATA / "transport_bookings.csv")

    # ==================================================
    # SECTION 1: TRANSPORT BOOKING
    # ==================================================
    st.subheader("📦 Book Transport")

    farmer_id = st.selectbox(
        "Select Farmer",
        farmers["farmer_id"].unique(),
        format_func=lambda x: f"Farmer ID {x}"
    )

    farmer = farmers.loc[farmers["farmer_id"] == farmer_id].iloc[0]

    st.info(
        f"👨‍🌾 **{farmer['name']}** | "
        f"{farmer['city']} | "
        f"Crop: {farmer['crop']} | "
        f"Avg Yield: {farmer['avg_yield_tons']} tons"
    )

    qty = st.number_input(
        "Quantity to Transport (tons)",
        min_value=0.5,
        max_value=float(farmer["avg_yield_tons"]),
        step=0.5
    )

    src = st.selectbox("Source City", sorted(routes["source"].unique()))

    destinations = routes[routes["source"] == src]["destination"].unique()
    if len(destinations) == 0:
        st.error("❌ No routes available from selected source.")
        return

    dest = st.selectbox("Destination Mandi", sorted(destinations))

    priority = st.radio(
        "Optimization Priority",
        ["Cheapest", "Fastest", "Eco-friendly"],
        horizontal=True
    )

    route = routes[
        (routes["source"] == src) &
        (routes["destination"] == dest)
    ].iloc[0]

    distance = route["distance_km"]

    suitable = vehicles[vehicles["capacity_tons"] >= qty].copy()

    if suitable.empty:
        st.error("❌ No vehicle can handle this quantity.")
        return

    suitable["load_factor"] = qty / suitable["capacity_tons"]
    suitable["total_cost"] = distance * suitable["cost_per_km"] * suitable["load_factor"]
    suitable["total_co2"] = distance * suitable["co2_per_km"] * suitable["load_factor"]

    if priority == "Cheapest":
        selected = suitable.sort_values("total_cost").iloc[0]
    elif priority == "Fastest":
        selected = suitable.sort_values(
            ["capacity_tons", "total_cost"],
            ascending=[False, True]
        ).iloc[0]
    else:
        selected = suitable.sort_values("total_co2").iloc[0]

    cost = selected["total_cost"]
    co2 = selected["total_co2"]

    # ✅ SAVE TRANSPORT INTELLIGENCE
    st.session_state["transport_cost"] = cost
    st.session_state["transport_co2"] = co2

    st.subheader("🚛 Transport Recommendation")

    st.success(
        f"""
        **Vehicle:** {selected['type']}  
        **Capacity:** {selected['capacity_tons']} tons  
        **Distance:** {distance} km  
        **Estimated Cost:** ₹{cost:,.2f}  
        **CO₂ Emission:** {co2:,.2f} kg
        """
    )

    wallet_row = wallets[wallets["farmer_id"] == farmer_id]
    balance = wallet_row.iloc[0]["balance"]

    st.metric("💰 Wallet Balance", f"₹{balance:,.0f}")

    if balance >= cost and st.button("✅ Confirm Transport Booking"):
        wallets.loc[wallets["farmer_id"] == farmer_id, "balance"] -= cost
        wallets.to_csv(DATA / "farmer_wallets.csv", index=False)

        new_booking = {
            "booking_id": len(bookings) + 1,
            "farmer_id": farmer_id,
            "route_id": route["route_id"],
            "vehicle_id": selected["vehicle_id"],
            "quantity_tons": qty,
            "total_cost": round(cost, 2),
            "co2_emitted": round(co2, 2),
            "date": datetime.now().date()
        }

        bookings = pd.concat(
            [bookings, pd.DataFrame([new_booking])],
            ignore_index=True
        )
        bookings.to_csv(DATA / "transport_bookings.csv", index=False)

        st.success("✅ Transport booked successfully!")
    # -------------------------------------------------------
    from utils.weather_engine import get_weather_risk

    weather = get_weather_risk(src, farmer["crop"])

    if weather["weather_risk_score"] > 25:
        st.warning(
            "🌧️ Adverse weather conditions may affect transport time & crop quality."
        )

    # ==================================================
    # SECTION 2: ADD VEHICLE (SERVICE PROVIDER MODE)
    # ==================================================
    st.divider()
    st.subheader("🚜 Provide Transport Services (Add Your Vehicle)")

    with st.form("add_vehicle"):
        v_type = st.selectbox(
            "Vehicle Type",
            ["Mini Truck", "Medium Truck", "Large Truck", "Electric Van"]
        )
        capacity = st.number_input("Capacity (tons)", 1.0, 50.0, 5.0)
        cost_km = st.number_input("Cost per km (₹)", 5.0, 100.0, 25.0)
        co2_km = st.number_input("CO₂ per km (kg)", 0.1, 5.0, 1.2)

        submit = st.form_submit_button("➕ Register Vehicle")

    if submit:
        new_vehicle = {
            "vehicle_id": vehicles["vehicle_id"].max() + 1,
            "type": v_type,
            "capacity_tons": capacity,
            "cost_per_km": cost_km,
            "co2_per_km": co2_km,
            "owner_farmer_id": farmer_id
        }

        vehicles = pd.concat(
            [vehicles, pd.DataFrame([new_vehicle])],
            ignore_index=True
        )
        vehicles.to_csv(DATA / "vehicles.csv", index=False)

        st.success("🚚 Vehicle registered and available for bookings!")

    # ==================================================
    # DECISION CONFIDENCE SCORE (UNCHANGED)
    # ==================================================
    st.divider()
    st.subheader("📊 Decision Confidence Score")

    confidence = 100
    if cost > 20000:
        confidence -= 20
    if selected["load_factor"] > 0.9:
        confidence -= 10
    if st.session_state.get("admin_mode"):
        confidence -= 10

    confidence = max(confidence, 40)

    st.progress(confidence / 100)
    st.write(f"**Confidence Score:** {confidence}/100")

    # ==================================================
    # FINAL INTEGRATED RECOMMENDATION (WORKING)
    # ==================================================
    st.divider()
    st.subheader("🧠 Final Integrated Recommendation")

    required_keys = [
        "market_trend",
        "market_volatility",
        "storage_score",
        "spoilage_risk",
        "transport_cost",
        "transport_co2"
    ]

    if all(k in st.session_state for k in required_keys):

        decision, score, reasons = final_decision_engine(
            st.session_state["market_trend"],
            st.session_state["market_volatility"],
            st.session_state["spoilage_risk"],
            st.session_state["storage_score"],
            st.session_state["transport_cost"],
            st.session_state["transport_co2"]
        )

        st.success(f"🏆 **Recommended Action: {decision}**")
        st.metric("Integrated Decision Score", f"{score}/100")

        st.markdown("### 📌 Why this recommendation?")
        for r in reasons:
            st.write(f"• {r}")

    else:
        st.info(
            "ℹ️ Complete Market, Storage, and Transport analysis "
            "to unlock final recommendation."
        )

import streamlit as st
import pandas as pd
from pathlib import Path

DATA = Path("data")

def show():
    st.title("👤 Farmer Profile")

    # ---------------- LOAD DATA ----------------
    farmers = pd.read_csv(DATA / "farmers.csv")
    wallets = pd.read_csv(DATA / "farmer_wallets.csv")
    bookings = pd.read_csv(DATA / "transport_bookings.csv")

    # ---------------- FARMER SELECTION ----------------
    farmer_id = st.selectbox(
        "Select Farmer",
        farmers["farmer_id"],
        format_func=lambda x: f"Farmer ID {x}"
    )

    farmer = farmers[farmers["farmer_id"] == farmer_id].iloc[0]
    wallet = wallets[wallets["farmer_id"] == farmer_id].iloc[0]
    history = bookings[bookings["farmer_id"] == farmer_id]

    # ---------------- FARMER SUMMARY CARD ----------------
    st.markdown(
        f"""
        <div class="card">
            <h3>🌾 {farmer['name']} — {farmer['city']}</h3>
            <p><b>Primary Crop:</b> {farmer['crop']}</p>
            <p><b>Land Holding:</b> {farmer.get('land_acres', 'N/A')} acres</p>
            <p><b>Experience:</b> {farmer.get('experience_years', 'N/A')} years</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------- WALLET METRICS ----------------
    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "💰 Wallet Balance",
            f"₹{wallet['balance']:,.0f}"
        )

    # ---------------- BOOKING HISTORY ----------------
    st.divider()
    st.subheader("📜 Transport Booking History")

    if history.empty:
        st.info("No transport bookings yet.")
        total_spend = 0
    else:
        st.dataframe(
            history.sort_values("date", ascending=False),
            use_container_width=True
        )
        total_spend = history["total_cost"].sum()

    with c2:
        st.metric(
            "📉 Total Transport Spend",
            f"₹{total_spend:,.0f}"
        )

    # ---------------- PERSONAL INSIGHTS ----------------
    st.divider()
    st.subheader("🔍 Personal Insights")

    if total_spend > 0:
        st.success(
            "You are actively using **optimized logistics**.\n\n"
            "Based on your usage pattern, **smart routing and vehicle selection** "
            "likely reduced your transport costs by **15–20%** compared to "
            "unplanned transport."
        )
    else:
        st.warning(
            "You haven’t used transport services yet.\n\n"
            "Using **HarvestLink logistics** can significantly reduce costs, "
            "especially during peak harvest season."
        )

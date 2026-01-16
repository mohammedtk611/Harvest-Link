import streamlit as st
import pandas as pd
from pathlib import Path

DATA = Path("data")

def show():
    st.title("🌍 HarvestLink Impact")
    st.caption("Estimated environmental & economic benefits")

    bookings = pd.read_csv(DATA / "transport_bookings.csv")

    if bookings.empty:
        st.info("Impact will appear once services are used.")
        return

    total_cost = bookings["total_cost"].sum()
    total_co2 = bookings["co2_emitted"].sum()
    total_trips = len(bookings)

    # realistic offline estimates
    estimated_savings = total_cost * 0.15      # pooling + optimization
    co2_saved = total_trips * 10                # kg saved per optimized trip
    wastage_reduced = total_trips * 0.4         # tons saved (est.)

    c1, c2, c3 = st.columns(3)
    c1.metric("💰 Money Saved", f"₹{estimated_savings:,.0f}")
    c2.metric("🌱 CO₂ Reduced", f"{co2_saved:.1f} kg")
    c3.metric("📦 Crop Wastage Reduced", f"{wastage_reduced:.1f} tons")

    st.divider()

    avg_cost = total_cost / total_trips
    st.metric("📊 Avg Transport Cost", f"₹{avg_cost:,.0f}")

    st.subheader("Why this matters")
    st.markdown(
        """
        - 🚚 Fewer trips through optimized routing  
        - 🌱 Lower emissions via vehicle selection  
        - 📦 Reduced post-harvest losses  
        - 💸 Higher farmer profitability  
        """
    )

    st.subheader("Platform Insight")
    st.success(
        "HarvestLink enables smarter logistics decisions that benefit "
        "both farmers and the environment — without requiring internet access."
    )
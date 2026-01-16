# from utils.weather_engine import get_weather_risk
# import streamlit as st
# import pandas as pd
# from pathlib import Path

# DATA = Path("data")

# def show():
#     st.title("🏬 Smart Storage Recommendation")
#     st.caption("Predictive, explainable & crop-aware storage intelligence")

#     # --------------------------------------------------
#     # LOAD DATA
#     # --------------------------------------------------
#     storage = pd.read_csv(DATA / "cold_storage.csv")
#     crops = pd.read_csv(DATA / "crop_profiles.csv")
#     reviews = pd.read_csv(DATA / "storage_reviews.csv")

#     # --------------------------------------------------
#     # USER INPUT
#     # --------------------------------------------------
#     crop = st.selectbox("🌾 Crop Type", sorted(crops["crop"].unique()))
#     city = st.selectbox("📍 Your City", sorted(storage["city"].unique()))
#     qty = st.number_input("📦 Quantity (tons)", min_value=0.5, step=0.5)

#     # --------------------------------------------------
#     # FILTER SUITABLE STORAGES
#     # --------------------------------------------------
#     options = storage[
#         (storage["crop_supported"] == crop) &
#         (storage["available_tons"] >= qty)
#     ].copy()

#     if options.empty:
#         st.error("❌ No suitable storage found for selected crop & quantity.")
#         return

#     # --------------------------------------------------
#     # DISTANCE (OFFLINE-SAFE)
#     # --------------------------------------------------
#     options["distance_km"] = options["city"].apply(
#         lambda x: 0 if x == city else 150
#     )

#     # --------------------------------------------------
#     # COST & UTILIZATION
#     # --------------------------------------------------
#     options["daily_cost"] = options["price_per_ton_per_day"] * qty
#     options["utilization_pct"] = (
#         (options["capacity_tons"] - options["available_tons"]) /
#         options["capacity_tons"]
#     ) * 100
#     # ------------------------------------------------------
#     weather = get_weather_risk(city, crop)

#     st.info(
#         f"🌤️ Weather Insight — "
#         f"Temp: {weather['temperature_c']}°C | "
#         f"Humidity: {weather['humidity_pct']}%"
#     )
#     # --------------------------------------------------
#     # SPOILAGE RISK ENGINE
#     # --------------------------------------------------
#     crop_row = crops[crops["crop"] == crop].iloc[0]
#     safe_days = crop_row["safe_days"]

#     def spoilage_risk(util):
#         if safe_days <= 3 or util > 85:
#             return "High"
#         elif safe_days <= 7 or util > 65:
#             return "Medium"
#         return "Low"

#     options["spoilage_risk"] = options["utilization_pct"].apply(spoilage_risk)
#     options["weather_risk"] = weather["weather_risk_score"]
#     options["final_score"] += options["weather_risk"] / 100

#     # --------------------------------------------------
#     # 7-DAY CONGESTION PREDICTION
#     # --------------------------------------------------
#     options["projected_util_7d"] = options["utilization_pct"] + 8

#     def congestion_risk(x):
#         if x > 90:
#             return "High"
#         elif x > 75:
#             return "Medium"
#         return "Low"

#     options["congestion_risk"] = options["projected_util_7d"].apply(congestion_risk)

#     # --------------------------------------------------
#     # TRUST SCORE (REVIEWS)
#     # --------------------------------------------------
#     avg_reviews = (
#         reviews.groupby("storage_id")["rating"]
#         .mean()
#         .reset_index(name="avg_rating")
#     )

#     options = options.merge(avg_reviews, on="storage_id", how="left")
#     options["avg_rating"] = options["avg_rating"].fillna(3.0)
#     options["trust_score"] = options["avg_rating"] * 20  # /100

#     # --------------------------------------------------
#     # MULTI-OBJECTIVE SCORING
#     # --------------------------------------------------
#     options["cost_score"] = options["daily_cost"] / options["daily_cost"].max()
#     options["distance_score"] = options["distance_km"] / options["distance_km"].max()
#     options["util_score"] = options["utilization_pct"] / 100
#     options["congestion_score"] = options["projected_util_7d"] / 100

#     options["final_score"] = (
#         0.35 * options["cost_score"] +
#         0.25 * options["distance_score"] +
#         0.2 * options["util_score"] +
#         0.1 * options["congestion_score"] +
#         0.1 * (1 - options["trust_score"] / 100)
#     )

#     ranked = options.sort_values("final_score")
#     best = ranked.iloc[0]

#     # ==================================================
#     # ✅ ADD JUST AFTER THIS (CRITICAL INTEGRATION)
#     # ==================================================
#     st.session_state["storage_score"] = round(best["final_score"], 3)
#     st.session_state["spoilage_risk"] = best["spoilage_risk"]

#     # --------------------------------------------------
#     # EXPLAINABLE RECOMMENDATION
#     # --------------------------------------------------
#     st.subheader("🏆 Best Recommended Storage")

#     st.success(
#         f"""
#         **Storage Name:** {best['storage_name']}  
#         **City:** {best['city']}  
#         **Daily Cost:** ₹{best['daily_cost']:.0f}  
#         **Distance:** {best['distance_km']} km  
#         **Utilization:** {best['utilization_pct']:.1f}%  
#         **Spoilage Risk:** {best['spoilage_risk']}  
#         **7-Day Congestion Risk:** {best['congestion_risk']}  
#         **Trust Score:** {best['trust_score']:.0f}/100 ⭐
#         """
#     )

#     st.info(
#         f"""
#         📌 **Why this storage?**
#         • Competitive pricing  
#         • Balanced utilization & congestion forecast  
#         • Safe for **{crop}** for up to {safe_days} days  
#         • Strong farmer trust rating  
#         • Best overall multi-factor score
#         """
#     )

#     # --------------------------------------------------
#     # FULL RANKED LIST
#     # --------------------------------------------------
#     st.subheader("📊 Ranked Storage Options")

#     st.dataframe(
#         ranked[
#             [
#                 "storage_name",
#                 "city",
#                 "available_tons",
#                 "daily_cost",
#                 "distance_km",
#                 "utilization_pct",
#                 "spoilage_risk",
#                 "congestion_risk",
#                 "trust_score",
#                 "final_score"
#             ]
#         ],
#         use_container_width=True
#     )

#     # --------------------------------------------------
#     # FOOTER
#     # --------------------------------------------------
#     st.caption(
#         "⚙️ Powered by crop science, congestion forecasting, "
#         "farmer trust signals & multi-objective optimization"
#     )


from utils.weather_engine import get_weather_risk
import streamlit as st
import pandas as pd
from pathlib import Path

DATA = Path("data")

def show():
    st.title("🏬 Smart Storage Recommendation")
    st.caption("Predictive, explainable & crop-aware storage intelligence")

    # --------------------------------------------------
    # LOAD DATA
    # --------------------------------------------------
    storage = pd.read_csv(DATA / "cold_storage.csv")
    crops = pd.read_csv(DATA / "crop_profiles.csv")
    reviews = pd.read_csv(DATA / "storage_reviews.csv")

    # --------------------------------------------------
    # USER INPUT
    # --------------------------------------------------
    crop = st.selectbox("🌾 Crop Type", sorted(crops["crop"].unique()))
    city = st.selectbox("📍 Your City", sorted(storage["city"].unique()))
    qty = st.number_input("📦 Quantity (tons)", min_value=0.5, step=0.5)

    # --------------------------------------------------
    # FILTER SUITABLE STORAGES
    # --------------------------------------------------
    options = storage[
        (storage["crop_supported"] == crop) &
        (storage["available_tons"] >= qty)
    ].copy()

    if options.empty:
        st.error("❌ No suitable storage found.")
        return

    # --------------------------------------------------
    # DISTANCE (OFFLINE SAFE)
    # --------------------------------------------------
    options["distance_km"] = options["city"].apply(
        lambda x: 0 if x == city else 150
    )

    # --------------------------------------------------
    # COST & UTILIZATION
    # --------------------------------------------------
    options["daily_cost"] = options["price_per_ton_per_day"] * qty
    options["utilization_pct"] = (
        (options["capacity_tons"] - options["available_tons"]) /
        options["capacity_tons"]
    ) * 100

    # --------------------------------------------------
    # WEATHER INTELLIGENCE (GOOGLE-INSPIRED)
    # --------------------------------------------------
    weather = get_weather_risk(city, crop)

    st.info(
        f"🌤️ Weather Insight — "
        f"Temp: {weather['temperature_c']}°C | "
        f"Humidity: {weather['humidity_pct']}%"
    )

    options["weather_risk"] = weather["weather_risk_score"]

    # --------------------------------------------------
    # SPOILAGE RISK
    # --------------------------------------------------
    safe_days = crops[crops["crop"] == crop].iloc[0]["safe_days"]

    def spoilage_risk(util):
        if safe_days <= 3 or util > 85:
            return "High"
        elif safe_days <= 7 or util > 65:
            return "Medium"
        return "Low"

    options["spoilage_risk"] = options["utilization_pct"].apply(spoilage_risk)

    # --------------------------------------------------
    # CONGESTION PREDICTION
    # --------------------------------------------------
    options["projected_util_7d"] = options["utilization_pct"] + 8

    def congestion_risk(x):
        if x > 90:
            return "High"
        elif x > 75:
            return "Medium"
        return "Low"

    options["congestion_risk"] = options["projected_util_7d"].apply(congestion_risk)

    # --------------------------------------------------
    # TRUST SCORE
    # --------------------------------------------------
    avg_reviews = (
        reviews.groupby("storage_id")["rating"]
        .mean()
        .reset_index(name="avg_rating")
    )

    options = options.merge(avg_reviews, on="storage_id", how="left")
    options["avg_rating"] = options["avg_rating"].fillna(3.0)
    options["trust_score"] = options["avg_rating"] * 20

    # --------------------------------------------------
    # MULTI-OBJECTIVE SCORING (FINAL SCORE CREATED HERE)
    # --------------------------------------------------
    options["cost_score"] = options["daily_cost"] / options["daily_cost"].max()
    options["distance_score"] = options["distance_km"] / options["distance_km"].max()
    options["util_score"] = options["utilization_pct"] / 100
    options["congestion_score"] = options["projected_util_7d"] / 100

    options["final_score"] = (
        0.32 * options["cost_score"] +
        0.22 * options["distance_score"] +
        0.18 * options["util_score"] +
        0.13 * options["congestion_score"] +
        0.10 * (1 - options["trust_score"] / 100) +
        0.05 * (options["weather_risk"] / 100)   # ✅ WEATHER ADDED CORRECTLY
    )

    ranked = options.sort_values("final_score")
    best = ranked.iloc[0]

    # --------------------------------------------------
    # SESSION STATE (FOR FINAL DECISION ENGINE)
    # --------------------------------------------------
    st.session_state["storage_score"] = round(best["final_score"], 3)
    st.session_state["spoilage_risk"] = best["spoilage_risk"]

    # --------------------------------------------------
    # DISPLAY RESULT
    # --------------------------------------------------
    st.subheader("🏆 Best Recommended Storage")

    st.success(
        f"""
        **Storage:** {best['storage_name']}  
        **City:** {best['city']}  
        **Daily Cost:** ₹{best['daily_cost']:.0f}  
        **Distance:** {best['distance_km']} km  
        **Utilization:** {best['utilization_pct']:.1f}%  
        **Spoilage Risk:** {best['spoilage_risk']}  
        **Congestion Risk:** {best['congestion_risk']}  
        **Trust Score:** {best['trust_score']:.0f}/100 ⭐
        """
    )

    st.subheader("📊 Ranked Storage Options")
    st.dataframe(
        ranked[
            [
                "storage_name",
                "city",
                "available_tons",
                "daily_cost",
                "distance_km",
                "utilization_pct",
                "spoilage_risk",
                "congestion_risk",
                "trust_score",
                "final_score"
            ]
        ],
        use_container_width=True
    )

    st.caption(
        "⚙️ Weather-aware, trust-driven, predictive decision system "
        "(Google-inspired climate intelligence)"
    )

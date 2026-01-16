import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from pathlib import Path

DATA = Path("data")

def show():
    st.title("📊 Advanced Market Intelligence")
    st.caption("Data-driven, explainable & farmer-centric market analysis")

    # --------------------------------------------------
    # LOAD DATA
    # --------------------------------------------------
    prices = pd.read_csv(
        DATA / "market_prices.csv",
        parse_dates=["date"]
    )

    crop = st.selectbox("🌾 Crop", prices["crop"].unique())
    mandi = st.selectbox("🏬 Mandi", prices["mandi"].unique())

    df = prices[
        (prices["crop"] == crop) &
        (prices["mandi"] == mandi)
    ].sort_values("date").reset_index(drop=True)

    if len(df) < 30:
        st.error("❌ Not enough historical data for analysis.")
        return

    # --------------------------------------------------
    # FEATURE ENGINEERING
    # --------------------------------------------------
    df["MA_7"] = df["price_per_quintal"].rolling(7).mean()
    df["MA_30"] = df["price_per_quintal"].rolling(30).mean()
    df["MA_90"] = df["price_per_quintal"].rolling(90).mean()

    # Daily returns
    df["returns"] = df["price_per_quintal"].pct_change()

    # Volatility (rolling)
    df["volatility_14"] = df["returns"].rolling(14).std() * 100

    # --------------------------------------------------
    # MOMENTUM (RSI-LIKE, OFFLINE)
    # --------------------------------------------------
    delta = df["price_per_quintal"].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = -delta.clip(upper=0).rolling(14).mean()
    rs = gain / loss
    df["momentum"] = 100 - (100 / (1 + rs))

    # --------------------------------------------------
    # FORECAST (EXPLAINABLE REGRESSION)
    # --------------------------------------------------
    x = np.arange(len(df))
    y = df["price_per_quintal"].values
    coef = np.polyfit(x, y, 1)
    trend_slope = coef[0]

    future_days = 14
    future_x = np.arange(len(df), len(df) + future_days)
    forecast = coef[0] * future_x + coef[1]

    forecast_df = pd.DataFrame({
        "date": pd.date_range(df["date"].iloc[-1], periods=future_days + 1, freq="D")[1:],
        "forecast_price": forecast
    })

    # --------------------------------------------------
    # MARKET RISK SCORE (0–100)
    # --------------------------------------------------
    risk_score = min(
        100,
        (df["volatility_14"].iloc[-1] * 5)
    )

    # --------------------------------------------------
    # VISUALIZATION
    # --------------------------------------------------
    base = alt.Chart(df).encode(x="date:T")

    price_line = base.mark_line(color="#4cc9f0").encode(
        y="price_per_quintal:Q",
        tooltip=["date", "price_per_quintal"]
    )

    ma7 = base.mark_line(strokeDash=[4,2], color="#90dbf4").encode(y="MA_7:Q")
    ma30 = base.mark_line(strokeDash=[6,3], color="#fcbf49").encode(y="MA_30:Q")

    forecast_line = alt.Chart(forecast_df).mark_line(
        color="#e63946", strokeDash=[5,3]
    ).encode(
        x="date:T",
        y="forecast_price:Q"
    )

    st.altair_chart(
        (price_line + ma7 + ma30 + forecast_line).properties(height=420),
        use_container_width=True
    )

    # --------------------------------------------------
    # DECISION ENGINE (THIS IS THE VALUE)
    # --------------------------------------------------
    latest_price = df["price_per_quintal"].iloc[-1]
    momentum = df["momentum"].iloc[-1]

    st.subheader("🧠 Smart Market Decision")

    if trend_slope > 2 and momentum < 70 and risk_score < 60:
        decision = "STORE"
        reason = "Uptrend detected with manageable risk."
        color = "🟢"
    elif momentum > 75:
        decision = "SELL"
        reason = "Market is overheated (overbought zone)."
        color = "🔴"
    elif risk_score > 70:
        decision = "HOLD"
        reason = "High volatility – wait for stability."
        color = "🟡"
    else:
        decision = "WAIT"
        reason = "No strong signal. Monitor closely."
        color = "🟠"

    st.success(
        f"""
        {color} **Recommended Action: {decision}**

        • Current Price: ₹{latest_price:.0f}/quintal  
        • Trend Strength: {trend_slope:.2f}  
        • Momentum Index: {momentum:.1f}/100  
        • Market Risk Score: {risk_score:.0f}/100  

        📌 **Reason:** {reason}
        """
    )

    # --------------------------------------------------
    # DEEP INSIGHTS
    # --------------------------------------------------
    st.subheader("📌 Market Insights")

    col1, col2, col3 = st.columns(3)

    col1.metric("📉 Volatility (14d)", f"{df['volatility_14'].iloc[-1]:.2f}%")
    col2.metric("📈 Momentum", f"{momentum:.1f}/100")
    col3.metric("⚠️ Risk Score", f"{risk_score:.0f}/100")

    # --------------------------------------------------
    # EXPORT (FARMER FRIENDLY)
    # --------------------------------------------------
    st.download_button(
        "⬇️ Download Market Analysis",
        df.to_csv(index=False),
        file_name=f"{crop}_{mandi}_market_analysis.csv",
        mime="text/csv"
    )

    st.caption(
        "⚙️ Powered by statistical learning, trend decomposition & risk analytics "
        "(offline-first, explainable AI for farmers)"
    )

def final_decision_engine(
    market_trend,
    market_volatility,
    spoilage_risk,
    storage_score,
    transport_cost,
    transport_co2
):
    score = 0
    reasons = []

    # ---- Market logic ----
    if market_trend > 2 and market_volatility < 150:
        score += 30
        reasons.append("Market prices are rising with low volatility")
    elif market_trend < -2:
        score -= 25
        reasons.append("Market prices are declining")

    # ---- Storage logic ----
    if spoilage_risk == "Low":
        score += 25
        reasons.append("Low spoilage risk for selected storage")
    elif spoilage_risk == "High":
        score -= 30
        reasons.append("High spoilage risk detected")

    # ---- Transport logic ----
    if transport_cost < 15000:
        score += 20
        reasons.append("Transport cost is economical")

    if transport_co2 < 500:
        score += 10
        reasons.append("Low CO₂ footprint")

    # ---- Final decision ----
    if score >= 60:
        decision = "STORE & WAIT"
    elif score >= 30:
        decision = "SELL PARTIALLY"
    else:
        decision = "SELL IMMEDIATELY"

    return decision, score, reasons

import random

def get_weather_risk(city, crop):
    """
    Simulated output inspired by Google Weather datasets
    Offline-safe, explainable
    """

    # Simulated climate sensitivity
    heat_sensitive = ["Tomato", "Apple", "Potato"]
    humidity_sensitive = ["Onion", "Orange"]

    base_temp = random.uniform(18, 35)
    humidity = random.uniform(40, 85)

    risk = 0

    if crop in heat_sensitive and base_temp > 30:
        risk += 20

    if crop in humidity_sensitive and humidity > 70:
        risk += 15

    if base_temp > 35:
        risk += 10

    risk = min(risk, 40)

    return {
        "temperature_c": round(base_temp, 1),
        "humidity_pct": round(humidity, 1),
        "weather_risk_score": risk
    }

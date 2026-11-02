"""
AgriSense - Rule-Based Irrigation Advisory Service
Provides transparent, agronomic irrigation recommendations based on:
- Crop water requirement profile (from structured crop library)
- Current ambient temperature and relative humidity (atmospheric evaporative demand)
- Recent rainfall and immediate rain forecast
- Soil texture and visual surface moisture observation
Clearly documents reasoning, priority, and physical limitations.
"""

from app.services.crop_data import get_crop_by_id

SOIL_WATER_RETENTION = {
    "clay": {"name": "Clay / Heavy Soil", "retention": "High", "drainage": "Slow", "evap_multiplier": 0.8},
    "loam": {"name": "Loam / Medium Soil", "retention": "Moderate", "drainage": "Good", "evap_multiplier": 1.0},
    "sandy": {"name": "Sandy / Light Soil", "retention": "Low", "drainage": "Very Fast", "evap_multiplier": 1.3}
}

SURFACE_MOISTURE_STATES = {
    "dry_cracked": {"label": "Dry & Hard / Surface Cracks", "stress_factor": 1.5, "desc": "Severe topsoil moisture depletion"},
    "dry_loose": {"label": "Dry Surface Layer (2-3 cm dry)", "stress_factor": 1.2, "desc": "Moderate surface drying"},
    "slightly_moist": {"label": "Slightly Moist Under Surface", "stress_factor": 0.8, "desc": "Adequate root moisture reserve"},
    "wet_saturated": {"label": "Saturated / Visible Wet Soil", "stress_factor": 0.1, "desc": "High moisture content, risk of waterlogging"}
}

def calculate_irrigation_advice(crop_id, temperature, humidity, rainfall_recent=0.0, rain_forecast_next_48h=0.0, soil_type="loam", surface_state="dry_loose"):
    """
    Computes rule-based irrigation recommendation with transparent logic.
    """
    crop_info = get_crop_by_id(crop_id)
    crop_name = crop_info["name"] if crop_info else (crop_id.capitalize() if crop_id else "General Field Crop")
    crop_water_req = crop_info.get("water_requirement", "Moderate") if crop_info else "Moderate"

    soil_spec = SOIL_WATER_RETENTION.get(soil_type.lower(), SOIL_WATER_RETENTION["loam"])
    moisture_spec = SURFACE_MOISTURE_STATES.get(surface_state.lower(), SURFACE_MOISTURE_STATES["dry_loose"])

    temp = float(temperature) if temperature is not None else 25.0
    humid = float(humidity) if humidity is not None else 60.0
    recent_rain = float(rainfall_recent) if rainfall_recent is not None else 0.0
    forecast_rain = float(rain_forecast_next_48h) if rain_forecast_next_48h is not None else 0.0

    # Atmospheric evaporative demand index (VPD proxy)
    # Higher temperature + lower humidity = intense evapotranspiration
    evap_demand = (temp * (100 - humid)) / 100.0

    reasons = []
    warnings = []

    # Priority determination rules
    if forecast_rain >= 15.0:
        priority = "None / Hold"
        recommendation = "Delay Irrigation — Significant Rain Forecasted"
        action = f"Hold off irrigation for the next 24-48 hours. A forecasted precipitation of {forecast_rain:.1f} mm will adequately replenish soil moisture."
        reasons.append(f"Upcoming weather forecast shows {forecast_rain:.1f} mm rain within 48 hours.")
        warnings.append("Applying irrigation immediately before heavy rainfall risks field waterlogging, nutrient leaching, and root rot.")
    elif recent_rain >= 20.0 or surface_state == "wet_saturated":
        priority = "None"
        recommendation = "No Irrigation Needed — Soil Saturated"
        action = "Soil has received substantial recent moisture. Ensure field drainage canals are clear."
        reasons.append(f"Recent rainfall ({recent_rain:.1f} mm) or visual saturation indicates field capacity is satisfied.")
    elif moisture_spec["stress_factor"] >= 1.5 or (temp > 35 and humid < 40 and crop_water_req in ["High", "Very High"]):
        priority = "High"
        recommendation = "Immediate Irrigation Advised"
        action = f"Apply immediate irrigation to {crop_name}, preferably during early morning or late evening hours to minimize evaporative loss."
        reasons.append(f"Soil shows {moisture_spec['label']}.")
        if temp > 33:
            reasons.append(f"High ambient temperature ({temp:.1f} °C) accelerates crop evapotranspiration.")
        if crop_water_req in ["High", "Very High"]:
            reasons.append(f"{crop_name} is in a high water-demand category.")
    elif moisture_spec["stress_factor"] >= 1.2 or (evap_demand > 18.0 and soil_type == "sandy"):
        priority = "Moderate"
        recommendation = "Scheduled Light Irrigation Recommended"
        action = "Provide a measured irrigation within the next 24-36 hours, focusing on root zone depth."
        reasons.append(f"{soil_spec['name']} exhibits {soil_spec['drainage'].lower()} drainage with moderate moisture drying.")
        if evap_demand > 15:
            reasons.append(f"Warm, dry air (Vapor Deficit Proxy: {evap_demand:.1f}) is drawing moisture from the topsoil.")
    else:
        priority = "Low"
        recommendation = "Maintain Normal Monitoring"
        action = "Soil moisture reserves remain adequate for the present crop stage. Check again in 48 hours."
        reasons.append(f"Balanced atmospheric conditions ({temp:.1f} °C, {humid:.0f}% humidity) and stable soil conditions.")

    if temp >= 38.0:
        warnings.append("Extreme heat condition: Avoid midday surface irrigation which can scald plants and waste up to 40% of water through solar evaporation.")
    if soil_type == "clay" and priority in ["High", "Moderate"]:
        warnings.append("Clay soil notice: Apply water at a controlled rate to prevent water pooling on the surface.")

    # Water efficiency tip
    best_practice = (
        "Adopt drip or micro-sprinkler irrigation where possible. Drip application conserves up to 45% water compared to furrow flooding "
        "and delivers moisture directly to root zones without wetting foliage."
    )

    return {
        "success": True,
        "crop": crop_name,
        "recommendation": recommendation,
        "priority": priority,
        "priority_badge": "danger" if priority == "High" else ("warning" if priority == "Moderate" else "success"),
        "action": action,
        "evaporative_demand_index": round(evap_demand, 1),
        "reasons": reasons,
        "warnings": warnings,
        "best_practice": best_practice,
        "parameters": {
            "temperature": temp,
            "humidity": humid,
            "recent_rainfall": recent_rain,
            "forecast_rain": forecast_rain,
            "soil_type": soil_spec["name"],
            "surface_state": moisture_spec["label"],
            "crop_water_req": crop_water_req
        },
        "disclaimer": "This is a rule-based agronomic advisory model. It provides seasonal guidance based on weather forecasts and surface observations, not real-time dielectric soil moisture sensors."
    }

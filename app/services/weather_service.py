"""
AgriSense - Weather & Geocoding Service
Integrates Open-Meteo Weather and Geocoding APIs with:
- Search by city, district, postal code
- Reverse geocoding for browser coordinates
- Current conditions (temperature, humidity, precipitation, wind speed, condition)
- 7-day agricultural forecast with daily highs, lows, and rain probability
- Agricultural weather alerts (frost, heat stress, fungal disease risk)
- Resilient error handling and fallback states
"""

import requests
from datetime import datetime

WMO_WEATHER_CODES = {
    0: {"description": "Clear Sky", "icon": "sun", "badge": "success"},
    1: {"description": "Mainly Clear", "icon": "sun-cloud", "badge": "success"},
    2: {"description": "Partly Cloudy", "icon": "cloud-sun", "badge": "info"},
    3: {"description": "Overcast", "icon": "cloud", "badge": "neutral"},
    45: {"description": "Fog", "icon": "smog", "badge": "neutral"},
    48: {"description": "Depositing Rime Fog", "icon": "smog", "badge": "neutral"},
    51: {"description": "Light Drizzle", "icon": "cloud-rain", "badge": "info"},
    53: {"description": "Moderate Drizzle", "icon": "cloud-rain", "badge": "info"},
    55: {"description": "Dense Drizzle", "icon": "cloud-rain", "badge": "warning"},
    61: {"description": "Slight Rain", "icon": "cloud-rain", "badge": "info"},
    63: {"description": "Moderate Rain", "icon": "cloud-showers-heavy", "badge": "primary"},
    65: {"description": "Heavy Rain", "icon": "cloud-showers-heavy", "badge": "warning"},
    71: {"description": "Slight Snow Fall", "icon": "snowflake", "badge": "warning"},
    73: {"description": "Moderate Snow Fall", "icon": "snowflake", "badge": "warning"},
    75: {"description": "Heavy Snow Fall", "icon": "snowflake", "badge": "danger"},
    80: {"description": "Slight Rain Showers", "icon": "cloud-rain", "badge": "info"},
    81: {"description": "Moderate Rain Showers", "icon": "cloud-showers-heavy", "badge": "primary"},
    82: {"description": "Violent Rain Showers", "icon": "cloud-showers-heavy", "badge": "danger"},
    95: {"description": "Thunderstorm", "icon": "bolt", "badge": "danger"},
    96: {"description": "Thunderstorm with Slight Hail", "icon": "cloud-bolt", "badge": "danger"},
    99: {"description": "Thunderstorm with Heavy Hail", "icon": "cloud-bolt", "badge": "danger"}
}

def get_weather_condition(code):
    return WMO_WEATHER_CODES.get(code, {"description": "Variable Conditions", "icon": "cloud", "badge": "neutral"})

def search_locations(query):
    """
    Searches location coordinates using Open-Meteo Geocoding API.
    """
    if not query or len(query.strip()) < 2:
        return {"success": False, "error": "Search query must be at least 2 characters."}

    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": query.strip(),
        "count": 5,
        "language": "en",
        "format": "json"
    }

    try:
        resp = requests.get(url, params=params, timeout=8)
        resp.raise_for_status()
        data = resp.json()
        results = []
        for item in data.get("results", []):
            label_parts = [item.get("name")]
            if item.get("admin2"):
                label_parts.append(item.get("admin2"))
            if item.get("admin1"):
                label_parts.append(item.get("admin1"))
            if item.get("country"):
                label_parts.append(item.get("country"))
            
            results.append({
                "name": item.get("name"),
                "display_name": ", ".join(label_parts),
                "latitude": item.get("latitude"),
                "longitude": item.get("longitude"),
                "country": item.get("country"),
                "admin1": item.get("admin1"),
                "elevation": item.get("elevation")
            })

        return {"success": True, "results": results}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Geocoding service unavailable: {str(e)}"}

def reverse_geocode(lat, lon):
    """
    Converts browser coordinates into human-readable location label.
    """
    try:
        url = "https://api.bigdatacloud.net/data/reverse-geocode-client"
        params = {"latitude": lat, "longitude": lon, "localityLanguage": "en"}
        resp = requests.get(url, params=params, timeout=6)
        if resp.status_code == 200:
            data = resp.json()
            city = data.get("city") or data.get("locality") or data.get("principalSubdivision") or "Detected Location"
            country = data.get("countryName", "")
            state = data.get("principalSubdivision", "")
            parts = [p for p in [city, state, country] if p]
            return ", ".join(parts)
    except Exception:
        pass
    return f"Farm at ({lat:.2f}°, {lon:.2f}°)"

def fetch_weather_forecast(lat, lon, location_name=None):
    """
    Fetches real-time weather and 7-day forecast for the specified coordinates.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,weather_code,wind_speed_10m,wind_direction_10m",
        "hourly": "temperature_2m,relative_humidity_2m,precipitation_probability,precipitation",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max",
        "timezone": "auto"
    }

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        raw = resp.json()

        current_data = raw.get("current", {})
        daily_data = raw.get("daily", {})
        hourly_data = raw.get("hourly", {})

        current_code = current_data.get("weather_code", 0)
        cond = get_weather_condition(current_code)

        temp = current_data.get("temperature_2m")
        humidity = current_data.get("relative_humidity_2m")
        precip = current_data.get("precipitation", 0.0)
        wind_speed = current_data.get("wind_speed_10m")

        # Agricultural alerts based on meteorological principles
        alerts = []
        if temp is not None:
            if temp <= 4.0:
                alerts.append({"type": "frost", "level": "danger", "title": "Frost Hazard Alert", "message": "Near-freezing temperatures may injure tender crop canopies. Protect saplings and consider light frost irrigation."})
            elif temp >= 38.0:
                alerts.append({"type": "heat", "level": "warning", "title": "Extreme Heat Stress", "message": "High evapotranspiration rate. Maintain adequate soil moisture to protect crops from floral abortion and heat wilt."})

        if humidity is not None and temp is not None and humidity >= 85 and temp >= 22:
            alerts.append({"type": "disease", "level": "info", "title": "Fungal & Blight Risk", "message": "High humidity coupled with warm temperatures creates favorable incubation conditions for fungal foliar pathogens."})

        if precip is not None and precip >= 25.0:
            alerts.append({"type": "flood", "level": "warning", "title": "Heavy Precipitation Alert", "message": "Substantial rainfall observed. Check field drainage channels to prevent waterlogging and root asphyxiation."})

        # Process 7-day daily forecast
        daily_forecast = []
        dates = daily_data.get("time", [])
        for i in range(min(len(dates), 7)):
            d_code = daily_data.get("weather_code", [])[i] if i < len(daily_data.get("weather_code", [])) else 0
            d_cond = get_weather_condition(d_code)
            d_obj = datetime.strptime(dates[i], "%Y-%m-%d")
            daily_forecast.append({
                "date": dates[i],
                "day_name": d_obj.strftime("%a"),
                "date_formatted": d_obj.strftime("%b %d"),
                "max_temp": daily_data.get("temperature_2m_max", [])[i] if i < len(daily_data.get("temperature_2m_max", [])) else None,
                "min_temp": daily_data.get("temperature_2m_min", [])[i] if i < len(daily_data.get("temperature_2m_min", [])) else None,
                "precipitation_sum": daily_data.get("precipitation_sum", [])[i] if i < len(daily_data.get("precipitation_sum", [])) else 0.0,
                "rain_prob": daily_data.get("precipitation_probability_max", [])[i] if i < len(daily_data.get("precipitation_probability_max", [])) else 0,
                "wind_max": daily_data.get("wind_speed_10m_max", [])[i] if i < len(daily_data.get("wind_speed_10m_max", [])) else None,
                "condition": d_cond["description"],
                "icon": d_cond["icon"]
            })

        # Process next 24 hours trend
        hourly_trend = []
        h_times = hourly_data.get("time", [])
        for i in range(min(len(h_times), 24)):
            h_obj = datetime.fromisoformat(h_times[i])
            hourly_trend.append({
                "time": h_obj.strftime("%H:%M"),
                "temp": hourly_data.get("temperature_2m", [])[i],
                "humidity": hourly_data.get("relative_humidity_2m", [])[i],
                "rain_prob": hourly_data.get("precipitation_probability", [])[i],
                "precip": hourly_data.get("precipitation", [])[i]
            })

        resolved_name = location_name or reverse_geocode(lat, lon)

        return {
            "success": True,
            "location": {
                "name": resolved_name,
                "latitude": round(lat, 4),
                "longitude": round(lon, 4),
                "timezone": raw.get("timezone", "UTC"),
                "elevation": raw.get("elevation", 0)
            },
            "current": {
                "temperature": temp,
                "apparent_temperature": current_data.get("apparent_temperature"),
                "humidity": humidity,
                "precipitation": precip,
                "wind_speed": wind_speed,
                "wind_direction": current_data.get("wind_direction_10m"),
                "condition": cond["description"],
                "icon": cond["icon"],
                "badge": cond["badge"],
                "is_day": bool(current_data.get("is_day", 1)),
                "last_updated": current_data.get("time", datetime.now().isoformat())
            },
            "alerts": alerts,
            "daily_forecast": daily_forecast,
            "hourly_trend": hourly_trend,
            "source": "Open-Meteo Weather API",
            "critical_note": "Current precipitation measures immediate atmospheric rainfall and is displayed for field operations. It does not replace the seasonal accumulated rainfall parameter used in long-term crop modeling."
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"Failed to retrieve weather data from Open-Meteo: {str(e)}",
            "location": {"name": location_name or f"Coords: {lat:.2f}, {lon:.2f}", "latitude": lat, "longitude": lon}
        }

"""
AgriSense - REST API Routes
Provides JSON endpoints for all 11 core features:
- Crop recommendation ML inference
- Soil health evaluation
- Open-Meteo weather and geocoding
- Irrigation advisory
- Fertilizer advisory
- Crop library and calendar
- Crop suitability comparison
- Farming history (SQLite persistence)
- Machine learning performance metrics
- Gemini AI agricultural chat
"""

import os
import json
from flask import Blueprint, request, jsonify
from app.ml.predict import predict_crop, VALIDATION_RANGES
from app.services.soil_service import analyze_soil_health
from app.services.weather_service import fetch_weather_forecast, search_locations
from app.services.irrigation_service import calculate_irrigation_advice
from app.services.fertilizer_service import generate_fertilizer_advice
from app.services.crop_data import get_all_crops, get_crop_by_id, search_crops
from app.services.comparison_service import compare_crops
from app.services.calendar_service import get_crop_calendar
from app.services.gemini_service import send_chat_message
from app.database.db import (
    save_recommendation_history,
    get_all_history,
    delete_history_record,
    get_history_summary,
    set_preference,
    get_preference
)

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.route("/predict", methods=["POST"])
def api_predict_crop():
    data = request.get_json() or {}
    result = predict_crop(data)

    # Automatically save to history if requested and successful
    if result.get("success") and data.get("save_history", True):
        rec_data = {
            "field_name": data.get("field_name", "Primary Plot"),
            "crop_recommended": result["recommended_crop"],
            "confidence": result["confidence"],
            "nitrogen": result["input_summary"]["N"],
            "phosphorus": result["input_summary"]["P"],
            "potassium": result["input_summary"]["K"],
            "temperature": result["input_summary"]["temperature"],
            "humidity": result["input_summary"]["humidity"],
            "ph": result["input_summary"]["ph"],
            "rainfall": result["input_summary"]["rainfall"],
            "location_name": data.get("location_name", "Local Field"),
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
            "selected_crop": data.get("selected_crop", result["recommended_crop"]),
            "notes": data.get("notes", "Model inference prediction")
        }
        try:
            record_id = save_recommendation_history(rec_data)
            result["saved_record_id"] = record_id
        except Exception as e:
            result["save_error"] = str(e)

    status_code = 200 if result.get("success") else 400
    return jsonify(result), status_code

@api_bp.route("/soil-health", methods=["POST"])
def api_soil_health():
    data = request.get_json() or {}
    try:
        n = data.get("nitrogen", data.get("N"))
        p = data.get("phosphorus", data.get("P"))
        k = data.get("potassium", data.get("K"))
        ph = data.get("ph")

        if any(v is None for v in [n, p, k, ph]):
            return jsonify({"success": False, "error": "Please provide nitrogen, phosphorus, potassium, and ph."}), 400

        result = analyze_soil_health(n, p, k, ph)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@api_bp.route("/weather", methods=["GET"])
def api_weather():
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)
    loc_name = request.args.get("name", type=str)

    if lat is None or lon is None:
        # Default fallback to central India (Nagpur)
        lat = 21.1458
        lon = 79.0882
        loc_name = "Central Agricultural Region (Default)"

    result = fetch_weather_forecast(lat, lon, loc_name)
    status_code = 200 if result.get("success") else 500
    return jsonify(result), status_code

@api_bp.route("/geocode", methods=["GET"])
def api_geocode():
    q = request.args.get("q", "")
    res = search_locations(q)
    return jsonify(res)

@api_bp.route("/irrigation", methods=["POST"])
def api_irrigation():
    data = request.get_json() or {}
    crop_id = data.get("crop_id", "rice")
    temp = data.get("temperature", 25.0)
    humid = data.get("humidity", 65.0)
    recent_rain = data.get("recent_rainfall", 0.0)
    forecast_rain = data.get("forecast_rain_48h", 0.0)
    soil_type = data.get("soil_type", "loam")
    surface_state = data.get("surface_state", "dry_loose")

    res = calculate_irrigation_advice(crop_id, temp, humid, recent_rain, forecast_rain, soil_type, surface_state)
    return jsonify(res)

@api_bp.route("/fertilizer", methods=["POST"])
def api_fertilizer():
    data = request.get_json() or {}
    try:
        n = data.get("nitrogen", data.get("N", 50))
        p = data.get("phosphorus", data.get("P", 50))
        k = data.get("potassium", data.get("K", 50))
        ph = data.get("ph", 6.5)
        crop_id = data.get("crop_id")
        res = generate_fertilizer_advice(n, p, k, ph, crop_id)
        return jsonify(res)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@api_bp.route("/crops", methods=["GET"])
def api_crops_list():
    query = request.args.get("q")
    category = request.args.get("category")
    season = request.args.get("season")
    crops = search_crops(query, category, season)
    return jsonify({"success": True, "count": len(crops), "crops": crops})

@api_bp.route("/crops/<crop_id>", methods=["GET"])
def api_crop_detail(crop_id):
    crop = get_crop_by_id(crop_id)
    if not crop:
        return jsonify({"success": False, "error": "Crop not found"}), 404
    return jsonify({"success": True, "crop": crop})

@api_bp.route("/calendar/<crop_id>", methods=["GET"])
def api_calendar(crop_id):
    res = get_crop_calendar(crop_id)
    status_code = 200 if res.get("success") else 404
    return jsonify(res), status_code

@api_bp.route("/compare", methods=["POST"])
def api_compare():
    data = request.get_json() or {}
    crop_ids = data.get("crop_ids", ["rice", "maize"])
    params = data.get("farm_params", {})
    res = compare_crops(crop_ids, params)
    return jsonify(res)

@api_bp.route("/history", methods=["GET", "POST"])
def api_history():
    if request.method == "POST":
        data = request.get_json() or {}
        try:
            record_id = save_recommendation_history(data)
            return jsonify({"success": True, "id": record_id}), 201
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 400

    limit = request.args.get("limit", 50, type=int)
    records = get_all_history(limit)
    summary = get_history_summary()
    return jsonify({"success": True, "records": records, "summary": summary})

@api_bp.route("/history/<int:record_id>", methods=["DELETE"])
def api_delete_history(record_id):
    deleted = delete_history_record(record_id)
    if deleted:
        return jsonify({"success": True, "message": "Record deleted"})
    return jsonify({"success": False, "error": "Record not found"}), 404

@api_bp.route("/ml-metrics", methods=["GET"])
def api_ml_metrics():
    metrics_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "saved_models",
        "ml_metrics.json"
    )
    if not os.path.exists(metrics_path):
        return jsonify({"success": False, "error": "ML metrics not generated yet. Run train.py first."}), 404
    
    with open(metrics_path, "r") as f:
        metrics = json.load(f)
    return jsonify({"success": True, "metrics": metrics})

@api_bp.route("/chat", methods=["POST"])
def api_chat():
    data = request.get_json() or {}
    message = data.get("message", "")
    history = data.get("history", [])
    farm_context = data.get("context", {})

    response = send_chat_message(message, history, farm_context)
    status_code = 200 if response.get("success") else 500
    return jsonify(response), status_code

@api_bp.route("/preferences", methods=["GET", "POST"])
def api_preferences():
    if request.method == "POST":
        data = request.get_json() or {}
        for k, v in data.items():
            set_preference(k, v)
        return jsonify({"success": True})
    
    key = request.args.get("key")
    if key:
        val = get_preference(key)
        return jsonify({"key": key, "value": val})
    
    return jsonify({"error": "Key required"}), 400

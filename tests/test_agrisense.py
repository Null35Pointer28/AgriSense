"""
AgriSense - Comprehensive Automated Test Suite
Covers:
1. ML inference and input range validation
2. Soil health assessment
3. Weather API condition mapping and error resilience
4. Irrigation advisor rule-based logic
5. Fertilizer advisor recommendations
6. Crop library integrity (22 crops)
7. Crop comparison algorithm
8. Crop calendar service
9. SQLite database CRUD operations
10. Flask API endpoints and Gemini key validation
"""

import os
import json
import pytest
from app import create_app
from app.ml.predict import predict_crop, validate_inputs
from app.services.soil_service import analyze_soil_health, interpret_ph
from app.services.irrigation_service import calculate_irrigation_advice
from app.services.fertilizer_service import generate_fertilizer_advice
from app.services.crop_data import get_all_crops, get_crop_by_id, search_crops
from app.services.comparison_service import compare_crops
from app.services.calendar_service import get_crop_calendar
from app.services.weather_service import get_weather_condition
from app.database.db import (
    save_recommendation_history,
    get_all_history,
    delete_history_record,
    get_history_summary
)
from app.services.gemini_service import send_chat_message

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

# ==============================================================================
# 1. Machine Learning & Crop Prediction Tests
# ==============================================================================
def test_valid_crop_prediction():
    sample_input = {
        "N": 90, "P": 42, "K": 43,
        "temperature": 21.0, "humidity": 82.0, "ph": 6.5, "rainfall": 202.0
    }
    result = predict_crop(sample_input)
    assert result["success"] is True
    assert result["recommended_crop"] == "rice"
    assert result["confidence"] > 50.0
    assert "explanation" in result
    assert isinstance(result["alternatives"], list)

def test_crop_prediction_out_of_bounds():
    invalid_input = {
        "N": 999,  # out of realistic agricultural bounds
        "P": 42, "K": 43,
        "temperature": 21.0, "humidity": 82.0, "ph": 6.5, "rainfall": 202.0
    }
    result = predict_crop(invalid_input)
    assert result["success"] is False
    assert any("outside realistic agricultural bounds" in err for err in result["errors"])

def test_crop_prediction_missing_parameter():
    missing_input = {
        "N": 50, "P": 50
        # missing other mandatory fields
    }
    result = predict_crop(missing_input)
    assert result["success"] is False
    assert len(result["errors"]) >= 5

# ==============================================================================
# 2. Soil Health Analysis Tests
# ==============================================================================
def test_soil_health_neutral_balanced():
    result = analyze_soil_health(nitrogen=60, phosphorus=45, potassium=50, ph=6.8)
    assert result["success"] is True
    assert result["overall_score"] >= 75
    assert result["ph_analysis"]["status"] == "Optimal / Neutral"
    assert result["nutrients"]["N"]["status"] == "Optimal / Sufficient"

def test_soil_health_acidic_deficient():
    result = analyze_soil_health(nitrogen=15, phosphorus=10, potassium=15, ph=4.8)
    assert result["success"] is True
    assert "Acidic" in result["ph_analysis"]["status"]
    assert result["nutrients"]["N"]["status"] == "Deficient / Low"
    assert len(result["improvement_plan"]) >= 2

def test_ph_interpretation():
    assert interpret_ph(4.5)["status"] == "Strongly Acidic"
    assert interpret_ph(6.8)["status"] == "Optimal / Neutral"
    assert interpret_ph(8.8)["status"] == "Strongly Alkaline / Sodic"

# ==============================================================================
# 3. Weather Service & Condition Mapping
# ==============================================================================
def test_weather_condition_mapping():
    clear = get_weather_condition(0)
    assert clear["description"] == "Clear Sky"
    rain = get_weather_condition(63)
    assert "Rain" in rain["description"]
    unknown = get_weather_condition(9999)
    assert "Variable" in unknown["description"]

# ==============================================================================
# 4. Irrigation Advisor Tests
# ==============================================================================
def test_irrigation_advisor_rain_forecast_delay():
    # If heavy rain forecasted, irrigation should be delayed
    advice = calculate_irrigation_advice(
        crop_id="rice",
        temperature=28.0,
        humidity=70.0,
        rainfall_recent=0.0,
        rain_forecast_next_48h=25.0,
        soil_type="clay",
        surface_state="dry_loose"
    )
    assert advice["success"] is True
    assert "Delay" in advice["recommendation"]
    assert advice["priority"] == "None / Hold"

def test_irrigation_advisor_high_heat_stress():
    advice = calculate_irrigation_advice(
        crop_id="banana",
        temperature=39.0,
        humidity=25.0,
        rainfall_recent=0.0,
        rain_forecast_next_48h=0.0,
        soil_type="sandy",
        surface_state="dry_cracked"
    )
    assert advice["success"] is True
    assert advice["priority"] == "High"
    assert len(advice["warnings"]) >= 1

# ==============================================================================
# 5. Fertilizer Advisor Tests
# ==============================================================================
def test_fertilizer_advisor_deficient_n():
    result = generate_fertilizer_advice(nitrogen=20, phosphorus=50, potassium=50, ph=6.5)
    assert result["success"] is True
    n_diag = next(d for d in result["diagnostics"] if "Nitrogen" in d["nutrient"])
    assert n_diag["status"] == "Deficient"
    assert len(result["recommended_fertilizers"]) >= 1

# ==============================================================================
# 6. Crop Library Catalog Integrity
# ==============================================================================
def test_crop_library_completeness():
    all_crops = get_all_crops()
    assert len(all_crops) == 22
    for crop in all_crops:
        assert "id" in crop
        assert "name" in crop
        assert "scientific_name" in crop
        assert "season" in crop
        assert "duration_days" in crop
        assert "stages" in crop
        assert len(crop["stages"]) >= 3

def test_crop_search():
    res = search_crops(query="rice")
    assert len(res) >= 1
    assert res[0]["id"] == "rice"

# ==============================================================================
# 7. Crop Suitability Comparison Tests
# ==============================================================================
def test_crop_comparison():
    params = {"N": 90, "P": 42, "K": 43, "temperature": 21, "humidity": 82, "ph": 6.5, "rainfall": 202}
    result = compare_crops(["rice", "cotton", "coffee"], params)
    assert result["success"] is True
    assert len(result["crops"]) == 3
    # Rice should rank top given its identical match to inputs
    assert result["crops"][0]["id"] == "rice"
    assert result["crops"][0]["suitability_score"] > result["crops"][2]["suitability_score"]

# ==============================================================================
# 8. Crop Calendar Tests
# ==============================================================================
def test_crop_calendar():
    cal = get_crop_calendar("maize")
    assert cal["success"] is True
    assert cal["crop_name"] == "Maize (Corn)"
    assert len(cal["stages"]) >= 4
    assert len(cal["operations"]) == 6

# ==============================================================================
# 9. SQLite Database Persistence Tests
# ==============================================================================
def test_database_crud():
    sample_rec = {
        "field_name": "Pytest Experimental Field",
        "crop_recommended": "chickpea",
        "confidence": 98.5,
        "nitrogen": 40.0,
        "phosphorus": 60.0,
        "potassium": 50.0,
        "temperature": 19.5,
        "humidity": 55.0,
        "ph": 7.0,
        "rainfall": 65.0,
        "location_name": "Automated Test Plot",
        "notes": "Pytest verified record"
    }
    rec_id = save_recommendation_history(sample_rec)
    assert rec_id > 0

    all_recs = get_all_history(10)
    found = any(r["id"] == rec_id for r in all_recs)
    assert found is True

    summary = get_history_summary()
    assert summary["total_records"] >= 1

    deleted = delete_history_record(rec_id)
    assert deleted is True

# ==============================================================================
# 10. Flask API Endpoints & Gemini Error Handling
# ==============================================================================
def test_api_index(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"AgriSense" in res.data

def test_api_predict_endpoint(client):
    payload = {
        "N": 80, "P": 40, "K": 40,
        "temperature": 22, "humidity": 80, "ph": 6.5, "rainfall": 190,
        "save_history": False
    }
    res = client.post("/api/predict", data=json.dumps(payload), content_type="application/json")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "recommended_crop" in data

def test_api_crops_endpoint(client):
    res = client.get("/api/crops")
    assert res.status_code == 200
    data = res.get_json()
    assert data["count"] == 22

def test_api_ml_metrics_endpoint(client):
    res = client.get("/api/ml-metrics")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["metrics"]["dataset_info"]["total_samples"] == 2200

def test_gemini_unconfigured_error(monkeypatch):
    """
    Verifies that when GEMINI_API_KEY is not configured or empty,
    the application safely returns a descriptive configuration error without crashing.
    """
    monkeypatch.setenv("GEMINI_API_KEY", "")
    res = send_chat_message("Hello AgriSense")
    assert res["success"] is False
    assert "API key is not configured" in res["error"]

def test_gemini_integration_when_configured():
    """
    Verifies that when a real API key is configured in .env,
    the service safely handles the request, returning either an AI-generated
    reply or a gracefully handled network/rate-limit error without unhandled exceptions.
    """
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if api_key and api_key != "your_actual_api_key_here":
        res = send_chat_message("Hello AgriSense")
        assert "success" in res
        if res["success"]:
            assert "reply" in res and len(res["reply"]) > 0
        else:
            assert "error" in res

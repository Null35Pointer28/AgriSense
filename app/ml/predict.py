"""
AgriSense - Crop Prediction Engine
Loads the trained Random Forest model pipeline and performs:
- Input parameter validation against realistic agricultural bounds
- Multiclass probability prediction (confidence score)
- Top recommended crop + alternative suggestions
- Transparent agronomic explanation
- Clear limitations notice
"""

import os
import joblib
import numpy as np
import pandas as pd

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "saved_models", "crop_recommendation_model.joblib")

# Feature validation boundaries based on agronomic bounds and dataset bounds
VALIDATION_RANGES = {
    "N": {"min": 0, "max": 200, "unit": "kg/ha", "desc": "Nitrogen ratio in soil"},
    "P": {"min": 0, "max": 200, "unit": "kg/ha", "desc": "Phosphorus ratio in soil"},
    "K": {"min": 0, "max": 300, "unit": "kg/ha", "desc": "Potassium ratio in soil"},
    "temperature": {"min": 4.0, "max": 52.0, "unit": "°C", "desc": "Ambient temperature"},
    "humidity": {"min": 5.0, "max": 100.0, "unit": "%", "desc": "Relative humidity"},
    "ph": {"min": 3.0, "max": 10.5, "unit": "pH", "desc": "Soil pH level"},
    "rainfall": {"min": 5.0, "max": 500.0, "unit": "mm", "desc": "Seasonal rainfall"}
}

_model_cache = None

def load_model():
    global _model_cache
    if _model_cache is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}. Please run train.py first.")
        _model_cache = joblib.load(MODEL_PATH)
    return _model_cache

def validate_inputs(params):
    """
    Validates input parameters against acceptable agricultural ranges.
    Returns (cleaned_params, errors_list).
    """
    cleaned = {}
    errors = []

    for key, spec in VALIDATION_RANGES.items():
        if key not in params or params[key] is None or params[key] == "":
            errors.append(f"Missing parameter '{key}' ({spec['desc']}).")
            continue
        try:
            val = float(params[key])
            if val < spec["min"] or val > spec["max"]:
                errors.append(
                    f"Parameter '{key}' ({val} {spec['unit']}) is outside realistic agricultural bounds "
                    f"[{spec['min']} - {spec['max']} {spec['unit']}]."
                )
            cleaned[key] = val
        except (ValueError, TypeError):
            errors.append(f"Invalid numeric value for '{key}': {params[key]}")

    return cleaned, errors

def generate_crop_explanation(crop_name, inputs):
    """
    Generates agronomic explanation for why the crop matches the given inputs.
    """
    n, p, k = inputs["N"], inputs["P"], inputs["K"]
    t, h, ph, r = inputs["temperature"], inputs["humidity"], inputs["ph"], inputs["rainfall"]

    crop_name_clean = crop_name.capitalize()
    reasons = []

    if r > 180:
        reasons.append(f"high seasonal water availability ({r:.1f} mm)")
    elif r < 60:
        reasons.append(f"drought tolerance under low rainfall conditions ({r:.1f} mm)")
    else:
        reasons.append(f"moderate water demand ({r:.1f} mm rainfall)")

    if t > 28:
        reasons.append(f"warm thermal conditions ({t:.1f} °C)")
    elif t < 20:
        reasons.append(f"cool weather adaptability ({t:.1f} °C)")
    else:
        reasons.append(f"temperate-to-tropical range ({t:.1f} °C)")

    if ph < 5.5:
        reasons.append("acidic soil suitability")
    elif ph > 7.5:
        reasons.append("alkaline soil resilience")
    else:
        reasons.append("balanced neutral soil pH")

    if n > 70:
        reasons.append("high nitrogen feeding requirement")
    if p > 60:
        reasons.append("high phosphorus root-development profile")
    if k > 70:
        reasons.append("heavy potassium fruiting/flowering requirement")

    summary_text = (
        f"{crop_name_clean} is recommended primarily due to its alignment with your farm's "
        + ", ".join(reasons[:3]) + "."
    )
    return summary_text

def predict_crop(params):
    """
    Predicts the top recommended crop, alternatives, confidence, and validation.
    """
    cleaned_params, errors = validate_inputs(params)
    if errors:
        return {
            "success": False,
            "errors": errors
        }

    model_data = load_model()
    pipeline = model_data["pipeline"]
    feature_cols = model_data["features"]

    input_df = pd.DataFrame([{col: cleaned_params[col] for col in feature_cols}])

    probabilities = pipeline.predict_proba(input_df)[0]
    classes = pipeline.classes_

    # Sort descending by probability
    ranked_indices = np.argsort(probabilities)[::-1]
    
    top_index = ranked_indices[0]
    top_crop = classes[top_index]
    top_confidence = round(float(probabilities[top_index]) * 100, 2)

    # Top 3 alternative crops with confidence >= 0.5%
    alternatives = []
    for idx in ranked_indices[1:4]:
        prob = round(float(probabilities[idx]) * 100, 2)
        if prob > 0.1:
            alternatives.append({
                "crop": classes[idx],
                "confidence": prob
            })

    explanation = generate_crop_explanation(top_crop, cleaned_params)

    return {
        "success": True,
        "recommended_crop": top_crop,
        "confidence": top_confidence,
        "input_summary": cleaned_params,
        "explanation": explanation,
        "alternatives": alternatives,
        "model_used": model_data.get("model_name", "Random Forest Classifier"),
        "disclaimer": "Agricultural recommendation based on machine learning modeling. Actual yield depends on local microclimates, seed varieties, pest control, and physical soil depth."
    }

if __name__ == "__main__":
    # Test sample prediction
    test_input = {
        "N": 90, "P": 42, "K": 43,
        "temperature": 21.0, "humidity": 82.0, "ph": 6.5, "rainfall": 202.0
    }
    res = predict_crop(test_input)
    print("Test Prediction Result:", res)

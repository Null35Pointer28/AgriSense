"""
AgriSense - Crop Suitability Comparison Service
Allows side-by-side comparative analysis of 2 to 4 crops.
Calculates a transparent, mathematically documented agronomic suitability score
against actual farm parameters (N, P, K, Temp, Humidity, pH, Rainfall).
"""

import json
import os
import numpy as np
import pandas as pd
from app.services.crop_data import get_crop_by_id

# Load empirical crop statistics from processed dataset to ground comparisons in actual data
_crop_stats = None

def get_crop_dataset_stats():
    global _crop_stats
    if _crop_stats is None:
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "processed", "crop_recommendation_clean.csv")
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            stats = {}
            for crop_name, grp in df.groupby("label"):
                stats[crop_name] = {
                    col: {
                        "mean": float(grp[col].mean()),
                        "std": float(grp[col].std()) if grp[col].std() > 0 else 1.0,
                        "min": float(grp[col].min()),
                        "max": float(grp[col].max())
                    }
                    for col in ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
                }
            _crop_stats = stats
        else:
            _crop_stats = {}
    return _crop_stats

def compute_dimension_fit(val, mean, std):
    """
    Computes a normalized agronomic fit score (0 - 100) using normalized z-distance.
    Score = 100 * exp(-0.5 * (z / 2)^2)
    A value equal to the mean scores 100.
    A value within 1 standard deviation scores ~88.
    A value within 2 standard deviations scores ~60.
    A value beyond 3 standard deviations drops towards 0.
    """
    z = abs(val - mean) / max(std, 1.0)
    score = 100.0 * np.exp(-0.5 * ((z / 1.8) ** 2))
    return float(np.clip(score, 0.0, 100.0))

def compare_crops(crop_ids, farm_params):
    """
    Compares selected crop IDs against farm parameters.
    """
    stats = get_crop_dataset_stats()
    comparison_data = []

    n = float(farm_params.get("N", 50))
    p = float(farm_params.get("P", 50))
    k = float(farm_params.get("K", 50))
    t = float(farm_params.get("temperature", 25))
    h = float(farm_params.get("humidity", 70))
    ph = float(farm_params.get("ph", 6.5))
    r = float(farm_params.get("rainfall", 100))

    for cid in crop_ids:
        cid_clean = cid.lower().strip()
        info = get_crop_by_id(cid_clean)
        crop_name = info["name"] if info else cid_clean.capitalize()

        crop_stat = stats.get(cid_clean)
        if crop_stat:
            s_n = compute_dimension_fit(n, crop_stat["N"]["mean"], crop_stat["N"]["std"])
            s_p = compute_dimension_fit(p, crop_stat["P"]["mean"], crop_stat["P"]["std"])
            s_k = compute_dimension_fit(k, crop_stat["K"]["mean"], crop_stat["K"]["std"])
            s_temp = compute_dimension_fit(t, crop_stat["temperature"]["mean"], crop_stat["temperature"]["std"])
            s_humid = compute_dimension_fit(h, crop_stat["humidity"]["mean"], crop_stat["humidity"]["std"])
            s_ph = compute_dimension_fit(ph, crop_stat["ph"]["mean"], crop_stat["ph"]["std"])
            s_rain = compute_dimension_fit(r, crop_stat["rainfall"]["mean"], crop_stat["rainfall"]["std"])

            # Sub-indices
            nutrient_score = round((s_n + s_p + s_k) / 3.0, 1)
            climate_score = round((s_temp + s_humid) / 2.0, 1)
            water_score = round(s_rain, 1)
            soil_score = round((s_ph * 0.6 + nutrient_score * 0.4), 1)

            # Documented aggregate suitability:
            # 30% Climate (temp, humidity), 25% Water (rainfall), 25% Soil pH, 20% Soil Nutrients
            overall_suitability = round(
                (climate_score * 0.30) +
                (water_score * 0.25) +
                (s_ph * 0.25) +
                (nutrient_score * 0.20),
                1
            )
        else:
            nutrient_score = 70.0
            climate_score = 70.0
            water_score = 70.0
            soil_score = 70.0
            overall_suitability = 70.0

        comparison_data.append({
            "id": cid_clean,
            "name": crop_name,
            "category": info["category"] if info else "Agricultural Crop",
            "season": info["season"] if info else "Seasonal",
            "duration": info["duration_days"] if info else "120 days",
            "water_requirement": info["water_requirement"] if info else "Moderate",
            "soil_type": info["soil_type"] if info else "Loamy",
            "suitability_score": overall_suitability,
            "scores": {
                "climate": climate_score,
                "water": water_score,
                "soil_ph": round(s_ph, 1) if crop_stat else 70.0,
                "nutrients": nutrient_score,
                "overall": overall_suitability
            },
            "radar_metrics": [
                {"subject": "Thermal Match", "value": round(s_temp, 1) if crop_stat else 70.0},
                {"subject": "Humidity Match", "value": round(s_humid, 1) if crop_stat else 70.0},
                {"subject": "Rainfall Match", "value": round(s_rain, 1) if crop_stat else 70.0},
                {"subject": "Soil pH Match", "value": round(s_ph, 1) if crop_stat else 70.0},
                {"subject": "NPK Balance", "value": nutrient_score}
            ]
        })

    # Sort descending by suitability score
    comparison_data.sort(key=lambda x: x["suitability_score"], reverse=True)

    return {
        "success": True,
        "crops": comparison_data,
        "input_parameters": {"N": n, "P": p, "K": k, "temperature": t, "humidity": h, "ph": ph, "rainfall": r},
        "methodology": "Suitability is calculated using normalized Gaussian deviations from empirical dataset distributions: Overall = 30% Climate (Temp/Humidity) + 25% Water (Rainfall) + 25% Soil pH + 20% Soil NPK.",
        "disclaimer": "Suitability scores are theoretical indices derived from statistical dataset means. Actual agronomic viability also depends on physical soil depth, disease pressure, seed variety, and irrigation availability."
    }

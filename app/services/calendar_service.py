"""
AgriSense - Crop Calendar & Phenology Service
Provides dynamic, crop-specific cultivation timelines:
- Sowing, vegetative, reproductive, and harvesting windows
- Chronological growth stages with duration in days
- Key agricultural operations (tillage, fertilizer splits, pest scouting, irrigation cut-off)
- Seasonal adjustment guidelines for Kharif, Rabi, and Zaid seasons
"""

from app.services.crop_data import get_crop_by_id, CROPS_CATALOG

# General Indian crop seasonality windows
SEASONAL_WINDOWS = {
    "Kharif (Monsoon)": {
        "sowing_months": "June - July",
        "active_months": "July - October",
        "harvesting_months": "October - November",
        "climate_character": "High temperature, monsoon rainfall, high humidity"
    },
    "Rabi (Winter)": {
        "sowing_months": "October - November",
        "active_months": "November - February",
        "harvesting_months": "March - April",
        "climate_character": "Mild warm days, cool nights, residual soil moisture"
    },
    "Zaid (Summer)": {
        "sowing_months": "February - March",
        "active_months": "March - May",
        "harvesting_months": "May - June",
        "climate_character": "Long sunny days, warm to hot temperatures, low humidity"
    },
    "Perennial": {
        "sowing_months": "Monsoon (July - Sept) for orchard planting",
        "active_months": "Year-round vegetative and reproductive maintenance",
        "harvesting_months": "Varies by seasonal bahar / flush",
        "climate_character": "Requires sustained multi-year climate compatibility"
    }
}

def get_crop_calendar(crop_id):
    crop = get_crop_by_id(crop_id)
    if not crop:
        return {"success": False, "error": f"Crop '{crop_id}' not found in library."}

    season_key = None
    for k in SEASONAL_WINDOWS.keys():
        if k.split()[0].lower() in crop["season"].lower():
            season_key = k
            break
    if not season_key:
        season_key = "Perennial" if "Perennial" in crop["season"] else "Kharif (Monsoon)"

    season_info = SEASONAL_WINDOWS[season_key]

    # Build operations schedule
    operations = [
        {
            "step": 1,
            "phase": "Pre-Sowing & Land Preparation",
            "timeframe": "15-20 days before sowing",
            "activities": [
                "Deep summer ploughing to expose soil pests and weed roots to solar heat.",
                "Incorporate 5-10 tonnes/ha well-decomposed Farmyard Manure (FYM).",
                "Level field to ensure uniform irrigation and prevent water stagnation."
            ]
        },
        {
            "step": 2,
            "phase": "Seed Treatment & Sowing",
            "timeframe": "Days 1 - 10",
            "activities": [
                "Treat seed with biological fungicide (Trichoderma) or Rhizobium / Azotobacter inoculants.",
                "Sow at recommended row-to-row spacing and depth into moist soil.",
                "Apply basal dose of Phosphorus (SSP/DAP) and Potassium (MOP)."
            ]
        },
        {
            "step": 3,
            "phase": "Early Vegetative & Weeding",
            "timeframe": "Days 15 - 35",
            "activities": [
                "Perform first hand-weeding or mechanical hoeing to eradicate weed competition.",
                "Thin out excess seedlings to achieve optimum plant population per square meter.",
                "First split application of Nitrogen (Urea) followed by light irrigation."
            ]
        },
        {
            "step": 4,
            "phase": "Flowering & Reproductive Management",
            "timeframe": "Days 45 - 80",
            "activities": [
                "Maintain adequate root-zone soil moisture; avoid water stress during blooming.",
                "Monitor field for sucking pests, leaf caterpillars, or fungal spots; apply neem oil spray as prophylactic.",
                "Second top-dressing of Nitrogen / foliar micronutrient spray if required."
            ]
        },
        {
            "step": 5,
            "phase": "Maturation & Pre-Harvest",
            "timeframe": "10-15 days before harvest",
            "activities": [
                "Withhold irrigation to encourage grain hardening or sugar accumulation in fruits.",
                "Scout for rodent activity and prepare storage / drying yards."
            ]
        },
        {
            "step": 6,
            "phase": "Harvesting & Post-Harvest Handling",
            "timeframe": "At physiological maturity",
            "activities": [
                "Harvest in dry sunny weather when crop reaches moisture threshold.",
                "Thresh, winnow, and sun-dry grains down to safe storage moisture (< 12%).",
                "Store grains in moisture-proof hermetic bags or aerated bins."
            ]
        }
    ]

    return {
        "success": True,
        "crop_id": crop["id"],
        "crop_name": crop["name"],
        "category": crop["category"],
        "duration_days": crop["duration_days"],
        "season": crop["season"],
        "season_details": season_info,
        "stages": crop["stages"],
        "operations": operations,
        "cultivation_tips": crop["cultivation_tips"],
        "disclaimer": "Calendar milestones are approximate averages. Phenological timing may advance or delay by 7-14 days based on seasonal temperatures, altitude, and selected seed variety (early vs. late maturing)."
    }

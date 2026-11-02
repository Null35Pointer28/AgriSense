"""
AgriSense - Fertilizer Advisory Service
Evaluates soil N-P-K reserves and pH chemistry to recommend:
- Nutrient status categorization (Deficient, Balanced, Excessive)
- Suitable organic and mineral fertilizer types with active nutrient ratios
- Application methods and split-dosage strategies
- Critical agronomic cautions and soil health preservation advice
"""

from app.services.crop_data import get_crop_by_id

COMMON_FERTILIZERS = {
    "nitrogen": [
        {"name": "Urea", "composition": "46-0-0 (46% N)", "type": "Chemical", "notes": "High nitrogen source. Apply in 2-3 split doses to prevent volatilization and leaching losses."},
        {"name": "Ammonium Sulfate", "composition": "20.6% N + 24% Sulfur", "type": "Chemical", "notes": "Supplies nitrogen and vital sulfur. Beneficial in alkaline and calcareous soils due to slight acidifying effect."},
        {"name": "Neem Coated Urea (NCU)", "composition": "46% N + Neem Oil coating", "type": "Slow-Release", "notes": "Slows nitrification, reducing nitrate leaching into groundwater and improving nitrogen-use efficiency by 10-15%."}
    ],
    "phosphorus": [
        {"name": "Single Superphosphate (SSP)", "composition": "16% P2O5 + 11% Sulfur + 19% Calcium", "type": "Chemical", "notes": "Premier source of phosphorus and essential secondary nutrients. Best applied as basal dressing during land preparation."},
        {"name": "Diammonium Phosphate (DAP)", "composition": "18-46-0 (18% N, 46% P2O5)", "type": "Chemical", "notes": "Highly concentrated source of phosphorus and starter nitrogen. Place near the seed row at planting."},
        {"name": "Rock Phosphate", "composition": "20-30% P2O5", "type": "Mineral / Organic", "notes": "Slow-acting natural mineral source, particularly effective in acidic soils with pH < 6.0."}
    ],
    "potassium": [
        {"name": "Muriate of Potash (MOP / KCl)", "composition": "60% K2O", "type": "Chemical", "notes": "Standard economical potassium fertilizer. Imparts disease resistance and improves drought resilience."},
        {"name": "Sulfate of Potash (SOP / K2SO4)", "composition": "50% K2O + 17.5% Sulfur", "type": "Chemical / Specialty", "notes": "Chloride-free premium potassium. Ideal for chloride-sensitive crops like grapes, tobacco, and potato."},
        {"name": "Wood Ash", "composition": "5-10% K2O + Micronutrients", "type": "Organic", "notes": "Natural alkaline potash source; also neutralizes acidic soils."}
    ],
    "biofertilizers": [
        {"name": "Phosphate Solubilizing Bacteria (PSB)", "strain": "Bacillus megaterium / Pseudomonas", "benefit": "Secretes organic acids to solubilize fixed soil phosphorus into bioavailable orthophosphate."},
        {"name": "Azotobacter / Azospirillum", "strain": "Free-living / Associative N-fixers", "benefit": "Fixes 15-25 kg N/ha from the atmosphere in non-legume crops (cereals, cotton, vegetables)."},
        {"name": "Rhizobium", "strain": "Symbiotic root nodule bacteria", "benefit": "Essential seed inoculant for pulses and legumes, fixing 40-100 kg atmospheric N/ha."},
        {"name": "Potash Mobilizing Bacteria (KMB)", "strain": "Frateuria aurantia", "benefit": "Mobilizes insoluble potassium locked in clay minerals for plant absorption."}
    ],
    "organic": [
        {"name": "Well-Decomposed Farmyard Manure (FYM)", "dosage": "5 - 10 tonnes/ha", "benefit": "Replenishes soil organic carbon, improves soil porosity, and feeds beneficial mycorrhizal earthworm networks."},
        {"name": "Vermicompost", "dosage": "2 - 4 tonnes/ha", "benefit": "Rich in plant growth hormones (auxins, cytokinins) and immediately accessible micronutrients."},
        {"name": "Neem Seed Cake", "dosage": "250 - 500 kg/ha", "benefit": "Natural organic nutrient source with natural nematicidal properties that repel soil-borne grubs and termites."}
    ]
}

def generate_fertilizer_advice(nitrogen, phosphorus, potassium, ph, crop_id=None):
    n = float(nitrogen)
    p = float(phosphorus)
    k = float(potassium)
    ph_val = float(ph)

    crop_info = get_crop_by_id(crop_id) if crop_id else None
    crop_name = crop_info["name"] if crop_info else "General Crop"

    diagnostics = []
    recommended_fertilizers = []
    organic_recommendations = []
    biofertilizers = []
    cautions = []

    # 1. Nitrogen Assessment
    if n < 40:
        diagnostics.append({
            "nutrient": "Nitrogen (N)",
            "status": "Deficient",
            "badge": "danger",
            "observation": f"Soil nitrogen ({n:.1f} kg/ha) is below optimal. Crop is likely to suffer from stunted growth, pale foliage, and reduced tillering."
        })
        recommended_fertilizers.append({
            "category": "Nitrogenous Supplementation",
            "options": COMMON_FERTILIZERS["nitrogen"][:2],
            "application_strategy": "Basal 33% at sowing, 33% at active tillering, and 33% at flower initiation. Prefer Neem Coated Urea."
        })
    elif n > 110:
        diagnostics.append({
            "nutrient": "Nitrogen (N)",
            "status": "Excessive",
            "badge": "warning",
            "observation": f"Soil nitrogen ({n:.1f} kg/ha) is very high. Risk of vegetative lodging, delayed maturity, and heightened pest/aphid susceptibility."
        })
        cautions.append("Avoid additional chemical nitrogen (Urea/DAP). Allow the crop to exhaust current reserves.")
    else:
        diagnostics.append({
            "nutrient": "Nitrogen (N)",
            "status": "Adequate",
            "badge": "success",
            "observation": f"Soil nitrogen ({n:.1f} kg/ha) is in a healthy maintenance zone."
        })

    # 2. Phosphorus Assessment
    if p < 25:
        diagnostics.append({
            "nutrient": "Phosphorus (P)",
            "status": "Deficient",
            "badge": "danger",
            "observation": f"Soil phosphorus ({p:.1f} kg/ha) is low. Weak root establishment, purpling on leaf undersides, and poor flower set may occur."
        })
        recommended_fertilizers.append({
            "category": "Phosphatic Supplementation",
            "options": COMMON_FERTILIZERS["phosphorus"][:2],
            "application_strategy": "Apply full dose as basal application placed 4-5 cm below seed depth. Phosphorus does not move readily through soil water."
        })
        biofertilizers.append(COMMON_FERTILIZERS["biofertilizers"][0]) # PSB
    elif p > 75:
        diagnostics.append({
            "nutrient": "Phosphorus (P)",
            "status": "High",
            "badge": "info",
            "observation": f"Soil phosphorus ({p:.1f} kg/ha) is abundant. Maintain with minimal basal starter."
        })
    else:
        diagnostics.append({
            "nutrient": "Phosphorus (P)",
            "status": "Adequate",
            "badge": "success",
            "observation": f"Soil phosphorus ({p:.1f} kg/ha) is in the optimal range."
        })

    # 3. Potassium Assessment
    if k < 30:
        diagnostics.append({
            "nutrient": "Potassium (K)",
            "status": "Deficient",
            "badge": "danger",
            "observation": f"Soil potassium ({k:.1f} kg/ha) is low. Leaves may exhibit margin scorching, reduced drought resilience, and weak stem lodging."
        })
        recommended_fertilizers.append({
            "category": "Potassic Supplementation",
            "options": COMMON_FERTILIZERS["potassium"][:2],
            "application_strategy": "Apply 50% basal and 50% at flowering/grain filling to ensure stalk rigidity and fruit quality."
        })
        biofertilizers.append(COMMON_FERTILIZERS["biofertilizers"][3]) # KMB
    else:
        diagnostics.append({
            "nutrient": "Potassium (K)",
            "status": "Adequate",
            "badge": "success",
            "observation": f"Soil potassium ({k:.1f} kg/ha) is sufficient."
        })

    # 4. pH and Micronutrient Interaction
    if ph_val < 5.8:
        cautions.append("Acidic Soil (pH < 5.8): Phosphorus is frequently locked with Aluminum and Iron. Apply agricultural lime and use PSB biofertilizers.")
    elif ph_val > 7.8:
        cautions.append("Alkaline Soil (pH > 7.8): Phosphorus and Zinc availability are depressed. Avoid broadcast DAP; band-place fertilizers and apply Zinc Sulfate.")

    # Organic additions
    organic_recommendations = COMMON_FERTILIZERS["organic"]

    # Legume specific biofertilizers
    if crop_info and crop_info.get("category") == "Pulse / Legume":
        biofertilizers.append(COMMON_FERTILIZERS["biofertilizers"][2]) # Rhizobium
    else:
        biofertilizers.append(COMMON_FERTILIZERS["biofertilizers"][1]) # Azotobacter

    return {
        "success": True,
        "crop_target": crop_name,
        "diagnostics": diagnostics,
        "recommended_fertilizers": recommended_fertilizers,
        "organic_amendments": organic_recommendations,
        "biofertilizers": biofertilizers,
        "cautions": cautions,
        "application_tips": [
            "Never mix Urea and Superphosphate long before application; mix only immediately before broadcasting to avoid caking.",
            "Always apply fertilizers when soil has sufficient moisture; applying concentrated salts to dry soil scorches roots.",
            "Split nitrogen applications match the plant's vegetative demand curves and prevent leaching into water bodies."
        ],
        "disclaimer": "This advisory is based on general agronomic nutrient indexing. Precise kilogram-per-hectare application rates require calibrated soil laboratory testing and local state agricultural university fertilizer dosage charts."
    }

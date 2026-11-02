"""
AgriSense - Soil Health Analysis Service
Analyzes user-entered or sensor soil indicators (N, P, K, pH):
- Computes nutrient rating tiers (Low, Medium, High, Excessive)
- Interprets soil pH and nutrient availability chemistry
- Produces organic and mineral soil amendment recommendations
- Transparently distinguishes user input from laboratory assays
"""

# Benchmark agricultural agronomic thresholds (in kg/ha or rating tiers)
NUTRIENT_THRESHOLDS = {
    "N": {
        "name": "Nitrogen (Available N)",
        "unit": "kg/ha",
        "low": 40,
        "opt_min": 40,
        "opt_max": 80,
        "high": 120,
        "role": "Vegetative canopy development, chlorophyll formation, and leafy biomass growth.",
        "deficiency_symptom": "General yellowing (chlorosis) of older lower leaves, stunted plant height.",
        "excess_risk": "Excess vegetative rank growth, delayed flowering, weak stems prone to lodging, pest susceptibility."
    },
    "P": {
        "name": "Phosphorus (Available P2O5)",
        "unit": "kg/ha",
        "low": 25,
        "opt_min": 25,
        "opt_max": 60,
        "high": 90,
        "role": "Root architecture, early seedling vigor, energy transfer (ATP), and flower/seed setting.",
        "deficiency_symptom": "Purplish or bronze discoloration on older leaf margins, poor root development, delayed maturity.",
        "excess_risk": "Interferes with zinc (Zn) and iron (Fe) micronutrient uptake."
    },
    "K": {
        "name": "Potassium (Available K2O)",
        "unit": "kg/ha",
        "low": 30,
        "opt_min": 30,
        "opt_max": 75,
        "high": 120,
        "role": "Stomatal water regulation, drought tolerance, enzyme activation, and fruit sweetness/disease resistance.",
        "deficiency_symptom": "Marginal scorching or leaf tip browning on older leaves, weak stalks.",
        "excess_risk": "May induce magnesium (Mg) or calcium (Ca) uptake competition in high concentrations."
    }
}

def interpret_ph(ph_val):
    """
    Evaluates soil pH classification and agronomic implications.
    """
    if ph_val < 5.0:
        return {
            "status": "Strongly Acidic",
            "badge": "danger",
            "color": "#ef4444",
            "impact": "Severe phosphorus fixation with aluminum/iron. Micronutrient toxicity (Al, Mn) possible. Beneficial bacterial activity suppressed.",
            "remedy": "Apply agricultural limestone (calcium carbonate, CaCO3) or dolomite at 1-2 tonnes/ha based on buffering capacity to raise pH towards neutral."
        }
    elif ph_val < 6.2:
        return {
            "status": "Moderately Acidic",
            "badge": "warning",
            "color": "#f59e0b",
            "impact": "Slight reduction in phosphorus and molybdenum availability. Suitable for acid-loving crops (tea, potato, coffee) but slightly sub-optimal for legumes.",
            "remedy": "Incorporate well-decomposed farmyard manure (FYM), compost, and light lime dressing before deep tillage."
        }
    elif ph_val <= 7.4:
        return {
            "status": "Optimal / Neutral",
            "badge": "success",
            "color": "#10b981",
            "impact": "Ideal agronomic zone. Maximum availability of primary (N-P-K), secondary (Ca, Mg, S), and essential micronutrients. Favorable soil microbiology.",
            "remedy": "Maintain current soil organic matter levels through crop residue retention and regular compost additions."
        }
    elif ph_val <= 8.2:
        return {
            "status": "Moderately Alkaline (Calcareous)",
            "badge": "warning",
            "color": "#f59e0b",
            "impact": "Phosphorus fixed as insoluble calcium phosphate. Micronutrients like Iron (Fe), Zinc (Zn), and Boron (B) become less bioavailable.",
            "remedy": "Apply agricultural sulfur or iron sulfate, use acid-forming fertilizers (such as ammonium sulfate), and incorporate green manures like Sesbania (Dhaincha)."
        }
    else:
        return {
            "status": "Strongly Alkaline / Sodic",
            "badge": "danger",
            "color": "#ef4444",
            "impact": "Severe nutrient lockup. High exchangeable sodium percentage (ESP) impairs soil physical structure, causing poor water permeability and crusting.",
            "remedy": "Reclamation with agricultural gypsum (calcium sulfate) followed by heavy fresh-water leaching to displace sodium ions into deep drainage."
        }

def analyze_nutrient_level(element, value):
    spec = NUTRIENT_THRESHOLDS[element]
    if value < spec["low"]:
        status = "Deficient / Low"
        badge = "warning"
        score = 35
        advice = f"Sub-optimal {spec['name']}. Plant growth and metabolic vigor may be restricted. Supplemental organic or mineral fertilizer recommended."
    elif value <= spec["opt_max"]:
        status = "Optimal / Sufficient"
        badge = "success"
        score = 90
        advice = f"Favorable {spec['name']} reserve for general crop uptake. Maintain levels with balanced maintenance applications."
    elif value <= spec["high"]:
        status = "High / Rich"
        badge = "info"
        score = 80
        advice = f"Ample {spec['name']} present in root zone. Fertilizer application can be scaled down or deferred to save operational costs."
    else:
        status = "Excessive / Very High"
        badge = "danger"
        score = 50
        advice = f"Excessive {spec['name']}. Potential hazard of nutrient imbalance or leaching runoff into groundwater."

    return {
        "element": element,
        "name": spec["name"],
        "value": value,
        "unit": spec["unit"],
        "status": status,
        "badge": badge,
        "score": score,
        "role": spec["role"],
        "symptoms": spec["deficiency_symptom"],
        "excess_risk": spec["excess_risk"],
        "advice": advice
    }

def analyze_soil_health(nitrogen, phosphorus, potassium, ph):
    """
    Comprehensive soil health diagnosis with safety disclaimers.
    """
    n_res = analyze_nutrient_level("N", float(nitrogen))
    p_res = analyze_nutrient_level("P", float(phosphorus))
    k_res = analyze_nutrient_level("K", float(potassium))
    ph_res = interpret_ph(float(ph))

    # Overall Soil Health Index (0 - 100)
    # Weightings: pH balance 30%, N 25%, P 25%, K 20%
    ph_score = 95 if ph_res["status"] == "Optimal / Neutral" else (65 if "Moderately" in ph_res["status"] else 35)
    overall_score = round(
        (ph_score * 0.30) +
        (n_res["score"] * 0.25) +
        (p_res["score"] * 0.25) +
        (k_res["score"] * 0.20)
    )

    if overall_score >= 80:
        overall_health = "Excellent Fertility"
        health_badge = "success"
    elif overall_score >= 60:
        overall_health = "Good / Moderate Fertility"
        health_badge = "info"
    elif overall_score >= 40:
        overall_health = "Fair / Imbalanced Fertility"
        health_badge = "warning"
    else:
        overall_health = "Poor / Nutrient Depleted"
        health_badge = "danger"

    improvement_plan = []
    if ph_res["status"] != "Optimal / Neutral":
        improvement_plan.append({"title": "pH Amendment", "detail": ph_res["remedy"]})

    if n_res["status"] == "Deficient / Low":
        improvement_plan.append({
            "title": "Nitrogen Enrichment",
            "detail": "Incorporate well-rotted cattle manure or compost (5-10 t/ha). Inoculate seeds with Rhizobium/Azotobacter and consider legume cover cropping."
        })
    elif n_res["status"] == "Excessive / Very High":
        improvement_plan.append({
            "title": "Nitrogen Management",
            "detail": "Withhold chemical nitrogen (urea) applications. Increase irrigation intervals slightly to allow natural crop absorption without vegetative surge."
        })

    if p_res["status"] == "Deficient / Low":
        improvement_plan.append({
            "title": "Phosphorus Enrichment",
            "detail": "Band placement of Single Superphosphate (SSP) or rock phosphate near root zone. Apply Phosphate Solubilizing Bacteria (PSB) biofertilizer."
        })

    if k_res["status"] == "Deficient / Low":
        improvement_plan.append({
            "title": "Potassium Enrichment",
            "detail": "Apply Muriate of Potash (MOP) or wood ash to fortify stalk strength and improve drought resistance."
        })

    improvement_plan.append({
        "title": "Soil Organic Matter (SOM) Preservation",
        "detail": "Practice minimum tillage, retain crop stubble, and apply a 2-3 inch organic mulch to stimulate earthworms and beneficial mycorrhizal fungi."
    })

    return {
        "success": True,
        "input_summary": {
            "nitrogen": float(nitrogen),
            "phosphorus": float(phosphorus),
            "potassium": float(potassium),
            "ph": float(ph)
        },
        "overall_score": overall_score,
        "overall_health": overall_health,
        "health_badge": health_badge,
        "nutrients": {
            "N": n_res,
            "P": p_res,
            "K": k_res
        },
        "ph_analysis": ph_res,
        "improvement_plan": improvement_plan,
        "disclaimer": "Diagnostic evaluation is based on standard agronomic nutrient indexing. This tool does not replace certified laboratory chemical soil tests (spectrophotometry/flame photometry). Validate through your district Krishi Vigyan Kendra (KVK) or soil testing laboratory before large-scale commercial inputs."
    }

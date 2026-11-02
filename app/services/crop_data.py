"""
AgriSense - Structured Crop Information Library & Knowledge Base
Contains detailed, verified agronomic profiles for all 22 crops in the system.
Covers biological classification, climatic requirements, soil preferences,
calendar stages, and cultivation practices.
"""

CROPS_CATALOG = {
    "rice": {
        "id": "rice",
        "name": "Rice (Paddy)",
        "scientific_name": "Oryza sativa",
        "family": "Poaceae",
        "category": "Cereal",
        "season": "Kharif (Monsoon)",
        "duration_days": "115 - 150 days",
        "min_duration": 115,
        "max_duration": 150,
        "soil_type": "Clayey, Clay-loam, Alluvial with high water retention",
        "optimal_ph": "5.5 - 7.5",
        "ph_min": 5.5,
        "ph_max": 7.5,
        "optimal_temp": "20°C - 35°C",
        "temp_min": 20,
        "temp_max": 35,
        "optimal_humidity": "70% - 90%",
        "water_requirement": "Very High",
        "rainfall_range": "150 - 300 mm monthly (1000-2000 mm seasonal)",
        "npk_profile": {"N": "High (80-120)", "P": "Moderate (40-60)", "K": "Moderate (40-60)"},
        "description": "Rice is the primary staple food for over half the world's population. It thrives in warm, humid climates with abundant standing water or assured irrigation, traditionally cultivated under puddled soil conditions.",
        "cultivation_tips": [
            "Puddle the field thoroughly to form an impermeable hardpan that conserves water.",
            "Maintain 2-5 cm shallow standing water during early tillering and panicle initiation.",
            "Apply nitrogen split into 3 doses: basal, active tillering, and panicle initiation."
        ],
        "stages": [
            {"stage": "Land Preparation & Nursery", "days": "Days 1-25", "desc": "Nursery sowing, puddling, bunding and leveling"},
            {"stage": "Transplanting / Tillering", "days": "Days 25-55", "desc": "Seedling transplanting and active tiller formation"},
            {"stage": "Panicle Initiation & Flowering", "days": "Days 55-90", "desc": "Critical water-sensitive reproductive phase"},
            {"stage": "Grain Filling & Dough Stage", "days": "Days 90-120", "desc": "Milk to dough transition, withhold water 10 days before harvest"},
            {"stage": "Harvesting", "days": "Days 120-140", "desc": "Harvest when 80-85% grains turn golden yellow"}
        ]
    },
    "maize": {
        "id": "maize",
        "name": "Maize (Corn)",
        "scientific_name": "Zea mays",
        "family": "Poaceae",
        "category": "Cereal",
        "season": "Kharif / Rabi / Spring",
        "duration_days": "90 - 120 days",
        "min_duration": 90,
        "max_duration": 120,
        "soil_type": "Well-drained deep loamy, alluvial or red soils",
        "optimal_ph": "5.8 - 7.5",
        "ph_min": 5.8,
        "ph_max": 7.5,
        "optimal_temp": "18°C - 32°C",
        "temp_min": 18,
        "temp_max": 32,
        "optimal_humidity": "50% - 75%",
        "water_requirement": "Moderate",
        "rainfall_range": "60 - 110 mm monthly",
        "npk_profile": {"N": "High (70-100)", "P": "Moderate (40-60)", "K": "Moderate (30-50)"},
        "description": "Known as the Queen of Cereals, maize has the highest genetic yield potential among grain crops. Highly intolerant to water stagnation.",
        "cultivation_tips": [
            "Ensure excellent surface drainage; even 24 hours of standing water severely stunts corn roots.",
            "Tasseling and silking are critical moisture stress periods.",
            "Maintain earthing up at knee-high stage to prevent lodging."
        ],
        "stages": [
            {"stage": "Sowing & Germination", "days": "Days 1-12", "desc": "Ridge sowing with good seed-soil contact"},
            {"stage": "Knee-High Stage", "days": "Days 13-35", "desc": "Rapid vegetative growth and earthing-up"},
            {"stage": "Tasseling & Silking", "days": "Days 36-65", "desc": "Pollen shed and silk receptive stage (moisture critical)"},
            {"stage": "Grain Development", "days": "Days 66-95", "desc": "Milking and starch accumulation in cobs"},
            {"stage": "Physiological Maturity", "days": "Days 96-115", "desc": "Black layer formation at grain base"}
        ]
    },
    "chickpea": {
        "id": "chickpea",
        "name": "Chickpea (Gram)",
        "scientific_name": "Cicer arietinum",
        "family": "Fabaceae",
        "category": "Pulse / Legume",
        "season": "Rabi (Winter)",
        "duration_days": "90 - 120 days",
        "min_duration": 90,
        "max_duration": 120,
        "soil_type": "Well-drained medium to heavy black cotton soils or sandy loam",
        "optimal_ph": "6.0 - 8.0",
        "ph_min": 6.0,
        "ph_max": 8.0,
        "optimal_temp": "15°C - 26°C",
        "temp_min": 15,
        "temp_max": 26,
        "optimal_humidity": "40% - 65%",
        "water_requirement": "Low",
        "rainfall_range": "35 - 75 mm",
        "npk_profile": {"N": "Low (20-40, fixes atmospheric N)", "P": "Moderate to High (50-70)", "K": "Moderate (30-50)"},
        "description": "Major cool-season pulse crop. Fixes atmospheric nitrogen through symbiotic Rhizobium root nodules, enriching soil fertility for subsequent crops.",
        "cultivation_tips": [
            "Inoculate seeds with Rhizobium culture before sowing to enhance nodulation.",
            "Avoid over-irrigation; excessive soil moisture causes collar rot and root wilt.",
            "Nip apical buds at 30-40 days to encourage extensive lateral branching."
        ],
        "stages": [
            {"stage": "Sowing & Emergence", "days": "Days 1-10", "desc": "Deep placement in residual moisture"},
            {"stage": "Vegetative & Branching", "days": "Days 11-40", "desc": "Active nodulation and lateral branch growth"},
            {"stage": "Flowering & Podding", "days": "Days 41-75", "desc": "Pink/white blossom and pod formation"},
            {"stage": "Pod Filling", "days": "Days 76-100", "desc": "Grain swelling inside pods"},
            {"stage": "Harvesting", "days": "Days 101-115", "desc": "Leaves turn straw-yellow and dry"}
        ]
    },
    "kidneybeans": {
        "id": "kidneybeans",
        "name": "Kidney Beans (Rajma)",
        "scientific_name": "Phaseolus vulgaris",
        "family": "Fabaceae",
        "category": "Pulse / Legume",
        "season": "Rabi (Plains) / Kharif (Hills)",
        "duration_days": "100 - 130 days",
        "min_duration": 100,
        "max_duration": 130,
        "soil_type": "Rich deep loamy soil with neutral pH and excellent drainage",
        "optimal_ph": "5.5 - 6.8",
        "ph_min": 5.5,
        "ph_max": 6.8,
        "optimal_temp": "15°C - 25°C",
        "temp_min": 15,
        "temp_max": 25,
        "optimal_humidity": "50% - 70%",
        "water_requirement": "Moderate",
        "rainfall_range": "60 - 120 mm",
        "npk_profile": {"N": "Moderate to High (unlike other pulses, poor N-fixer)", "P": "High (50-70)", "K": "Moderate (40-60)"},
        "description": "High-protein pulse requiring mild, frost-free weather. Unlike many legumes, Rajma possesses poor natural nodulation with native Rhizobium and requires starter nitrogen.",
        "cultivation_tips": [
            "Provide basal nitrogen application as natural nodulation is inherently inefficient in Rajma.",
            "Sensitive to both waterlogging and drought; ensure uniform light irrigations.",
            "Keep field weed-free during the first 35 days."
        ],
        "stages": [
            {"stage": "Germination", "days": "Days 1-10", "desc": "Seedling emergence"},
            {"stage": "Vegetative Growth", "days": "Days 11-40", "desc": "Trifoliate leaf canopy development"},
            {"stage": "Flowering", "days": "Days 41-65", "desc": "Inflorescence emergence"},
            {"stage": "Pod Filling", "days": "Days 66-95", "desc": "Bean development inside elongated pods"},
            {"stage": "Maturity", "days": "Days 96-120", "desc": "Pods dry to papery tan color"}
        ]
    },
    "pigeonpeas": {
        "id": "pigeonpeas",
        "name": "Pigeonpeas (Red Gram / Arhar / Tur)",
        "scientific_name": "Cajanus cajan",
        "family": "Fabaceae",
        "category": "Pulse / Legume",
        "season": "Kharif (Monsoon)",
        "duration_days": "150 - 210 days",
        "min_duration": 150,
        "max_duration": 210,
        "soil_type": "Deep well-drained loamy to black cotton soils",
        "optimal_ph": "6.0 - 7.5",
        "ph_min": 6.0,
        "ph_max": 7.5,
        "optimal_temp": "20°C - 35°C",
        "temp_min": 20,
        "temp_max": 35,
        "optimal_humidity": "45% - 70%",
        "water_requirement": "Low to Moderate",
        "rainfall_range": "50 - 100 mm",
        "npk_profile": {"N": "Low (20-30)", "P": "High (50-70)", "K": "Moderate (20-40)"},
        "description": "Deep-rooted, drought-hardy legume widely intercropped with cotton, sorghum, or soybean. Deep taproot penetrates hard subsoil and extracts deep moisture.",
        "cultivation_tips": [
            "Ensure ridge sowing to prevent collar rot during heavy monsoon rains.",
            "Apply phosphorus at sowing to stimulate deep taproot expansion.",
            "Intercrop with short-duration crops like greengram or cowpea for optimal land use."
        ],
        "stages": [
            {"stage": "Establishment", "days": "Days 1-20", "desc": "Slow initial above-ground growth while taproot burrows"},
            {"stage": "Branching & Canopy", "days": "Days 21-80", "desc": "Extensive bushy vegetative development"},
            {"stage": "Flowering", "days": "Days 81-130", "desc": "Copious yellow blossom"},
            {"stage": "Pod Maturation", "days": "Days 131-170", "desc": "Seed development in mottled pods"},
            {"stage": "Harvest", "days": "Days 171-190", "desc": "Whole plant sickle harvest when pods turn brown"}
        ]
    },
    "mothbeans": {
        "id": "mothbeans",
        "name": "Moth Beans (Matki)",
        "scientific_name": "Vigna aconitifolia",
        "family": "Fabaceae",
        "category": "Pulse / Legume",
        "season": "Kharif (Monsoon)",
        "duration_days": "75 - 90 days",
        "min_duration": 75,
        "max_duration": 90,
        "soil_type": "Sandy, marginal desert soils with good drainage",
        "optimal_ph": "5.5 - 7.5",
        "ph_min": 5.5,
        "ph_max": 7.5,
        "optimal_temp": "25°C - 38°C",
        "temp_min": 25,
        "temp_max": 38,
        "optimal_humidity": "35% - 60%",
        "water_requirement": "Very Low",
        "rainfall_range": "30 - 60 mm",
        "npk_profile": {"N": "Low (15-25)", "P": "Moderate (30-50)", "K": "Low to Moderate (20-30)"},
        "description": "The most drought-resistant legume in arid and semi-arid India. Forms a dense mat over the ground, conserving moisture and preventing soil erosion.",
        "cultivation_tips": [
            "Ideal for drought-prone regions and sandy soils.",
            "Minimal fertilizer inputs needed; fixes nitrogen autonomously.",
            "Prevents wind erosion by forming a dense vegetative carpet."
        ],
        "stages": [
            {"stage": "Sowing & Sprouting", "days": "Days 1-7", "desc": "Rapid germination in low moisture"},
            {"stage": "Mat Formation", "days": "Days 8-35", "desc": "Spreading prostrate canopy covering bare ground"},
            {"stage": "Flowering", "days": "Days 36-55", "desc": "Yellow floral cluster development"},
            {"stage": "Pod Filling & Harvest", "days": "Days 56-80", "desc": "Harvesting when pods dry out"}
        ]
    },
    "mungbean": {
        "id": "mungbean",
        "name": "Mung Bean (Green Gram)",
        "scientific_name": "Vigna radiata",
        "family": "Fabaceae",
        "category": "Pulse / Legume",
        "season": "Kharif / Spring / Zaid (Summer)",
        "duration_days": "60 - 75 days",
        "min_duration": 60,
        "max_duration": 75,
        "soil_type": "Well-drained loamy to sandy loam soils",
        "optimal_ph": "6.2 - 7.5",
        "ph_min": 6.2,
        "ph_max": 7.5,
        "optimal_temp": "24°C - 35°C",
        "temp_min": 24,
        "temp_max": 35,
        "optimal_humidity": "50% - 75%",
        "water_requirement": "Low",
        "rainfall_range": "40 - 70 mm",
        "npk_profile": {"N": "Low (15-25)", "P": "Moderate (40-50)", "K": "Low (20-30)"},
        "description": "Short-duration pulse crop that fits perfectly into catch-cropping or relay-cropping windows between major crop rotations.",
        "cultivation_tips": [
            "Use as a summer catch crop following wheat harvest.",
            "Maintain soil moisture at flowering; drought at pod setting causes flower drop.",
            "Incorporate residues back into soil after pod picking to build soil organic carbon."
        ],
        "stages": [
            {"stage": "Emergence", "days": "Days 1-6", "desc": "Rapid sprouting"},
            {"stage": "Vegetative", "days": "Days 7-25", "desc": "Foliage development and early nodulation"},
            {"stage": "Flowering", "days": "Days 26-45", "desc": "Bright yellow blooms"},
            {"stage": "Pod Ripening", "days": "Days 46-65", "desc": "Pods turn black/brown for picking"}
        ]
    },
    "blackgram": {
        "id": "blackgram",
        "name": "Blackgram (Urad)",
        "scientific_name": "Vigna mungo",
        "family": "Fabaceae",
        "category": "Pulse / Legume",
        "season": "Kharif / Rabi / Summer",
        "duration_days": "70 - 85 days",
        "min_duration": 70,
        "max_duration": 85,
        "soil_type": "Medium to heavy soils, black cotton soil with good water capacity",
        "optimal_ph": "6.5 - 7.8",
        "ph_min": 6.5,
        "ph_max": 7.8,
        "optimal_temp": "25°C - 35°C",
        "temp_min": 25,
        "temp_max": 35,
        "optimal_humidity": "55% - 75%",
        "water_requirement": "Low to Moderate",
        "rainfall_range": "50 - 80 mm",
        "npk_profile": {"N": "Low (20-30)", "P": "Moderate to High (40-60)", "K": "Low (20-30)"},
        "description": "Nutritious pulse essential for dal and traditional fermented preparations. Highly valued for nitrogen fixation and soil health enhancement.",
        "cultivation_tips": [
            "Sow on raised beds in high-rainfall zones to prevent waterlogging.",
            "Apply single superphosphate (SSP) to deliver both phosphorus and sulfur.",
            "Harvest promptly when 85% pods turn black to prevent shattering losses."
        ],
        "stages": [
            {"stage": "Sowing & Germination", "days": "Days 1-7", "desc": "Uniform emergence"},
            {"stage": "Vegetative Phase", "days": "Days 8-30", "desc": "Erect hairy stems with trifoliate leaves"},
            {"stage": "Reproductive Phase", "days": "Days 31-55", "desc": "Dense flowering and pod initiation"},
            {"stage": "Pod Maturation", "days": "Days 56-75", "desc": "Pods darken to cylindrical black pods"}
        ]
    },
    "lentil": {
        "id": "lentil",
        "name": "Lentil (Masoor)",
        "scientific_name": "Lens culinaris",
        "family": "Fabaceae",
        "category": "Pulse / Legume",
        "season": "Rabi (Winter)",
        "duration_days": "100 - 130 days",
        "min_duration": 100,
        "max_duration": 130,
        "soil_type": "Light loamy to clay soils, tolerant to marginal soils",
        "optimal_ph": "6.0 - 7.5",
        "ph_min": 6.0,
        "ph_max": 7.5,
        "optimal_temp": "15°C - 24°C",
        "temp_min": 15,
        "temp_max": 24,
        "optimal_humidity": "45% - 65%",
        "water_requirement": "Low",
        "rainfall_range": "35 - 65 mm",
        "npk_profile": {"N": "Low (15-25)", "P": "Moderate (40-50)", "K": "Low (20-30)"},
        "description": "One of the oldest domesticated crops, highly drought and cold tolerant. Valued for easy digestibility and high protein content.",
        "cultivation_tips": [
            "Can be broadcast into standing rice crop as a paira/utera crop to utilize residual soil moisture.",
            "Water stress at podding significantly reduces grain count; provide one light irrigation if winter rain fails.",
            "Harvest before pods become brittle to avoid seed shattering."
        ],
        "stages": [
            {"stage": "Emergence", "days": "Days 1-10", "desc": "Delicate feathery seedling emergence"},
            {"stage": "Vegetative", "days": "Days 11-45", "desc": "Sub-erect branching canopy"},
            {"stage": "Flowering", "days": "Days 46-75", "desc": "Small pale blue/white blossoms"},
            {"stage": "Podding & Drydown", "days": "Days 76-115", "desc": "Small flat pods bearing 1-2 lens-shaped seeds"}
        ]
    },
    "pomegranate": {
        "id": "pomegranate",
        "name": "Pomegranate (Anar)",
        "scientific_name": "Punica granatum",
        "family": "Lythraceae",
        "category": "Fruit / Horticultural",
        "season": "Perennial (Ambe / Mrig / Hasta Bahar)",
        "duration_days": "150 - 180 days per fruiting cycle",
        "min_duration": 150,
        "max_duration": 180,
        "soil_type": "Deep, well-drained loamy to light black soils",
        "optimal_ph": "6.5 - 7.8",
        "ph_min": 6.5,
        "ph_max": 7.8,
        "optimal_temp": "20°C - 38°C",
        "temp_min": 20,
        "temp_max": 38,
        "optimal_humidity": "40% - 65%",
        "water_requirement": "Moderate (Drip)",
        "rainfall_range": "80 - 130 mm",
        "npk_profile": {"N": "Moderate (25-45)", "P": "Low to Moderate (15-30)", "K": "High (40-60)"},
        "description": "Subtropical fruit renowned for antioxidant-rich arils. Thrives in semi-arid zones with hot dry summers and cool winters.",
        "cultivation_tips": [
            "Practice Bahar treatment (withholding water followed by pruning and fertilizer) to regulate flowering.",
            "Adopt drip irrigation to prevent fruit cracking caused by uneven moisture fluctuation.",
            "Bag fruits on tree to guard against pomegranate butterfly (Deudorix isocrates) and bacterial blight."
        ],
        "stages": [
            {"stage": "Water Stress & Defoliation", "days": "Days 1-35", "desc": "Stress period to induce uniform dormancy"},
            {"stage": "Pruning & Irrigation Resumption", "days": "Days 36-50", "desc": "Canopy sanitation and burst of new shoots"},
            {"stage": "Flowering & Fruit Set", "days": "Days 51-85", "desc": "Pollination and setting of calyx"},
            {"stage": "Fruit Development", "days": "Days 86-140", "desc": "Aril expansion and sugar development"},
            {"stage": "Harvesting", "days": "Days 141-170", "desc": "Rind develops deep red blush and hollow sound when tapped"}
        ]
    },
    "banana": {
        "id": "banana",
        "name": "Banana",
        "scientific_name": "Musa acuminata / paradisiaca",
        "family": "Musaceae",
        "category": "Fruit / Commercial",
        "season": "Perennial / Year-round",
        "duration_days": "300 - 365 days (10 - 12 months)",
        "min_duration": 300,
        "max_duration": 365,
        "soil_type": "Rich, deep, loamy soil with high organic matter and superb drainage",
        "optimal_ph": "6.0 - 7.5",
        "ph_min": 6.0,
        "ph_max": 7.5,
        "optimal_temp": "22°C - 35°C",
        "temp_min": 22,
        "temp_max": 35,
        "optimal_humidity": "70% - 90%",
        "water_requirement": "Very High",
        "rainfall_range": "100 - 200 mm monthly",
        "npk_profile": {"N": "Very High (100-120)", "P": "Moderate (60-80)", "K": "Extremely High (150-200)"},
        "description": "Gigantic herbaceous plant with tremendous biomass and heavy nutrient consumption, particularly potassium. Highly susceptible to wind lodging.",
        "cultivation_tips": [
            "Heavy feeder: requires substantial potassium for bunch development and finger filling.",
            "Desuckering is critical; retain only one healthy follower sucker per mother plant.",
            "Provide propping with bamboo poles when bunches emerge to prevent trunk snapping."
        ],
        "stages": [
            {"stage": "Planting & Sucker Sprouting", "days": "Months 1-2", "desc": "Tissue culture or sword sucker rooting"},
            {"stage": "Active Vegetative", "days": "Months 3-7", "desc": "Emergence of broad lush leaves (broadleaf canopy)"},
            {"stage": "Shooting / Inflorescence", "days": "Months 7-8", "desc": "Emergence of large purple pendulous flower bud"},
            {"stage": "Bunch Development", "days": "Months 8-11", "desc": "Hands unfold and fingers fill with starch"},
            {"stage": "Bunch Harvest", "days": "Months 11-12", "desc": "Harvest when finger angles become rounded"}
        ]
    },
    "mango": {
        "id": "mango",
        "name": "Mango",
        "scientific_name": "Mangifera indica",
        "family": "Anacardiaceae",
        "category": "Fruit / Horticultural",
        "season": "Perennial (Summer harvest)",
        "duration_days": "100 - 140 days from fruit set",
        "min_duration": 100,
        "max_duration": 140,
        "soil_type": "Deep well-drained alluvial, loamy or lateritic soils with low water table",
        "optimal_ph": "5.5 - 7.5",
        "ph_min": 5.5,
        "ph_max": 7.5,
        "optimal_temp": "24°C - 36°C",
        "temp_min": 24,
        "temp_max": 36,
        "optimal_humidity": "45% - 65%",
        "water_requirement": "Moderate",
        "rainfall_range": "80 - 140 mm",
        "npk_profile": {"N": "Moderate (20-40)", "P": "Moderate (20-40)", "K": "Moderate to High (30-50)"},
        "description": "The King of Fruits. Requires dry conditions during winter flowering and hot sunny weather during fruit maturation.",
        "cultivation_tips": [
            "Withhold irrigation in autumn/winter for 2-3 months before flowering to encourage vegetative dormancy and floral bud differentiation.",
            "Rain or cloudiness during flowering encourages powdery mildew and anthracnose.",
            "Harvest with 1 cm stalk intact to prevent latex sap burn on fruit surface."
        ],
        "stages": [
            {"stage": "Winter Dormancy", "days": "Nov - Dec", "desc": "Rest period essential for floral induction"},
            {"stage": "Panicle Emergence & Bloom", "days": "Jan - Feb", "desc": "Dense blossom requiring active bee pollination"},
            {"stage": "Fruit Set & Pea Stage", "days": "Feb - Mar", "desc": "Initial fruit drop and marble stage thinning"},
            {"stage": "Fruit Growth & Maturity", "days": "Mar - May", "desc": "Rapid sizing, shoulder development and blush"},
            {"stage": "Harvest", "days": "May - June", "desc": "Hand harvesting at physiological maturity"}
        ]
    },
    "grapes": {
        "id": "grapes",
        "name": "Grapes",
        "scientific_name": "Vitis vinifera",
        "family": "Vitaceae",
        "category": "Fruit / Commercial",
        "season": "Perennial (Two pruning cycles/year in tropics)",
        "duration_days": "120 - 140 days post forward pruning",
        "min_duration": 120,
        "max_duration": 140,
        "soil_type": "Well-drained sandy loam or gravelly soils",
        "optimal_ph": "6.0 - 7.5",
        "ph_min": 6.0,
        "ph_max": 7.5,
        "optimal_temp": "15°C - 32°C",
        "temp_min": 15,
        "temp_max": 32,
        "optimal_humidity": "50% - 85%",
        "water_requirement": "Moderate",
        "rainfall_range": "65 - 80 mm",
        "npk_profile": {"N": "Moderate (20-40)", "P": "High (120-140)", "K": "Extremely High (180-210)"},
        "description": "High-value perennial woody vine. Requires warm dry climate during grape berry ripening to prevent downy mildew and achieve high Brix sugar levels.",
        "cultivation_tips": [
            "Trellis training system (Bower/Y-trellis) ensures maximum canopy sunlight exposure.",
            "Apply Gibberellic Acid (GA3) at bloom for cluster elongation and berry thinning.",
            "Withhold water 7-10 days prior to harvest to increase sugar concentration."
        ],
        "stages": [
            {"stage": "Foundation Pruning (April)", "days": "Summer", "desc": "Cane development for next year"},
            {"stage": "Forward Pruning (October)", "days": "Autumn", "desc": "Fruit pruning to induce berry clusters"},
            {"stage": "Bud Break & Bloom", "days": "Days 15-40", "desc": "Rapid shoot burst and cap fall flowering"},
            {"stage": "Berry Sizing (Veraison)", "days": "Days 41-90", "desc": "Berry softening, color change and sugar surge"},
            {"stage": "Harvest", "days": "Days 110-135", "desc": "Harvest when TSS exceeds 18° Brix"}
        ]
    },
    "watermelon": {
        "id": "watermelon",
        "name": "Watermelon",
        "scientific_name": "Citrullus lanatus",
        "family": "Cucurbitaceae",
        "category": "Fruit / Cucurbit",
        "season": "Zaid (Summer)",
        "duration_days": "80 - 100 days",
        "min_duration": 80,
        "max_duration": 100,
        "soil_type": "Sandy, sandy loam, or alluvial riverbeds with warm temperature",
        "optimal_ph": "6.0 - 7.0",
        "ph_min": 6.0,
        "ph_max": 7.0,
        "optimal_temp": "24°C - 35°C",
        "temp_min": 24,
        "temp_max": 35,
        "optimal_humidity": "45% - 70%",
        "water_requirement": "Moderate to High",
        "rainfall_range": "40 - 60 mm",
        "npk_profile": {"N": "Moderate (30-50)", "P": "Moderate (15-30)", "K": "Moderate to High (45-60)"},
        "description": "Warm-season trailing vine requiring long sunny days and dry weather during ripening. Very sensitive to frost.",
        "cultivation_tips": [
            "Excellent for riverbed (diara) farming in deep sandy deposits.",
            "Water deeply but infrequently; reduce irrigation during ripening to sweeten flesh.",
            "Check harvest readiness: yellow ground spot and dry tendril opposite the fruit stem."
        ],
        "stages": [
            {"stage": "Sowing & Sprouting", "days": "Days 1-8", "desc": "Pit sowing under warm soil conditions"},
            {"stage": "Vine Extension", "days": "Days 9-35", "desc": "Trailing ground runner growth"},
            {"stage": "Flowering & Fruit Set", "days": "Days 36-55", "desc": "Yellow unisexual flowers requiring honeybee visits"},
            {"stage": "Fruit Swelling", "days": "Days 56-80", "desc": "Rapid melon weight gain"},
            {"stage": "Harvest", "days": "Days 81-95", "desc": "Dull thud sound and drying tendril"}
        ]
    },
    "muskmelon": {
        "id": "muskmelon",
        "name": "Muskmelon (Cantaloupe / Kharbooza)",
        "scientific_name": "Cucumis melo",
        "family": "Cucurbitaceae",
        "category": "Fruit / Cucurbit",
        "season": "Zaid (Summer)",
        "duration_days": "75 - 90 days",
        "min_duration": 75,
        "max_duration": 90,
        "soil_type": "Well-drained sandy loam or riverbed soils",
        "optimal_ph": "6.0 - 7.5",
        "ph_min": 6.0,
        "ph_max": 7.5,
        "optimal_temp": "25°C - 35°C",
        "temp_min": 25,
        "temp_max": 35,
        "optimal_humidity": "45% - 65%",
        "water_requirement": "Moderate",
        "rainfall_range": "20 - 40 mm",
        "npk_profile": {"N": "Moderate (20-40)", "P": "Moderate (15-30)", "K": "Moderate to High (45-60)"},
        "description": "Sweet, aromatic melon thriving in hot, arid conditions. High atmospheric humidity during ripening degrades fruit flavor and causes fungal fruit rot.",
        "cultivation_tips": [
            "Requires bright sunshine and dry atmospheric conditions during ripening.",
            "Avoid overhead irrigation which promotes powdery and downy mildew on leaves.",
            "Harvest at 'full slip' stage when the stem separates cleanly with gentle thumb pressure."
        ],
        "stages": [
            {"stage": "Emergence", "days": "Days 1-7", "desc": "Cotyledon emergence"},
            {"stage": "Runner Development", "days": "Days 8-30", "desc": "Vegetative vine expansion"},
            {"stage": "Flowering", "days": "Days 31-50", "desc": "Male flowers appear first, followed by female blooms"},
            {"stage": "Netting & Ripening", "days": "Days 51-75", "desc": "Cork-like net formation and aroma emergence"},
            {"stage": "Harvest", "days": "Days 76-85", "desc": "Full-slip detachment"}
        ]
    },
    "apple": {
        "id": "apple",
        "name": "Apple",
        "scientific_name": "Malus domestica",
        "family": "Rosaceae",
        "category": "Temperate Fruit",
        "season": "Perennial (Autumn harvest)",
        "duration_days": "130 - 160 days from blossom",
        "min_duration": 130,
        "max_duration": 160,
        "soil_type": "Deep, well-drained loamy soils rich in organic matter",
        "optimal_ph": "5.5 - 6.8",
        "ph_min": 5.5,
        "ph_max": 6.8,
        "optimal_temp": "10°C - 24°C (requires winter chilling)",
        "temp_min": 10,
        "temp_max": 24,
        "optimal_humidity": "60% - 85%",
        "water_requirement": "Moderate",
        "rainfall_range": "100 - 130 mm",
        "npk_profile": {"N": "Moderate (20-40)", "P": "High (120-145)", "K": "Extremely High (190-210)"},
        "description": "Premier temperate deciduous fruit tree. Requires 800 - 1500 winter chilling hours below 7°C to break winter dormancy and achieve uniform spring blossom.",
        "cultivation_tips": [
            "Plant cross-pollinating pollinizer varieties (e.g. Golden Delicious) at 15-20% orchard ratio.",
            "Perform winter dormant pruning to open the center canopy to direct sunlight.",
            "Maintain soil mulch around root zone to preserve moisture and suppress weeds."
        ],
        "stages": [
            {"stage": "Winter Dormancy", "days": "Dec - Feb", "desc": "Chilling accumulation period"},
            {"stage": "Silver Tip to Pink Bud", "days": "March", "desc": "Bud swell and flower bud show"},
            {"stage": "Full Bloom & Pollination", "days": "April", "desc": "Critical honeybee pollination window"},
            {"stage": "Fruit Development", "days": "May - July", "desc": "Cell division and sizing"},
            {"stage": "Coloring & Harvest", "days": "Aug - Oct", "desc": "Sugar accumulation and harvesting"}
        ]
    },
    "orange": {
        "id": "orange",
        "name": "Orange (Citrus / Mandarin)",
        "scientific_name": "Citrus sinensis / reticulata",
        "family": "Rutaceae",
        "category": "Fruit / Citrus",
        "season": "Perennial (Winter harvest)",
        "duration_days": "240 - 270 days from bloom",
        "min_duration": 240,
        "max_duration": 270,
        "soil_type": "Light to medium loamy or sandy loam soil with excellent drainage",
        "optimal_ph": "6.0 - 7.5",
        "ph_min": 6.0,
        "ph_max": 7.5,
        "optimal_temp": "15°C - 35°C",
        "temp_min": 15,
        "temp_max": 35,
        "optimal_humidity": "60% - 90%",
        "water_requirement": "Moderate",
        "rainfall_range": "100 - 120 mm",
        "npk_profile": {"N": "Moderate (15-35)", "P": "Low to Moderate (10-25)", "K": "Low to Moderate (10-25)"},
        "description": "Subtropical evergreen citrus. Deeply sensitive to saline soil, heavy clay, and stagnant subsurface moisture.",
        "cultivation_tips": [
            "Avoid deep tillage near trunk to protect shallow fibrous feeder roots.",
            "Apply zinc and iron micronutrient foliar sprays if chlorosis appears on young flush.",
            "Ensure subsoil drainage: water stagnation induces Phytophthora gummosis root rot."
        ],
        "stages": [
            {"stage": "Spring Blossom", "days": "Feb - March", "desc": "Fragrant white citrus blossoms"},
            {"stage": "Fruitlet Set", "days": "April", "desc": "Initial set and natural summer fruit drop"},
            {"stage": "Fruit Sizing", "days": "May - Sept", "desc": "Cell expansion and juice sac formation"},
            {"stage": "Degreening / Color Break", "days": "Oct - Nov", "desc": "Cool nights trigger chlorophyll breakdown and carotenoid yellowing"},
            {"stage": "Harvesting", "days": "Dec - Feb", "desc": "Snip fruit using clippers without tearing peel"}
        ]
    },
    "papaya": {
        "id": "papaya",
        "name": "Papaya",
        "scientific_name": "Carica papaya",
        "family": "Caricaceae",
        "category": "Fruit / Quick Commercial",
        "season": "Year-round in frost-free tropics",
        "duration_days": "270 - 330 days (9 - 11 months)",
        "min_duration": 270,
        "max_duration": 330,
        "soil_type": "Rich, well-drained sandy loam or alluvial soil",
        "optimal_ph": "6.0 - 7.0",
        "ph_min": 6.0,
        "ph_max": 7.0,
        "optimal_temp": "22°C - 35°C",
        "temp_min": 22,
        "temp_max": 35,
        "optimal_humidity": "70% - 95%",
        "water_requirement": "Moderate to High",
        "rainfall_range": "120 - 200 mm",
        "npk_profile": {"N": "High (40-60)", "P": "Moderate to High (50-70)", "K": "High (45-60)"},
        "description": "Fast-growing giant herbaceous fruit plant producing within 10 months. Extremely sensitive to waterlogging and frost.",
        "cultivation_tips": [
            "Plant on raised mounds or ridges; water stagnation around stem base for even 12 hours causes lethal foot rot (Pythium).",
            "Maintain 1 male plant for every 10 female plants for dioecious cultivars (unnecessary for gynodioecious varieties like Red Lady).",
            "Harvest when skin shows yellow streaks at apex."
        ],
        "stages": [
            {"stage": "Nursery & Transplant", "days": "Days 1-45", "desc": "Seed germination and polybag seedling raising"},
            {"stage": "Establishment & Growth", "days": "Days 46-120", "desc": "Rapid hollow stem expansion and canopy fan"},
            {"stage": "Sex Determination & Flowering", "days": "Days 121-160", "desc": "Bud emergence and thinning excess male trees"},
            {"stage": "Fruit Development", "days": "Days 161-270", "desc": "Heavy cluster loading along main stem"},
            {"stage": "Harvesting", "days": "Days 270-360", "desc": "Continuous selective picking as fruit ripens"}
        ]
    },
    "coconut": {
        "id": "coconut",
        "name": "Coconut (Kalpavriksha)",
        "scientific_name": "Cocos nucifera",
        "family": "Arecaceae",
        "category": "Plantation / Cash Crop",
        "season": "Perennial (Continuous monthly harvest)",
        "duration_days": "12 months per nut bunch from pollination",
        "min_duration": 365,
        "max_duration": 365,
        "soil_type": "Coastal sandy, red loamy, lateritic, or alluvial soils",
        "optimal_ph": "5.2 - 8.0",
        "ph_min": 5.2,
        "ph_max": 8.0,
        "optimal_temp": "25°C - 35°C",
        "temp_min": 25,
        "temp_max": 35,
        "optimal_humidity": "70% - 99%",
        "water_requirement": "High",
        "rainfall_range": "130 - 250 mm",
        "npk_profile": {"N": "Moderate (20-30)", "P": "Low to Moderate (15-25)", "K": "Moderate (25-35)"},
        "description": "The Palm of Life. Thrives in warm, humid coastal and tropical plains with regular rainfall and high relative humidity.",
        "cultivation_tips": [
            "Provide balanced organic manuring and common salt (sodium chloride) in inland areas to supply chlorine.",
            "Crown cleaning twice a year prevents rhinoceros beetle and red palm weevil infestations.",
            "Mulch palm basin with dried coconut fronds and husk to conserve soil moisture."
        ],
        "stages": [
            {"stage": "Seednut Germination", "days": "Months 1-5", "desc": "Sprouting in sand beds"},
            {"stage": "Juvenile Field Establishment", "days": "Years 1-4", "desc": "Trunk development and crown expansion"},
            {"stage": "First Flowering", "days": "Years 5-6", "desc": "Spathe emergence"},
            {"stage": "Bunch Maturation", "days": "12 Months/Bunch", "desc": "Successive monthly bunch development"},
            {"stage": "Productive Bearing", "days": "Years 7-60+", "desc": "Regular nut harvesting every 45-60 days"}
        ]
    },
    "cotton": {
        "id": "cotton",
        "name": "Cotton (White Gold)",
        "scientific_name": "Gossypium hirsutum",
        "family": "Malvaceae",
        "category": "Fiber / Cash Crop",
        "season": "Kharif (Monsoon)",
        "duration_days": "150 - 180 days",
        "min_duration": 150,
        "max_duration": 180,
        "soil_type": "Deep black cotton soils (Vertisols) or deep fertile alluvium",
        "optimal_ph": "6.0 - 8.0",
        "ph_min": 6.0,
        "ph_max": 8.0,
        "optimal_temp": "22°C - 35°C",
        "temp_min": 22,
        "temp_max": 35,
        "optimal_humidity": "50% - 80%",
        "water_requirement": "Moderate",
        "rainfall_range": "60 - 100 mm",
        "npk_profile": {"N": "High (100-130)", "P": "Moderate (40-60)", "K": "Low (15-25)"},
        "description": "The world's leading natural textile fiber. Requires warm days, plenty of sunshine during boll bursting, and no rain at harvest.",
        "cultivation_tips": [
            "Deep black soil preserves moisture during reproductive phase.",
            "Install yellow sticky traps and pheromone traps to scout pink bollworm.",
            "Rainfall during boll opening stains lint and causes severe quality degradation."
        ],
        "stages": [
            {"stage": "Germination & Square Formation", "days": "Days 1-45", "desc": "Emergence and floral bud (square) appearance"},
            {"stage": "Flowering & Boll Setting", "days": "Days 46-90", "desc": "White flowers pollinate, turn pink, form bolls"},
            {"stage": "Boll Development", "days": "Days 91-130", "desc": "Boll expansion and fiber elongation inside"},
            {"stage": "Boll Bursting", "days": "Days 131-160", "desc": "Bolls burst open revealing clean white fluffy lint"},
            {"stage": "Picking", "days": "Days 161-180", "desc": "2-3 manual pickings on dry sunny mornings"}
        ]
    },
    "jute": {
        "id": "jute",
        "name": "Jute (Golden Fiber)",
        "scientific_name": "Corchorus olitorius / capsularis",
        "family": "Malvaceae",
        "category": "Fiber / Cash Crop",
        "season": "Pre-Kharif / Monsoon",
        "duration_days": "120 - 140 days",
        "min_duration": 120,
        "max_duration": 140,
        "soil_type": "Rich new alluvial delta soils subject to annual river silt deposits",
        "optimal_ph": "6.0 - 7.5",
        "ph_min": 6.0,
        "ph_max": 7.5,
        "optimal_temp": "24°C - 35°C",
        "temp_min": 24,
        "temp_max": 35,
        "optimal_humidity": "75% - 95%",
        "water_requirement": "High",
        "rainfall_range": "150 - 250 mm",
        "npk_profile": {"N": "High (70-90)", "P": "Moderate (40-55)", "K": "Moderate (35-45)"},
        "description": "Eco-friendly natural golden fiber crop. Thrives in warm, tropical, humid climates with heavy rainfall and standing water for retting.",
        "cultivation_tips": [
            "Weeding and thinning at 20 days is essential for straight stem growth without branching.",
            "Harvest at 50% flowering stage for the finest fiber tensile strength.",
            "Steep harvested bundles in slow-moving fresh water for 12-15 days for optimal retting."
        ],
        "stages": [
            {"stage": "Sowing & Germination", "days": "Days 1-8", "desc": "Broadcast or line sowing in moist silt"},
            {"stage": "Thinning & Weeding", "days": "Days 9-30", "desc": "Singling out plants to ensure tall unbranched canes"},
            {"stage": "Rapid Stem Elongation", "days": "Days 31-90", "desc": "Stems reach 2.5 to 3.5 meters in height"},
            {"stage": "Flowering & Harvest", "days": "Days 91-120", "desc": "Cutting canes at ground level at early bloom"},
            {"stage": "Retting & Fiber Extraction", "days": "Post-Harvest", "desc": "Water soaking to decompose pectins, stripping fibers"}
        ]
    },
    "coffee": {
        "id": "coffee",
        "name": "Coffee (Arabica / Robusta)",
        "scientific_name": "Coffea arabica / canephora",
        "family": "Rubiaceae",
        "category": "Beverage / Plantation",
        "season": "Perennial (Winter berry picking)",
        "duration_days": "210 - 270 days from blossom to berry harvest",
        "min_duration": 210,
        "max_duration": 270,
        "soil_type": "Deep, porous, slightly acidic forest loam rich in organic humus",
        "optimal_ph": "5.5 - 6.5",
        "ph_min": 5.5,
        "ph_max": 6.5,
        "optimal_temp": "15°C - 28°C",
        "temp_min": 15,
        "temp_max": 28,
        "optimal_humidity": "65% - 85%",
        "water_requirement": "Moderate to High",
        "rainfall_range": "150 - 200 mm",
        "npk_profile": {"N": "High (90-110)", "P": "Moderate (25-35)", "K": "Moderate (25-35)"},
        "description": "High-value shade-grown plantation beverage crop. Cultivated under a multi-tier forest canopy in hilly elevations (600 - 1500m MSL).",
        "cultivation_tips": [
            "Cultivate under two-tier shade trees (e.g. Silver Oak, Dadap) to regulate light and buffer temperature.",
            "Blossom showers in March-April are mandatory to trigger uniform flower opening.",
            "Pick only bright red ripe 'cherries' for superior cupping quality."
        ],
        "stages": [
            {"stage": "Blossom Showers & Bloom", "days": "March - April", "desc": "Star-like jasmine scented blossom trigger"},
            {"stage": "Berry Setting", "days": "May - June", "desc": "Pinhead stage to berry expansion"},
            {"stage": "Monsoon Berry Sizing", "days": "July - Sept", "desc": "Berry weight gain under cloud cover"},
            {"stage": "Berry Ripening", "days": "Oct - Nov", "desc": "Green berries turn deep crimson cherry red"},
            {"stage": "Selective Picking", "days": "Dec - Feb", "desc": "Hand picking ripe cherries in 3-4 rounds"}
        ]
    }
}

def get_all_crops():
    return list(CROPS_CATALOG.values())

def get_crop_by_id(crop_id):
    if not crop_id:
        return None
    key = crop_id.lower().strip()
    return CROPS_CATALOG.get(key)

def search_crops(query=None, category=None, season=None):
    results = []
    for crop in CROPS_CATALOG.values():
        match = True
        if query:
            q = query.lower().strip()
            name_match = q in crop["name"].lower() or q in crop["id"] or q in crop["scientific_name"].lower()
            if not name_match:
                match = False
        if category and category != "all":
            if category.lower() not in crop["category"].lower():
                match = False
        if season and season != "all":
            if season.lower() not in crop["season"].lower():
                match = False
        if match:
            results.append(crop)
    return results

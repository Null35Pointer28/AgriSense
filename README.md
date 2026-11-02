# 🌱 AgriSense
### Intelligent Crop Management and Agricultural Decision Support System

> A production-grade, full-stack agricultural decision-support platform designed to provide precision crop suitability recommendations, soil fertility diagnostics, rule-based irrigation scheduling, meteorological forecasting, fertilizer guidance, crop phenology management, historical field tracking, and generative agronomic intelligence.

---

## 📖 Executive Summary & Context

**AgriSense** is an academic software project developed to bridge modern computer science technologies—supervised machine learning, agrometeorological APIs, SQLite data persistence, and Google Gemini AI—with real-world agricultural decision-making. 

AgriSense serves as the **software intelligence and decision-support layer** for a larger, future **Agri-Solar Dome and IoT-based agricultural monitoring ecosystem**.

---

## 🛠 Technology Stack

### Frontend
- **HTML5 & Modern Semantic Markup**
- **Custom CSS3 Design System**: Agricultural SaaS aesthetic with dark forest green (`#0a2f1d`), emerald accents (`#16a34a`), warm neutrals, and responsive grid layouts.
- **Vanilla JavaScript (ES6+)**: Zero framework lock-in; modular reactive state management, asynchronous fetch pipelines, and interactive UI modals.
- **Chart.js (v4.4)**: Real-time interactive visualizations including 24-hour weather trends, NPK benchmark comparisons, multi-crop 5-axis radar suitability charts, and ML model performance metrics.

### Backend & Machine Learning
- **Python (3.12+)**
- **Flask (v3.1+)**: Application factory pattern, RESTful API blueprints (`/api/*`), and static asset serving.
- **Scikit-learn (v1.5+)**: Reproducible stratified train/test pipeline, scaling, and multiclass classifier comparison.
- **Pandas & NumPy**: Dataset preprocessing, numerical statistics, and Gaussian suitability distance functions.
- **Joblib**: Serialized best-performing model pipeline (`Random Forest`).

### Database
- **SQLite3**: ACID-compliant local database storing farming history, field soil test records, crop recommendation logs, and user location preferences.

### AI Assistant & External APIs
- **Google Gemini API**: Utilizing the official modern SDK `google-genai` and `python-dotenv`. Model: `gemini-3.8-flash` (configurable via `.env`).
- **Open-Meteo Weather API**: Live ambient temperature, relative humidity, precipitation, wind speed, WMO weather codes, and 7-day agricultural forecasts.
- **Open-Meteo Geocoding API**: Location search by city, district, or agricultural zone with browser geolocation reverse-geocoding.

---

## 📂 Project Structure

```text
AgriSense/
│
├── app.py                         # Application entrypoint (python app.py)
├── requirements.txt               # Pinned project dependencies
├── .env.example                   # Environment configuration template
├── .env                           # Local environment secrets (in .gitignore)
├── .gitignore                     # Git exclusion rules
├── README.md                      # Comprehensive project documentation
│
├── app/
│   ├── __init__.py                # Flask application factory & database initializer
│   ├── database/
│   │   └── db.py                  # SQLite schema, connection lifecycle, CRUD queries
│   ├── ml/
│   │   ├── train.py               # 5-Model evaluation, comparison & training pipeline
│   │   └── predict.py             # Inference engine, agronomic explanations & range validation
│   ├── routes/
│   │   ├── api.py                 # REST API endpoints for all 11 features
│   │   └── views.py               # Frontend page render routes
│   └── services/
│       ├── crop_data.py           # Structured knowledge catalog for all 22 crops
│       ├── soil_service.py        # NPK rating & soil pH chemical remediation
│       ├── weather_service.py     # Open-Meteo weather and geocoding integration
│       ├── irrigation_service.py  # Transparent rule-based water budgeting advisor
│       ├── fertilizer_service.py  # Mineral, organic & biofertilizer recommendations
│       ├── comparison_service.py  # Gaussian mathematical multi-crop suitability engine
│       ├── calendar_service.py    # Phenological growth stages and operations schedule
│       └── gemini_service.py      # Google Gemini integration with farm context injection
│
├── data/
│   ├── raw/
│   │   └── Crop_recommendation.csv # Original Kaggle Crop Recommendation Dataset
│   ├── processed/
│   │   ├── crop_recommendation_clean.csv # Clean verified dataset
│   │   └── dataset_report.json           # Verification metrics & distributions
│   └── agrisense.db               # SQLite database file (auto-generated)
│
├── saved_models/
│   ├── crop_recommendation_model.joblib # Serialized best model pipeline
│   └── ml_metrics.json                  # Real test evaluation metrics & confusion matrix
│
├── static/
│   ├── css/
│   │   └── style.css              # Agricultural SaaS styling & responsive design
│   └── js/
│       └── app.js                 # Frontend application controller & Chart.js drivers
│
├── templates/
│   └── index.html                 # Unified dashboard template with all 11 feature views
│
└── tests/
    └── test_agrisense.py          # 20 automated pytest test cases
```

---

## 📊 Dataset Acquisition & Rigorous Verification

AgriSense uses the verified **Crop Recommendation Dataset** originally published by Atharva Ingle on Kaggle.

- **Storage Location**: Preserved raw in `data/raw/Crop_recommendation.csv` and processed in `data/processed/crop_recommendation_clean.csv`.
- **Dimensions**: Exactly **2,200 records** across **8 columns**.
- **Missing Values**: 0 (Zero nulls across all features).
- **Duplicate Rows**: 0 duplicates.
- **Classes**: Exactly **22 crop classes** in balanced distribution (100 records per crop):
  * *Cereals*: Rice, Maize
  * *Pulses*: Chickpea, Kidneybeans, Pigeonpeas, Mothbeans, Mungbean, Blackgram, Lentil
  * *Fruits*: Pomegranate, Banana, Mango, Grapes, Watermelon, Muskmelon, Apple, Orange, Papaya
  * *Fibers & Commercial*: Coconut, Cotton, Jute, Coffee
- **Feature Ranges**:
  - **Nitrogen (N)**: 0.0 - 140.0 kg/ha (Mean: 50.55, Std: 36.92)
  - **Phosphorus (P)**: 5.0 - 145.0 kg/ha (Mean: 53.36, Std: 32.99)
  - **Potassium (K)**: 5.0 - 205.0 kg/ha (Mean: 48.15, Std: 50.65)
  - **Temperature**: 8.83 - 43.68 °C (Mean: 25.62, Std: 5.06)
  - **Humidity**: 14.26 - 99.98 % (Mean: 71.48, Std: 22.26)
  - **Soil pH**: 3.50 - 9.94 (Mean: 6.47, Std: 0.77)
  - **Rainfall**: 20.21 - 298.56 mm (Mean: 103.46, Std: 54.96)

---

## 🤖 Machine Learning Model Training & Evaluation

The ML pipeline (`app/ml/train.py`) trains and compares 5 classification algorithms using a stratified 80/20 train/test split (1,760 train samples, 440 test samples) with `random_state=42`. Zero synthetic or fabricated data is used.

### Actual Evaluation Results (from `saved_models/ml_metrics.json`)

| Model Algorithm | Accuracy | Precision (Weighted) | Recall (Weighted) | F1-Score (Weighted) | Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Random Forest Classifier** | **99.55%** | **99.56%** | **99.55%** | **99.55%** | **Selected Model** |
| **Gaussian Naive Bayes** | 99.55% | 99.57% | 99.55% | 99.54% | Evaluated |
| **Support Vector Machine (RBF)** | 98.86% | 98.92% | 98.86% | 98.87% | Evaluated |
| **Decision Tree Classifier** | 98.18% | 98.24% | 98.18% | 98.17% | Evaluated |
| **K-Nearest Neighbors (k=5)** | 97.95% | 98.10% | 97.95% | 97.93% | Evaluated |

Random Forest achieved the highest weighted F1-score (**0.9955**) and is serialized to `saved_models/crop_recommendation_model.joblib`. The ML Performance Center view on the dashboard dynamically visualizes this comparison along with the complete 22x22 confusion matrix.

---

## 🌟 The 11 Core Application Features

1. **Crop Recommendation Engine (ML)**: Predicts optimal crop suitability using the trained Random Forest model with input bounds validation, confidence percentages, alternative crop suggestions, and transparent agronomic explanations.
2. **Soil Health Diagnostics**: Evaluates user-entered or lab-tested NPK and pH values, calculates an overall Soil Health Index (0-100), provides pH chemical interpretation (acidic/neutral/alkaline), and outlines a custom soil amendment plan.
3. **Weather Intelligence Center**: Connects to Open-Meteo to provide live ambient temperature, relative humidity, wind speed, precipitation, 7-day agricultural forecasts, 24-hour trends, and automatic agro-meteorological alerts (frost hazard, extreme heat stress, fungal blight risk).
4. **Irrigation Advisor**: Transparent rule-based water budgeting evaluating crop water demand, current temperature, humidity, surface moisture, and upcoming 48-hour rainfall forecasts to calculate irrigation priority (High, Moderate, Low, Hold).
5. **Crop Information Library**: A structured catalog containing verified agronomic data for all 22 crops, searchable and filterable by category and season, with growth stages and cultivation tips.
6. **Fertilizer Advisor**: Evaluates soil N-P-K reserves to detect deficiencies or imbalances, offering chemical, slow-release, organic (FYM, vermicompost), and biofertilizer (PSB, Rhizobium, Azotobacter, KMB) options with split-dosing strategies.
7. **Crop Suitability Comparison**: Side-by-side comparative analysis of 2 to 4 crops using a documented Gaussian distance function to compute transparent suitability scores, accompanied by an interactive 5-axis Chart.js radar chart.
8. **Crop Calendar & Phenology**: Displays sowing, active growth, and harvesting windows alongside chronological growth stages and a 6-step field operations checklist.
9. **Farming History**: SQLite database persistence allowing farmers to save soil readings, crop recommendations, and field notes, with record filtering, deletion, and historical nutrient averaging.
10. **ML Performance Dashboard**: Interactive visual display of real model evaluation metrics, algorithm comparison bar charts, dataset facts, and the full multiclass confusion matrix.
11. **AgriSense AI Assistant**: Real conversational AI powered by Google Gemini (`google-genai` SDK) that ingests current farm context (location, weather, soil test, last recommended crop) to deliver tailored agronomic explanations.

---

## 🚀 Quickstart Installation Guide

### Prerequisites
- Python 3.10+ (tested on Python 3.12)
- Git (optional)
- Modern web browser (Chrome, Edge, Firefox)

### Step 1: Clone or Navigate to the Project Directory
```powershell
cd "d:\Projects\College\PBL\New folder\AgriSense"
```

### Step 2: Install Python Dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
Copy `.env.example` to `.env`:
```powershell
copy .env.example .env
```
Open `.env` in any text editor and configure your settings:
```env
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
FLASK_DEBUG=True
SECRET_KEY=agrisense-secure-local-secret-key-2026

# Google Gemini API Key (Obtain from https://aistudio.google.com/)
GEMINI_API_KEY=your_actual_api_key_here
GEMINI_MODEL=gemini-3.8-flash
```

*(Note: The application will launch and operate all features even if `GEMINI_API_KEY` is not yet configured. The AI assistant will gracefully notify you to provide a key when opened).*

### Step 4: Run the Machine Learning Pipeline (Optional - Pre-trained models included)
If you wish to re-train the models from scratch:
```powershell
python app/ml/train.py
```

### Step 5: Start the Application (One-Command Startup)
```powershell
python app.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🧪 Running Automated Tests

Run the comprehensive pytest suite covering all 11 modules:
```powershell
python -m pytest tests/test_agrisense.py -v
```
All 20 tests verify ML inference, out-of-bound parameter handling, soil health formulas, weather mapping, irrigation logic, fertilizer diagnostics, SQLite persistence, and API routes.

---

## ⚠️ Agronomic Disclaimers & Dataset Limitations

1. **Accumulated Rainfall vs. Daily Precipitation**: The rainfall feature in the Kaggle dataset represents total seasonal precipitation across the growing cycle (typically 100 - 300 mm). AgriSense explicitly distinguishes this from instantaneous daily weather rainfall to prevent erroneous model predictions.
2. **Geographical Representativeness**: The training dataset reflects typical Indian subcontinental agricultural ranges. Predictions should be interpreted as general suitability indicators rather than yield guarantees.
3. **Physical Soil Properties**: Real-world crop success depends on factors not present in the tabular dataset, such as effective rooting depth, hardpan presence, drainage rate, seed variety, and pest pressure.
4. **Laboratory Soil Testing**: User-entered soil values provide preliminary screening; commercial fertilizer purchases should always be confirmed through certified agricultural laboratory testing (e.g. Krishi Vigyan Kendra - KVK).

---

## 🔭 Future Scope: Agri-Solar Dome & IoT Integration

AgriSense is architecturally designed to serve as the intelligence hub for future hardware expansions:
1. **Agri-Solar Dome Architecture**: Integrating bifacial photovoltaic canopy telemetry with microclimate humidity and photosynthetically active radiation (PAR) management.
2. **ESP32 IoT Sensor Network**: Ingesting real-time telemetry from capacitive soil moisture probes, DHT22 air sensors, and NPK optical sensors via MQTT or REST endpoints.
3. **Automated Irrigation Control**: Driving solenoid valves and relay-switched water pumps using edge microcontroller actuators.
4. **Solar Energy Telemetry**: Monitoring solar generation, battery state-of-charge, and pump power consumption.
5. **Computer Vision Pathology**: Future integration of CNN-based plant leaf disease detection using edge cameras.

---

## 📄 License
This academic project is developed for educational and research purposes under the MIT License.

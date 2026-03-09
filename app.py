from flask import Flask, render_template, request, jsonify
from typing import Dict, List, Any
import sys
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')

# ─── Crop Knowledge Base ───────────────────────────────────────────────────────
CROP_DATABASE: Dict[str, Dict[str, Any]] = {
    "Rice": {
        "icon": "🌾", "color": "#4CAF50",
        "optimal_rainfall": (1200, 2000), "optimal_temp": (22, 35),
        "soils": ["Clay", "Loamy", "Silty"],
        "seasons": ["Kharif", "Rabi"],
        "water_need": "High", "growth_days": 120,
        "description": "Staple grain crop highly adaptable to flooded conditions.",
        "market_value": "₹18-22/kg", "protein": "7.1g/100g",
        "irrigation": "Water every 3–4 days; 1200–1500 mm total.",
        "economics": {"yield_per_acre": "2.5 tons", "price": "₹22/kg", "profit": "₹55,000/acre"},
        "calendar": ["Sowing (Jun)", "Vegetative (Jul-Aug)", "Fertilization (Sep)", "Harvest (Oct)"],
        "rotation": "Chickpea or Mustard"
    },
    "Wheat": {
        "icon": "🌿", "color": "#FFC107",
        "optimal_rainfall": (400, 900), "optimal_temp": (10, 25),
        "soils": ["Loamy", "Clay", "Sandy Loam"],
        "seasons": ["Rabi", "Winter"],
        "water_need": "Medium", "growth_days": 110,
        "description": "Cool-season cereal crop with high yield potential.",
        "market_value": "₹20-25/kg", "protein": "12.6g/100g",
        "irrigation": "Water every 7–10 days; 450–650 mm total.",
        "economics": {"yield_per_acre": "2.0 tons", "price": "₹25/kg", "profit": "₹50,000/acre"},
        "calendar": ["Sowing (Nov)", "Tillering (Dec-Jan)", "Flowering (Feb)", "Harvest (Mar-Apr)"],
        "rotation": "Maize or Soybean"
    },
    "Maize": {
        "icon": "🌽", "color": "#FF9800",
        "optimal_rainfall": (600, 1100), "optimal_temp": (18, 32),
        "soils": ["Sandy Loam", "Loamy", "Clay"],
        "seasons": ["Kharif", "Summer"],
        "water_need": "Medium", "growth_days": 90,
        "description": "Versatile crop suitable for food, feed, and biofuel.",
        "market_value": "₹15-18/kg", "protein": "9.4g/100g",
        "irrigation": "Water every 5–7 days; 500–800 mm total.",
        "economics": {"yield_per_acre": "3.0 tons", "price": "₹18/kg", "profit": "₹54,000/acre"},
        "calendar": ["Sowing (Jun/Mar)", "Growth (Jul/Apr)", "Tasseling (Aug/May)", "Harvest (Sep/Jun)"],
        "rotation": "Mustard or Wheat"
    },
    "Cotton": {
        "icon": "☁️", "color": "#9C27B0",
        "optimal_rainfall": (600, 1200), "optimal_temp": (20, 35),
        "soils": ["Black Cotton", "Sandy Loam", "Loamy"],
        "seasons": ["Kharif"],
        "water_need": "Medium-High", "growth_days": 160,
        "description": "Cash crop ideal for black soil regions with warm climate.",
        "market_value": "₹55-65/kg", "protein": "N/A",
        "irrigation": "Water every 10–12 days; 700–1200 mm total.",
        "economics": {"yield_per_acre": "0.8 tons", "price": "₹65/kg", "profit": "₹52,000/acre"},
        "calendar": ["Sowing (May-Jun)", "Squaring (Aug)", "Bols (Sep-Oct)", "Picking (Nov-Dec)"],
        "rotation": "Groundnut or Gram"
    },
    "Soybean": {
        "icon": "🫘", "color": "#8BC34A",
        "optimal_rainfall": (500, 900), "optimal_temp": (20, 30),
        "soils": ["Loamy", "Sandy Loam", "Clay"],
        "seasons": ["Kharif"],
        "water_need": "Medium", "growth_days": 100,
        "description": "Nitrogen-fixing legume with high protein content.",
        "market_value": "₹38-45/kg", "protein": "36.5g/100g",
        "irrigation": "Water every 7–10 days; 450–700 mm total.",
        "economics": {"yield_per_acre": "1.2 tons", "price": "₹45/kg", "profit": "₹54,000/acre"},
        "calendar": ["Sowing (Jun)", "Seedling (Jul)", "Flowering (Aug)", "Harvest (Sep-Oct)"],
        "rotation": "Wheat or Mustard"
    },
    "Sugarcane": {
        "icon": "🎋", "color": "#00BCD4",
        "optimal_rainfall": (1000, 2000), "optimal_temp": (25, 35),
        "soils": ["Loamy", "Clay", "Alluvial"],
        "seasons": ["Kharif", "Rabi", "Summer", "Winter"],
        "water_need": "Very High", "growth_days": 365,
        "description": "High-value cash crop for sugar and ethanol production.",
        "market_value": "₹3.1-3.5/kg", "protein": "N/A",
        "irrigation": "Water every 10–15 days; 1500–2500 mm total.",
        "economics": {"yield_per_acre": "35 tons", "price": "₹3.5/kg", "profit": "₹1,22,500/acre"},
        "calendar": ["Planting (Jan-Mar)", "Tillering (Apr-Jun)", "Growth (Jul-Oct)", "Harvest (Dec-Mar)"],
        "rotation": "Pulses or Green Manure"
    },
    "Groundnut": {
        "icon": "🥜", "color": "#795548",
        "optimal_rainfall": (400, 800), "optimal_temp": (22, 33),
        "soils": ["Sandy Loam", "Sandy", "Loamy"],
        "seasons": ["Kharif", "Rabi"],
        "water_need": "Low-Medium", "growth_days": 120,
        "description": "Drought-tolerant oilseed crop with sandy soil preference.",
        "market_value": "₹45-55/kg", "protein": "25.8g/100g",
        "irrigation": "Water every 12–15 days; 400–600 mm total.",
        "economics": {"yield_per_acre": "1.0 tons", "price": "₹55/kg", "profit": "₹55,000/acre"},
        "calendar": ["Sowing (Jun/Oct)", "Pegging (Jul/Nov)", "Pod formation (Aug/Dec)", "Harvest (Oct/Feb)"],
        "rotation": "Cotton or Sunflower"
    },
    "Tomato": {
        "icon": "🍅", "color": "#F44336",
        "optimal_rainfall": (400, 800), "optimal_temp": (18, 28),
        "soils": ["Sandy Loam", "Loamy", "Silty"],
        "seasons": ["Rabi", "Summer"],
        "water_need": "Medium", "growth_days": 75,
        "description": "High-value vegetable crop with good market demand.",
        "market_value": "₹15-40/kg", "protein": "0.9g/100g",
        "irrigation": "Water every 3–5 days; 400–600 mm total.",
        "economics": {"yield_per_acre": "8.0 tons", "price": "₹20/kg", "profit": "₹1,60,000/acre"},
        "calendar": ["Nursery (Nov-Dec)", "Transplant (Jan)", "Growth (Feb)", "Harvest (Mar-Apr)"],
        "rotation": "Beans or Cabbage"
    },
    "Chickpea": {
        "icon": "🌱", "color": "#607D8B",
        "optimal_rainfall": (300, 700), "optimal_temp": (15, 28),
        "soils": ["Sandy Loam", "Loamy", "Clay"],
        "seasons": ["Rabi", "Winter"],
        "water_need": "Low", "growth_days": 95,
        "description": "Drought-resistant pulse crop with high protein value.",
        "market_value": "₹55-70/kg", "protein": "19g/100g",
        "irrigation": "Water only if needed; 200–300 mm total.",
        "economics": {"yield_per_acre": "0.7 tons", "price": "₹70/kg", "profit": "₹49,000/acre"},
        "calendar": ["Sowing (Oct-Nov)", "Flowering (Jan)", "Podding (Feb)", "Harvest (Mar)"],
        "rotation": "Rice or Sorghum"
    },
    "Mustard": {
        "icon": "🌼", "color": "#FFEB3B",
        "optimal_rainfall": (250, 600), "optimal_temp": (10, 22),
        "soils": ["Loamy", "Sandy Loam", "Clay"],
        "seasons": ["Rabi", "Winter"],
        "water_need": "Low", "growth_days": 110,
        "description": "Cool-season oilseed crop with excellent drought tolerance.",
        "market_value": "₹48-58/kg", "protein": "25g/100g",
        "irrigation": "Water every 15–20 days; 250–400 mm total.",
        "economics": {"yield_per_acre": "0.6 tons", "price": "₹58/kg", "profit": "₹34,800/acre"},
        "calendar": ["Sowing (Oct)", "Vegetative (Nov-Dec)", "Flowering (Jan)", "Harvest (Feb-Mar)"],
        "rotation": "Maize or Pearl Millet"
    }
}

WEATHER_HISTORY: Dict[str, Dict[str, List[float]]] = {
    "Punjab": {"avg_rainfall": [45, 38, 52, 78, 92, 110, 185, 195, 125, 45, 12, 8], "avg_temp": [13, 16, 22, 30, 35, 38, 35, 33, 30, 25, 17, 13]},
    "Maharashtra": {"avg_rainfall": [8, 5, 12, 22, 58, 195, 285, 265, 185, 65, 18, 6], "avg_temp": [25, 27, 31, 35, 36, 30, 27, 27, 27, 28, 26, 24]},
    "Uttar Pradesh": {"avg_rainfall": [22, 18, 12, 8, 22, 95, 255, 265, 185, 38, 8, 12], "avg_temp": [14, 18, 25, 32, 37, 38, 34, 33, 30, 25, 18, 13]},
    "Tamil Nadu": {"avg_rainfall": [35, 22, 15, 28, 52, 45, 85, 125, 145, 295, 345, 155], "avg_temp": [28, 30, 33, 35, 36, 34, 32, 32, 31, 29, 27, 27]},
    "Gujarat": {"avg_rainfall": [5, 3, 4, 2, 8, 55, 175, 215, 115, 25, 8, 4], "avg_temp": [20, 23, 28, 34, 37, 36, 32, 30, 30, 28, 23, 19]},
    "Rajasthan": {"avg_rainfall": [8, 5, 4, 3, 5, 28, 115, 135, 55, 12, 4, 6], "avg_temp": [16, 20, 26, 33, 38, 38, 35, 33, 31, 26, 20, 15]},
    "West Bengal": {"avg_rainfall": [28, 35, 42, 82, 155, 285, 355, 315, 265, 165, 35, 12], "avg_temp": [19, 22, 27, 31, 33, 32, 30, 30, 30, 28, 23, 19]},
    "Madhya Pradesh": {"avg_rainfall": [18, 12, 8, 8, 22, 135, 325, 285, 185, 42, 12, 8], "avg_temp": [18, 22, 28, 34, 38, 36, 30, 28, 29, 27, 21, 17]},
    "Karnataka": {"avg_rainfall": [8, 12, 22, 45, 125, 65, 95, 115, 195, 195, 62, 22], "avg_temp": [24, 26, 30, 33, 33, 28, 26, 26, 26, 25, 23, 22]},
    "Andhra Pradesh": {"avg_rainfall": [12, 8, 12, 28, 65, 55, 115, 155, 155, 155, 85, 22], "avg_temp": [26, 28, 32, 35, 36, 33, 30, 30, 30, 28, 26, 25]},
}

DEFAULT_WEATHER: Dict[str, List[float]] = {"avg_rainfall": [25, 20, 15, 10, 30, 120, 220, 200, 150, 55, 20, 10], "avg_temp": [20, 22, 27, 32, 36, 35, 30, 29, 28, 25, 20, 18]}

def calculate_crop_score(crop_data: Dict[str, Any], user_data: Dict[str, Any]) -> Dict[str, Any]:
    # Scale monthly rainfall to annual for comparison with database ranges
    rainfall = float(user_data["rainfall"]) * 12
    temp = float(user_data["temperature"])
    soil = user_data["soil_type"]
    season = user_data["season"]

    r_min, r_max = crop_data["optimal_rainfall"]
    t_min, t_max = crop_data["optimal_temp"]

    # Rainfall score (0.0-40.0)
    r_center = (r_min + r_max) / 2.0
    r_range = (r_max - r_min) / 2.0
    if r_range == 0: r_range = 1.0
    r_score = max(0.0, 40.0 * (1.0 - abs(rainfall - r_center) / (r_range * 1.8)))

    # Temperature score (0.0-35.0)
    t_center = (t_min + t_max) / 2.0
    t_range = (t_max - t_min) / 2.0
    if t_range == 0: t_range = 1.0
    t_score = max(0.0, 35.0 * (1.0 - abs(temp - t_center) / (t_range * 1.8)))

    # Soil compatibility (0.0-15.0)
    s_score = 15.0 if soil in crop_data["soils"] else 4.0

    # Season compatibility (0.0-10.0)
    season_score = 10.0 if season in crop_data["seasons"] else 2.0

    total = r_score + t_score + s_score + season_score

    # Risk calculation
    deviation = abs(rainfall - r_center) / max(r_center, 1.0) + abs(temp - t_center) / max(t_center, 1.0)
    if deviation < 0.25:
        risk = "Low"
    elif deviation < 0.55:
        risk = "Medium"
    else:
        risk = "High"

    # Yield stability (0-100)
    yield_stability = min(100, int(total * 1.05))

    return {
        "score": round(float(total), 2),
        "risk": risk,
        "yield_stability": yield_stability,
        "rainfall_match": round(float(r_score) / 40.0 * 100.0),
        "temp_match": round(float(t_score) / 35.0 * 100.0),
        "soil_match": round(float(s_score) / 15.0 * 100.0),
        "season_match": round(float(season_score) / 10.0 * 100.0),
    }

def get_climate_risk_score(rainfall: float, temp: float, location: str) -> int:
    hist = WEATHER_HISTORY.get(location, DEFAULT_WEATHER)
    avg_annual = sum(hist["avg_rainfall"])
    avg_temp_annual = sum(hist["avg_temp"]) / 12.0

    rainfall_deviation = abs(rainfall - avg_annual / 12.0) / max(avg_annual / 12.0, 1.0)
    temp_deviation = abs(temp - avg_temp_annual) / max(avg_temp_annual, 1.0)

    risk_score = min(100, int((rainfall_deviation * 40.0 + temp_deviation * 30.0) * 2.5 + 20.0))
    return risk_score

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/planner")
def planner():
    return render_template("planner.html")

@app.route("/results")
def results():
    return render_template("results.html")

@app.route("/insights")
def insights():
    return render_template("insights.html")

@app.route("/doctor")
def doctor():
    return render_template("doctor.html")

@app.route("/api/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        if not data or not all(k in data for k in ["location", "rainfall", "temperature", "season", "soil_type"]):
            return jsonify({"error": "Missing required fields"}), 400

        try:
            user_rainfall = float(data["rainfall"])
            user_temp = float(data["temperature"])
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid rainfall or temperature values"}), 400

        scored_crops: List[Dict[str, Any]] = []

        for crop_name, crop_data in CROP_DATABASE.items():
            result = calculate_crop_score(crop_data, data)
            scored_crops.append({
                "name": crop_name,
                "icon": crop_data["icon"],
                "color": crop_data["color"],
                "description": crop_data["description"],
                "water_need": crop_data["water_need"],
                "growth_days": crop_data["growth_days"],
                "market_value": crop_data["market_value"],
                "protein": crop_data["protein"],
                "optimal_rainfall": crop_data["optimal_rainfall"],
                "optimal_temp": crop_data["optimal_temp"],
                "irrigation": crop_data.get("irrigation"),
                "economics": crop_data.get("economics"),
                "calendar": crop_data.get("calendar"),
                "rotation": crop_data.get("rotation"),
                **result
            })

        scored_crops.sort(key=lambda x: x["score"], reverse=True)
        top_3 = scored_crops[0:3]

        # Weather history for chart
        location = data.get("location", "Punjab")
        hist = WEATHER_HISTORY.get(location, DEFAULT_WEATHER)

        climate_risk = get_climate_risk_score(
            user_rainfall,
            user_temp,
            location
        )

        return jsonify({
            "recommendations": top_3,
            "all_crops": scored_crops,
            "weather_history": hist,
            "climate_risk_score": climate_risk,
            "location": location
        })
    except Exception as e:
        print(f"Error in prediction: {e}", file=sys.stderr)
        return jsonify({"error": "An internal error occurred during prediction"}), 500

@app.route("/api/weather/<location>")
def get_weather(location):
    hist = WEATHER_HISTORY.get(location, DEFAULT_WEATHER)
    return jsonify(hist)

@app.route("/api/locations")
def get_locations():
    return jsonify(list(WEATHER_HISTORY.keys()))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)


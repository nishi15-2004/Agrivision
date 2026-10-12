from flask import Flask, render_template, request, jsonify, session, redirect

import requests
import sqlite3
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

import torch
from torchvision import transforms, models
from PIL import Image


# =========================================================
# AGRIVISION SMART AGRICULTURE SYSTEM
# =========================================================

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get(
    "FLASK_SECRET_KEY",
    "agrivision-local-development-key-change-before-deployment"
)

DATABASE = "agrivision.db"

WEATHER_API_KEY = "e40d0386dea1d24b401dfba8e2908124"

UPLOAD_FOLDER = "static/uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.before_request
def require_login():
    public_routes = [
        "login",
        "signup",
        "api_login",
        "api_signup",
        "static"
    ]

    if request.endpoint is None:
        return None

    if request.endpoint in public_routes:
        return None

    if "user_id" not in session:
        return redirect("/login")


# =========================================================
# DATABASE
# =========================================================

def db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_users_table():
    conn = db_connection()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    finally:
        conn.close()


init_users_table()



# =========================================================
# GLOBAL LANGUAGE SYSTEM
# =========================================================

@app.context_processor
def inject_language_data():

    return {
        "language_system_enabled": True
    }

# =========================================================
# AGRIVISION MULTILINGUAL SYSTEM
# =========================================================

@app.route("/api/languages")
def get_languages():

    conn = db_connection()

    try:

        languages = conn.execute("""
            SELECT
                id,
                code,
                name,
                native_name
            FROM languages
            WHERE is_active = 1
            ORDER BY
                CASE
                    WHEN code = 'en' THEN 0
                    ELSE 1
                END,
                name
        """).fetchall()

        return jsonify({
            "languages": [
                dict(row)
                for row in languages
            ]
        })

    except sqlite3.Error as e:

        return jsonify({
            "error": "Unable to load languages.",
            "languages": []
        }), 500

    finally:

        conn.close()


# =========================================================
# TRANSLATIONS
# =========================================================

@app.route("/api/translations/<language>")
def get_translations(language):

    language = (
        language
        .strip()
        .lower()
    )

    conn = db_connection()

    try:

        # Check language exists

        language_row = conn.execute("""
            SELECT id, code
            FROM languages
            WHERE code = ?
            AND is_active = 1
            LIMIT 1
        """, (language,)).fetchone()

        if not language_row:

            return jsonify({
                "error": "Language not found.",
                "language": language,
                "translations": {}
            }), 404


        translations = conn.execute("""
            SELECT
                t.translation_key,
                t.translated_text
            FROM translations t

            WHERE t.language_id = ?

            ORDER BY t.translation_key
        """, (
            language_row["id"],
        )).fetchall()


        return jsonify({

            "language":
            language,

            "translations": {

                row["translation_key"]:
                row["translated_text"]

                for row in translations

            }

        })


    except sqlite3.Error as e:

        return jsonify({

            "error":
            "Unable to load translations.",

            "translations":
            {}

        }), 500


    finally:

        conn.close()


# =========================================================
# SINGLE TRANSLATION HELPER
# =========================================================

def get_translation(language, key, default_text):

    if not language:
        return default_text

    language = language.strip().lower()

    conn = db_connection()

    try:

        result = conn.execute("""
            SELECT
                t.translated_text
            FROM translations t
            JOIN languages l
                ON t.language_id = l.id
            WHERE l.code = ?
            AND t.translation_key = ?
            LIMIT 1
        """, (
            language,
            key
        )).fetchone()

        if result:
            return result["translated_text"]

        return default_text

    except sqlite3.Error:

        return default_text

    finally:

        conn.close()


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():
    print("HOME ROUTE CHECK:", dict(session))

    if "user_id" not in session:
        return redirect("/login")

    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/api/signup", methods=["POST"])
def api_signup():
    data = request.get_json(silent=True) or {}

    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or not email or not password:
        return jsonify({
            "success": False,
            "message": "Please fill in all fields."
        }), 400

    if len(password) < 8:
        return jsonify({
            "success": False,
            "message": "Password must be at least 8 characters."
        }), 400

    conn = db_connection()
    try:
        conn.execute(
            """
            INSERT INTO users (name, email, password_hash)
            VALUES (?, ?, ?)
            """,
            (name, email, generate_password_hash(password))
        )
        conn.commit()

        return jsonify({
            "success": True,
            "message": "Account created successfully."
        }), 201

    except sqlite3.IntegrityError:
        return jsonify({
            "success": False,
            "message": "This email is already registered."
        }), 409

    finally:
        conn.close()

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json(silent=True) or {}

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    conn = db_connection()
    try:
        user = conn.execute(
            """
            SELECT id, name, email, password_hash
            FROM users
            WHERE email = ?
            LIMIT 1
            """,
            (email,)
        ).fetchone()
    finally:
        conn.close()

    if not user or not check_password_hash(
        user["password_hash"], password
    ):
        return jsonify({
            "success": False,
            "message": "Invalid email or password."
        }), 401

    session["user_id"] = user["id"]
    session["user_name"] = user["name"]

    return jsonify({
        "success": True,
        "redirect": "/"
    })

# =========================================================
# WEATHER
# =========================================================

@app.route("/weather", methods=["GET", "POST"])
def weather():

    weather_data = None
    forecast = []
    advice = ""
    error = None

    lat = request.args.get("lat")
    lon = request.args.get("lon")

    city = request.form.get(
        "city",
        ""
    ).strip()


    # -----------------------------------------------------
    # CURRENT LOCATION
    # -----------------------------------------------------

    if lat and lon:

        weather_url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?lat={lat}"
            f"&lon={lon}"
            f"&appid={WEATHER_API_KEY}"
            "&units=metric"
        )

        forecast_url = (
            "https://api.openweathermap.org/data/2.5/forecast"
            f"?lat={lat}"
            f"&lon={lon}"
            f"&appid={WEATHER_API_KEY}"
            "&units=metric"
        )


    # -----------------------------------------------------
    # CITY SEARCH
    # -----------------------------------------------------

    elif request.method == "POST":

        if not city:

            return render_template(
                "weather.html",
                weather=None,
                forecast=[],
                advice="",
                error="Please enter a city name."
            )

        weather_url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}"
            f"&appid={WEATHER_API_KEY}"
            "&units=metric"
        )

        forecast_url = (
            "https://api.openweathermap.org/data/2.5/forecast"
            f"?q={city}"
            f"&appid={WEATHER_API_KEY}"
            "&units=metric"
        )


    else:

        return render_template(
            "weather.html",
            weather=None,
            forecast=[],
            advice="",
            error=None
        )


    # -----------------------------------------------------
    # WEATHER API
    # -----------------------------------------------------

    try:

        response = requests.get(
            weather_url,
            timeout=15
        )

    except requests.exceptions.RequestException:

        return render_template(
            "weather.html",
            weather=None,
            forecast=[],
            advice="",
            error="Unable to connect to weather service."
        )


    if response.status_code != 200:

        return render_template(
            "weather.html",
            weather=None,
            forecast=[],
            advice="",
            error="Weather data not found."
        )


    data = response.json()


    # -----------------------------------------------------
    # WEATHER DATA
    # -----------------------------------------------------

    weather_data = {

        "city":
        data.get("name", "-"),

        "temp":
        round(
            data.get(
                "main",
                {}
            ).get(
                "temp",
                0
            )
        ),

        "temp_max":
        round(
            data.get(
                "main",
                {}
            ).get(
                "temp_max",
                0
            )
        ),

        "temp_min":
        round(
            data.get(
                "main",
                {}
            ).get(
                "temp_min",
                0
            )
        ),

        "humidity":
        data.get(
            "main",
            {}
        ).get(
            "humidity",
            0
        ),

        "pressure":
        data.get(
            "main",
            {}
        ).get(
            "pressure",
            0
        ),

        "wind":
        round(
            data.get(
                "wind",
                {}
            ).get(
                "speed",
                0
            ),
            1
        ),

        "visibility":
        round(
            data.get(
                "visibility",
                0
            ) / 1000,
            1
        ),

        "condition":
        data.get(
            "weather",
            [{"description": "Unknown"}]
        )[0].get(
            "description",
            "Unknown"
        ).title(),

        "icon":
        data.get(
            "weather",
            [{"icon": "01d"}]
        )[0].get(
            "icon",
            "01d"
        ),

        "sunrise":
        datetime.fromtimestamp(
            data.get(
                "sys",
                {}
            ).get(
                "sunrise",
                0
            )
        ).strftime("%I:%M %p")
        if data.get(
            "sys",
            {}
        ).get(
            "sunrise"
        )
        else "-",

        "sunset":
        datetime.fromtimestamp(
            data.get(
                "sys",
                {}
            ).get(
                "sunset",
                0
            )
        ).strftime("%I:%M %p")
        if data.get(
            "sys",
            {}
        ).get(
            "sunset"
        )
        else "-"
    }


    # -----------------------------------------------------
    # FARMER WEATHER ADVICE
    # -----------------------------------------------------

    condition = data.get(
        "weather",
        [{"description": ""}]
    )[0].get(
        "description",
        ""
    ).lower()

    temperature = data.get(
        "main",
        {}
    ).get(
        "temp",
        0
    )

    humidity = data.get(
        "main",
        {}
    ).get(
        "humidity",
        0
    )

    wind_speed = data.get(
        "wind",
        {}
    ).get(
        "speed",
        0
    )


    if "rain" in condition:

        advice = (
            "🌧 Rain expected. "
            "Avoid irrigation and pesticide spraying."
        )

    elif temperature > 35:

        advice = (
            "🌞 High temperature. "
            "Water crops during morning or evening."
        )

    elif humidity > 80:

        advice = (
            "🌿 High humidity. "
            "Check crops for fungal diseases."
        )

    elif wind_speed > 8:

        advice = (
            "💨 Strong wind. "
            "Avoid pesticide spraying."
        )

    else:

        advice = (
            "✅ Weather conditions are suitable for farming."
        )


    # -----------------------------------------------------
    # FORECAST
    # -----------------------------------------------------

    try:

        forecast_response = requests.get(
            forecast_url,
            timeout=15
        )

    except requests.exceptions.RequestException:

        forecast_response = None


    if (
        forecast_response
        and forecast_response.status_code == 200
    ):

        forecast_data = forecast_response.json()

        selected_items = forecast_data.get(
            "list",
            []
        )[::8]


        for item in selected_items:

            degrees = item.get(
                "wind",
                {}
            ).get(
                "deg",
                0
            )


            if degrees >= 337 or degrees < 22:
                direction = "N"

            elif degrees < 67:
                direction = "NE"

            elif degrees < 112:
                direction = "E"

            elif degrees < 157:
                direction = "SE"

            elif degrees < 202:
                direction = "S"

            elif degrees < 247:
                direction = "SW"

            elif degrees < 292:
                direction = "W"

            else:
                direction = "NW"


            forecast.append({

                "day":
                item.get(
                    "dt_txt",
                    "-"
                ).split(" ")[0],

                "temp":
                round(
                    item.get(
                        "main",
                        {}
                    ).get(
                        "temp",
                        0
                    )
                ),

                "condition":
                item.get(
                    "weather",
                    [{"description": "Unknown"}]
                )[0].get(
                    "description",
                    "Unknown"
                ).title(),

                "icon":
                item.get(
                    "weather",
                    [{"icon": "01d"}]
                )[0].get(
                    "icon",
                    "01d"
                ),

                "rain":
                round(
                    item.get(
                        "pop",
                        0
                    ) * 100
                ),

                "wind_direction":
                direction
            })


    return render_template(
        "weather.html",
        weather=weather_data,
        forecast=forecast,
        advice=advice,
        error=error
    )


# =========================================================
# MULTI-CROP DISEASE AI (228 DISEASE CLASSES / 203 CROPS)
# =========================================================

MULTICROP_MODEL_PATH = "models/multicrop_model.pth"

multicrop_model = None
multicrop_classes = []

multicrop_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])


def load_multicrop_model():
    global multicrop_model, multicrop_classes

    if not os.path.exists(MULTICROP_MODEL_PATH):
        print("WARNING: multicrop_model.pth not found.")
        return

    try:
        checkpoint = torch.load(
            MULTICROP_MODEL_PATH,
            map_location="cpu",
            weights_only=False
        )

        multicrop_classes = checkpoint["classes"]

        multicrop_model = models.resnet18(weights=None)
        multicrop_model.fc = torch.nn.Linear(
            multicrop_model.fc.in_features,
            len(multicrop_classes)
        )
        multicrop_model.load_state_dict(checkpoint["model_state"])
        multicrop_model.eval()

        print(
            f"Multi-crop AI model loaded successfully: "
            f"{len(multicrop_classes)} classes."
        )

    except Exception as e:
        multicrop_model = None
        print("ERROR loading multicrop model:", e)


load_multicrop_model()


# =========================================================
# DISEASE PAGE
# =========================================================

@app.route("/disease", methods=["GET", "POST"])
def disease():

    result = None
    image_path = None

    if request.method == "POST":

        file = request.files.get("leaf_image")
        crop = request.form.get("crop", "").strip().lower()

        if not file or not file.filename:
            result = {
                "disease": "Please upload a leaf image.",
                "confidence": 0,
                "treatment": "Upload a clear crop leaf image.",
                "prevention": "Use a well-lit image showing the affected leaf."
            }

        elif not multicrop_model:
            result = {
                "disease": "Multi-crop AI model is not available.",
                "confidence": 0,
                "treatment": "Please check models/multicrop_model.pth.",
                "prevention": "Make sure the recovered multi-crop model is present."
            }

        else:
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
            filename = f"{timestamp}_{filename}"

            save_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )
            file.save(save_path)

            image_path = "/" + save_path.replace("\\", "/")

            try:
                image = Image.open(save_path).convert("RGB")
                image = multicrop_transform(image).unsqueeze(0)

                with torch.no_grad():
                    output = multicrop_model(image)
                    probabilities = torch.softmax(output, dim=1)
                    confidence, predicted = torch.max(probabilities, 1)

                predicted_class = multicrop_classes[predicted.item()]
                confidence_value = round(confidence.item() * 100, 2)

                if "___" in predicted_class:
                    predicted_crop, predicted_disease = predicted_class.split("___", 1)
                else:
                    predicted_crop = "Unknown crop"
                    predicted_disease = predicted_class

                predicted_crop_display = predicted_crop.replace("_", " ")
                predicted_disease_display = predicted_disease.replace("_", " ")

                if "healthy" in predicted_disease.lower():
                    treatment = (
                        "The AI model classified the uploaded image as healthy. "
                        "Continue regular crop monitoring and recommended farm practices."
                    )
                    prevention = (
                        "Maintain proper irrigation, nutrition, field hygiene and "
                        "regularly inspect leaves for early symptoms."
                    )
                else:
                    treatment = (
                        f"AI prediction: {predicted_disease_display}. "
                        "Remove severely affected plant material where appropriate "
                        "and consult an agriculture expert before using pesticides or fungicides."
                    )
                    prevention = (
                        "Monitor nearby plants, maintain proper spacing and field hygiene, "
                        "avoid excess moisture and use crop-specific recommended practices."
                    )

                if crop:
                    selected_crop_display = crop.replace("_", " ")
                    if selected_crop_display != predicted_crop_display.lower():
                        prevention += (
                            f" The selected crop was {selected_crop_display}, while the model "
                            f"predicted {predicted_crop_display}; verify the image and crop "
                            "selection before taking treatment action."
                        )

                result = {
                    "disease": f"{predicted_crop_display}: {predicted_disease_display}",
                    "confidence": confidence_value,
                    "treatment": treatment,
                    "prevention": prevention
                }

            except Exception as e:
                print("Disease prediction error:", e)
                result = {
                    "disease": "Prediction failed.",
                    "confidence": 0,
                    "treatment": "Please try another clear crop image.",
                    "prevention": "Upload a clear, well-lit image with the affected leaf visible."
                }

    return render_template(
        "disease.html",
        result=result,
        image_path=image_path
    )


# =========================================================
# MARKET PRICE
# =========================================================
MARKET_API_KEY = "579b464db66ec23bdd0000015cdc410d7c554abf6b51a47d8498c4e9Y"


MARKET_RESOURCE_ID = (
    "9ef84268-d588-465a-a308-a864a43d0070"
)


@app.route("/market")
def market():

    return render_template(
        "market.html"
    )


@app.route("/api/market-prices")
def market_prices():

    crop = request.args.get(
        "crop",
        ""
    ).strip()

    state = request.args.get(
        "state",
        ""
    ).strip()

    district = request.args.get(
        "district",
        ""
    ).strip()

    mandi = request.args.get(
        "mandi",
        ""
    ).strip()


    if not MARKET_API_KEY:

        return jsonify({

            "error":
            "Market API key is not configured yet.",

            "records":
            []

        }), 503


    api_url = (
        "https://api.data.gov.in/resource/"
        + MARKET_RESOURCE_ID
    )


    params = {

        "api-key":
        MARKET_API_KEY,

        "format":
        "json",

        "limit":
        100
    }


    if crop:
        params["filters[commodity]"] = crop

    if state:
        params["filters[state]"] = state

    if district:
        params["filters[district]"] = district

    if mandi:
        params["filters[market]"] = mandi


    try:

        response = requests.get(
            api_url,
            params=params,
            timeout=15
        )


        if response.status_code != 200:

            return jsonify({

                "error":
                "Government market API returned an error.",

                "records":
                []

            }), response.status_code


        data = response.json()

        records = []


        for item in data.get(
            "records",
            []
        ):

            records.append({

                "commodity":
                item.get(
                    "commodity",
                    "-"
                ),

                "state":
                item.get(
                    "state",
                    "-"
                ),

                "district":
                item.get(
                    "district",
                    "-"
                ),

                "market":
                item.get(
                    "market",
                    "-"
                ),

                "variety":
                item.get(
                    "variety",
                    "-"
                ),

                "min_price":
                item.get(
                    "min_price",
                    "-"
                ),

                "max_price":
                item.get(
                    "max_price",
                    "-"
                ),

                "modal_price":
                item.get(
                    "modal_price",
                    "-"
                ),

                "date":
                item.get(
                    "arrival_date"
                )
                or
                item.get(
                    "date"
                )
                or
                "-"
            })


        return jsonify({
            "records": records
        })


    except requests.exceptions.RequestException as e:

     return jsonify({
        "error": "Unable to connect to market data service.",
        "details": str(e),
        "records": []
    }), 503


# =========================================================
# GOVERNMENT SCHEMES
# =========================================================

@app.route("/schemes")
def schemes():

    return render_template(
        "schemes.html"
    )


# =========================================================
# COMPENSATION PAGE
# =========================================================

@app.route("/compensation")
def compensation():

    return render_template(
        "compensation.html"
    )


# =========================================================
# STATES
# =========================================================

@app.route(
    "/api/compensation/states"
)
def compensation_states():

    conn = db_connection()

    try:

        states = conn.execute("""
            SELECT
                id,
                name
            FROM states
            ORDER BY name
        """).fetchall()


        return jsonify({

            "states":
            [
                dict(row)
                for row in states
            ]

        })

    finally:

        conn.close()


# =========================================================
# DISTRICTS
# =========================================================

@app.route(
    "/api/compensation/districts/<int:state_id>"
)
def compensation_districts(
    state_id
):

    conn = db_connection()

    try:

        districts = conn.execute("""
            SELECT
                id,
                name
            FROM districts
            WHERE state_id = ?
            ORDER BY name
        """, (
            state_id,
        )).fetchall()


        return jsonify({

            "districts":
            [
                dict(row)
                for row in districts
            ]

        })

    finally:

        conn.close()


# =========================================================
# CROPS
# =========================================================

@app.route(
    "/api/compensation/crops"
)
def compensation_crops():

    conn = db_connection()

    try:

        crops = conn.execute("""
            SELECT
                id,
                name,
                category
            FROM crops
            ORDER BY
                category,
                name
        """).fetchall()


        return jsonify({

            "crops":
            [
                dict(row)
                for row in crops
            ]

        })

    finally:

        conn.close()


# =========================================================
# DAMAGE TYPES
# =========================================================

@app.route(
    "/api/compensation/damage-types"
)
def compensation_damage_types():

    conn = db_connection()

    try:

        damage_types = conn.execute("""
            SELECT
                id,
                name,
                description
            FROM damage_types
            ORDER BY name
        """).fetchall()


        return jsonify({

            "damage_types":
            [
                dict(row)
                for row in damage_types
            ]

        })

    finally:

        conn.close()


# =========================================================
# IMMEDIATE ACTION GUIDE
# =========================================================

DAMAGE_ACTION_GUIDE = {

    1: {
        "title": "Flood / Excess Water",
        "icon": "🌊",
        "first_steps": [
            "Ensure your safety first and avoid unsafe flooded areas.",
            "Take clear photos and videos of the damaged crop.",
            "Document waterlogging and the affected field area.",
            "Record the date, location, crop and approximate affected area.",
            "Do not remove damaged crop before checking the applicable assessment process."
        ],
        "evidence": [
            "Photos/videos of damaged crop",
            "Photos of waterlogging",
            "Date and location",
            "Crop and affected-area details"
        ],
        "report": "Report the loss through the applicable crop insurance or government reporting process."
    },


    2: {
        "title": "Drought",
        "icon": "☀️",
        "first_steps": [
            "Take clear photos/videos showing the drought-related crop damage.",
            "Record the crop and sowing details.",
            "Estimate and record the affected area.",
            "Preserve available rainfall, moisture or field-condition evidence.",
            "Check the applicable insurance and government reporting requirements."
        ],
        "evidence": [
            "Photos of dry/damaged crop",
            "Field photos",
            "Crop and sowing details",
            "Affected area"
        ],
        "report": "Report the loss through the applicable crop insurance or government procedure."
    },


    3: {
        "title": "Hailstorm",
        "icon": "🧊",
        "first_steps": [
            "Take photos/videos of the damaged crop as soon as it is safe.",
            "Photograph hail damage on leaves, stems, fruits or grains.",
            "Record the date and location of the hailstorm.",
            "Record the affected crop and approximate affected area.",
            "Preserve damage evidence before removing damaged crop."
        ],
        "evidence": [
            "Hail-damaged crop photos",
            "Field photos/videos",
            "Incident date",
            "Affected area"
        ],
        "report": "Report the damage through the applicable crop insurance or government reporting channel."
    },


    4: {
        "title": "Cyclone / Storm",
        "icon": "🌪️",
        "first_steps": [
            "Ensure your safety before entering the field.",
            "Take photos/videos after the storm has passed.",
            "Document fallen plants, broken stems and field damage.",
            "Record the incident date, location and affected area.",
            "Preserve important evidence for damage assessment."
        ],
        "evidence": [
            "Photos of fallen/damaged plants",
            "Field damage photos/videos",
            "Date and location",
            "Affected area"
        ],
        "report": "Follow the applicable crop insurance or government loss-reporting process."
    },


    5: {
        "title": "Fire / Lightning",
        "icon": "🔥",
        "first_steps": [
            "Ensure your safety first.",
            "If the fire is active, contact appropriate emergency assistance.",
            "After the incident, photograph and record the crop damage.",
            "Record the approximate burned area.",
            "Preserve evidence needed for damage assessment."
        ],
        "evidence": [
            "Burnt crop photos/videos",
            "Affected-field photos",
            "Incident date",
            "Affected area"
        ],
        "report": "Verify applicable insurance and local authority reporting requirements and report the loss."
    },


    6: {
        "title": "Pest Attack",
        "icon": "🐛",
        "first_steps": [
            "Take clear close-up photos of affected leaves, stems, fruits or plants.",
            "Do not spray pesticides without confirming the pest and recommended treatment.",
            "Record the affected crop stage and approximate affected area.",
            "Take photos of both healthy and affected plants.",
            "Consult an agriculture expert or local agriculture department."
        ],
        "evidence": [
            "Close-up pest photos",
            "Affected crop photos",
            "Crop variety",
            "Affected area"
        ],
        "report": "Check applicable crop protection and insurance reporting requirements."
    },


    7: {
        "title": "Crop Disease",
        "icon": "🌿",
        "first_steps": [
            "Take clear close-up photos of diseased leaves and plants.",
            "Take comparison photos of healthy and affected plants.",
            "Record the approximate affected area.",
            "Do not apply pesticides or fungicides without proper identification.",
            "Consult an agriculture expert for disease identification and treatment."
        ],
        "evidence": [
            "Disease-symptom photos",
            "Affected-field photos",
            "Crop variety",
            "Approximate disease spread"
        ],
        "report": "Verify the applicable crop insurance or agriculture department reporting process."
    },


    8: {
        "title": "Prevented Sowing",
        "icon": "🌱",
        "first_steps": [
            "Record why sowing could not take place.",
            "Take photos/videos of the field condition.",
            "Keep evidence showing that the field was prepared for sowing.",
            "Preserve available seed and fertilizer purchase records.",
            "Check the applicable scheme notification and reporting requirements."
        ],
        "evidence": [
            "Field photos",
            "Sowing-related records",
            "Seed/fertilizer records where available",
            "Date and location"
        ],
        "report": "Follow the applicable notified-area and insurance reporting procedure."
    },


    9: {
        "title": "Post-Harvest Loss",
        "icon": "🌾",
        "first_steps": [
            "Take photos/videos of harvested crop and damaged produce.",
            "Document the storage location and damage.",
            "Record the harvest date.",
            "Estimate and record the affected quantity.",
            "Check whether the loss falls within applicable post-harvest coverage conditions."
        ],
        "evidence": [
            "Damaged harvested crop photos",
            "Storage/location photos",
            "Harvest date",
            "Approximate quantity"
        ],
        "report": "Follow the applicable post-harvest loss reporting process."
    },


    10: {
        "title": "Localized Calamity",
        "icon": "📍",
        "first_steps": [
            "Take clear photos/videos of the affected crop and field.",
            "Record the incident date and field location.",
            "Record crop details and approximate affected area.",
            "Preserve all damage evidence.",
            "Verify the applicable local calamity and insurance reporting process."
        ],
        "evidence": [
            "Crop damage photos/videos",
            "Field location",
            "Incident date",
            "Affected area"
        ],
        "report": "Follow the applicable local calamity and crop insurance reporting procedure."
    }
}


# =========================================================
# ACTION GUIDE API
# =========================================================

@app.route(
    "/api/compensation/action-guide/<int:damage_type_id>"
)
def compensation_action_guide(
    damage_type_id
):

    guide = DAMAGE_ACTION_GUIDE.get(
        damage_type_id
    )


    if not guide:

        return jsonify({
            "error":
            "Action guide not available for this damage type."
        }), 404


    return jsonify({
        "damage_type_id":
        damage_type_id,

        "guide":
        guide
    })


# =========================================================
# CROP-SPECIFIC COMPENSATION
# =========================================================

@app.route(
    "/api/compensation"
)
def compensation_information():

    state_id = request.args.get(
        "state_id",
        type=int
    )

    district_id = request.args.get(
        "district_id",
        type=int
    )

    crop_id = request.args.get(
        "crop_id",
        type=int
    )

    damage_type_id = request.args.get(
        "damage_type_id",
        type=int
    )


    if not all([
        state_id,
        district_id,
        crop_id,
        damage_type_id
    ]):

        return jsonify({

            "error":
            "State, district, crop and damage type are required.",

            "compensation":
            None

        }), 400


    conn = db_connection()

    try:

        record = conn.execute("""
            SELECT

                compensation.id,

                states.name
                    AS state_name,

                districts.name
                    AS district_name,

                crops.id
                    AS crop_id,

                crops.name
                    AS crop_name,

                crops.category
                    AS crop_category,

                damage_types.id
                    AS damage_type_id,

                damage_types.name
                    AS damage_type_name,

                damage_types.description
                    AS damage_description,

                schemes.id
                    AS scheme_id,

                schemes.name
                    AS scheme_name,

                schemes.description
                    AS scheme_description,

                schemes.official_url
                    AS official_url,

                compensation.eligibility,

                compensation.coverage,

                compensation.claim_process,

                compensation.source

            FROM compensation

            JOIN states
                ON compensation.state_id =
                   states.id

            JOIN districts
                ON compensation.district_id =
                   districts.id

            JOIN crops
                ON compensation.crop_id =
                   crops.id

            JOIN damage_types
                ON compensation.damage_type_id =
                   damage_types.id

            JOIN schemes
                ON compensation.scheme_id =
                   schemes.id

            WHERE compensation.state_id = ?

            AND compensation.district_id = ?

            AND compensation.crop_id = ?

            AND compensation.damage_type_id = ?

            LIMIT 1
        """, (
            state_id,
            district_id,
            crop_id,
            damage_type_id
        )).fetchone()


        action_guide = DAMAGE_ACTION_GUIDE.get(
            damage_type_id
        )


        if not record:

            return jsonify({

                "compensation":
                None,

                "action_guide":
                action_guide,

                "message":
                "No exact crop-specific compensation record was found for this combination."
            })


        return jsonify({

            "compensation":
            dict(record),

            "action_guide":
            action_guide,

            "message":
            "Crop-specific compensation information found."
        })


    except sqlite3.Error as e:

        return jsonify({

            "error":
            "Database error while retrieving compensation information.",

            "details":
            str(e),

            "compensation":
            None

        }), 500

    finally:

        conn.close()


# =========================================================
# COMPENSATION SUMMARY
# =========================================================

@app.route(
    "/api/compensation/summary"
)
def compensation_summary():

    conn = db_connection()

    try:

        total_crops = conn.execute("""
            SELECT COUNT(*)
            FROM crops
        """).fetchone()[0]


        total_states = conn.execute("""
            SELECT COUNT(*)
            FROM states
        """).fetchone()[0]


        total_districts = conn.execute("""
            SELECT COUNT(*)
            FROM districts
        """).fetchone()[0]


        total_damage_types = conn.execute("""
            SELECT COUNT(*)
            FROM damage_types
        """).fetchone()[0]


        total_records = conn.execute("""
            SELECT COUNT(*)
            FROM compensation
        """).fetchone()[0]


        crop_specific_records = conn.execute("""
            SELECT COUNT(*)
            FROM compensation
            WHERE crop_id IS NOT NULL
        """).fetchone()[0]


        return jsonify({

            "crops":
            total_crops,

            "states":
            total_states,

            "districts":
            total_districts,

            "damage_types":
            total_damage_types,

            "total_compensation_records":
            total_records,

            "crop_specific_records":
            crop_specific_records
        })


    finally:

        conn.close()


# =========================================================
# FARMER HELP
# =========================================================

@app.route("/help")
def help():

    return render_template(
        "help.html"
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/api/health")
def health():

    conn = db_connection()

    try:

        conn.execute(
            "SELECT 1"
        ).fetchone()

        return jsonify({

            "status":
            "ok",

            "database":
            "connected"
        })

    except Exception as e:

        return jsonify({

            "status":
            "error",

            "database":
            str(e)

        }), 500

    finally:

        conn.close()


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("AGRIVISION SMART AGRICULTURE SYSTEM")
    print("=" * 60)
    print("Database:", DATABASE)
    print("Server: http://127.0.0.1:5000")
    print("=" * 60)

    app.run(
        debug=True
    )
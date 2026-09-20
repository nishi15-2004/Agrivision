import sqlite3


DATABASE = "agrivision.db"


TRANSLATIONS = {

    "site_title": {
        "en": "Agrivision"
    },

    "brand_name": {
        "en": "🌾 Agrivision"
    },

    "home_title": {
        "en": "Smart Agriculture Support System"
    },

    "nav_home": {
        "en": "Home"
    },

    "nav_weather": {
        "en": "Weather"
    },

    "nav_disease": {
        "en": "Disease Detection"
    },

    "nav_schemes": {
        "en": "Government Schemes"
    },

    "nav_compensation": {
        "en": "Compensation"
    },

    "nav_market": {
        "en": "Market Prices"
    },

    "nav_help": {
        "en": "Help"
    },

    "welcome": {
        "en": "Welcome Farmers 👨‍🌾"
    },

    "hero_description": {
        "en": "Get weather updates, crop disease detection, government schemes and compensation information in one place."
    },

    "explore_now": {
        "en": "Explore Now"
    },

    "our_services": {
        "en": "Our Services"
    },

    "weather_title": {
        "en": "Weather Updates"
    },

    "weather_description": {
        "en": "Get real-time weather forecasts for better farming decisions."
    },

    "disease_title": {
        "en": "Disease Detection"
    },

    "disease_description": {
        "en": "Upload crop images and identify diseases quickly."
    },

    "schemes_title": {
        "en": "Government Schemes"
    },

    "schemes_description": {
        "en": "Discover the latest schemes and subsidies available for farmers."
    },

    "compensation_title": {
        "en": "Compensation"
    },

    "compensation_description": {
        "en": "Check crop damage compensation and insurance support."
    },

    "market_title": {
        "en": "Market Prices"
    },

    "market_description": {
        "en": "Stay updated with daily mandi prices."
    },

    "help_title": {
        "en": "Farmer Help"
    },

    "help_description": {
        "en": "Get support through FAQs and emergency contact information."
    },

    "why_choose": {
        "en": "Why Choose Agrivision?"
    },

    "live_weather": {
        "en": "Live Weather"
    },

    "live_weather_description": {
        "en": "Accurate weather updates to help farmers plan irrigation and harvesting."
    },

    "smart_detection": {
        "en": "Smart Detection"
    },

    "smart_detection_description": {
        "en": "Identify crop diseases quickly using image-based detection."
    },

    "government_support": {
        "en": "Government Support"
    },

    "government_support_description": {
        "en": "Access important schemes and compensation information in one place."
    },

    "agrivision_impact": {
        "en": "Agrivision Impact"
    },

    "farmers_helped": {
        "en": "Farmers Helped"
    },

    "crop_varieties": {
        "en": "Crop Varieties"
    },

    "districts_covered": {
        "en": "Districts Covered"
    },

    "government_schemes": {
        "en": "Government Schemes"
    },

    "latest_farming_tips": {
        "en": "Latest Farming Tips"
    },

    "smart_irrigation": {
        "en": "💧 Smart Irrigation"
    },

    "smart_irrigation_description": {
        "en": "Water crops early in the morning or evening to reduce evaporation and save water."
    },

    "healthy_soil": {
        "en": "🌱 Healthy Soil"
    },

    "healthy_soil_description": {
        "en": "Use organic compost and rotate crops regularly to improve soil fertility."
    },

    "pest_management": {
        "en": "🐛 Pest Management"
    },

    "pest_management_description": {
        "en": "Inspect crops regularly and use appropriate crop-protection methods."
    },

    "footer_description": {
        "en": "Smart Agriculture Support System for Indian Farmers."
    },

    "email_label": {
        "en": "Email"
    },

    "phone_label": {
        "en": "Phone"
    },

    "copyright": {
        "en": "© 2026 Agrivision. All Rights Reserved."
    }
}


conn = sqlite3.connect(DATABASE)

cursor = conn.cursor()


# ---------------------------------------------------------
# Get language IDs
# ---------------------------------------------------------

languages = cursor.execute("""
    SELECT id, code
    FROM languages
    WHERE is_active = 1
""").fetchall()


language_ids = {
    code: language_id
    for language_id, code in languages
}


print("=" * 60)
print("ADDING AGRIVISION HOMEPAGE TRANSLATIONS")
print("=" * 60)


new_count = 0
existing_count = 0


# ---------------------------------------------------------
# English entries
# ---------------------------------------------------------

for key, language_data in TRANSLATIONS.items():

    for language_code, text in language_data.items():

        if language_code not in language_ids:
            continue


        language_id = language_ids[language_code]


        existing = cursor.execute("""
            SELECT id
            FROM translations
            WHERE language_id = ?
            AND translation_key = ?
            LIMIT 1
        """, (
            language_id,
            key
        )).fetchone()


        if existing:

            existing_count += 1

            continue


        cursor.execute("""
            INSERT INTO translations
            (
                language_id,
                translation_key,
                translated_text
            )
            VALUES (?, ?, ?)
        """, (
            language_id,
            key,
            text
        ))


        new_count += 1


conn.commit()

conn.close()


print()
print("TRANSLATION DATABASE UPDATED")
print("-" * 60)
print("New translations :", new_count)
print("Already existed   :", existing_count)
print("-" * 60)
print("DONE")
print("=" * 60)
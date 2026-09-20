import sqlite3

DATABASE = "agrivision.db"

# ============================================================
# AGRIVISION MULTILINGUAL DATABASE
# English + 22 Indian Scheduled Languages
# ============================================================

LANGUAGES = [

    ("en", "English", "English"),

    ("as", "Assamese", "অসমীয়া"),
    ("bn", "Bengali", "বাংলা"),
    ("brx", "Bodo", "बड़ो"),
    ("doi", "Dogri", "डोगरी"),
    ("gu", "Gujarati", "ગુજરાતી"),
    ("hi", "Hindi", "हिन्दी"),
    ("kn", "Kannada", "ಕನ್ನಡ"),
    ("ks", "Kashmiri", "कॉशुर"),
    ("kok", "Konkani", "कोंकणी"),
    ("mai", "Maithili", "मैथिली"),
    ("ml", "Malayalam", "മലയാളം"),
    ("mni", "Manipuri", "মৈতৈলোন্"),
    ("mr", "Marathi", "मराठी"),
    ("ne", "Nepali", "नेपाली"),
    ("or", "Odia", "ଓଡ଼ିଆ"),
    ("pa", "Punjabi", "ਪੰਜਾਬੀ"),
    ("sa", "Sanskrit", "संस्कृतम्"),
    ("sat", "Santali", "ᱥᱟᱱᱛᱟᱲᱤ"),
    ("sd", "Sindhi", "سنڌي"),
    ("ta", "Tamil", "தமிழ்"),
    ("te", "Telugu", "తెలుగు"),
    ("ur", "Urdu", "اردو")
]


# ============================================================
# COMMON WEBSITE TRANSLATIONS
# ============================================================

TRANSLATIONS = {

    "home": {
        "en": "Home",
        "hi": "होम",
        "bn": "হোম",
        "gu": "હોમ",
        "mr": "मुख्यपृष्ठ",
        "ta": "முகப்பு",
        "te": "హోమ్",
        "kn": "ಮುಖಪುಟ",
        "ml": "ഹോം",
        "pa": "ਮੁੱਖ ਪੰਨਾ",
        "or": "ମୁଖ୍ୟ ପୃଷ୍ଠା",
        "as": "মুখ্য পৃষ্ঠা",
        "ne": "गृहपृष्ठ"
    },

    "weather": {
        "en": "Weather",
        "hi": "मौसम",
        "bn": "আবহাওয়া",
        "gu": "હવામાન",
        "mr": "हवामान",
        "ta": "வானிலை",
        "te": "వాతావరణం",
        "kn": "ಹವಾಮಾನ",
        "ml": "കാലാവസ്ഥ",
        "pa": "ਮੌਸਮ",
        "or": "ପାଣିପାଗ",
        "as": "বতৰ",
        "ne": "मौसम"
    },

    "disease_detection": {
        "en": "Disease Detection",
        "hi": "रोग पहचान",
        "bn": "রোগ শনাক্তকরণ",
        "gu": "રોગ ઓળખ",
        "mr": "रोग ओळख",
        "ta": "நோய் கண்டறிதல்",
        "te": "వ్యాధి గుర్తింపు",
        "kn": "ರೋಗ ಪತ್ತೆ",
        "ml": "രോഗ നിർണയം",
        "pa": "ਰੋਗ ਪਛਾਣ",
        "or": "ରୋଗ ଚିହ୍ନଟ",
        "as": "ৰোগ চিনাক্তকৰণ",
        "ne": "रोग पहिचान"
    },

    "market_prices": {
        "en": "Market Prices",
        "hi": "बाजार भाव",
        "bn": "বাজার মূল্য",
        "gu": "બજાર ભાવ",
        "mr": "बाजार भाव",
        "ta": "சந்தை விலை",
        "te": "మార్కెట్ ధరలు",
        "kn": "ಮಾರುಕಟ್ಟೆ ಬೆಲೆ",
        "ml": "വിപണി വില",
        "pa": "ਮੰਡੀ ਭਾਅ",
        "or": "ବଜାର ଦର",
        "as": "বজাৰৰ মূল্য",
        "ne": "बजार मूल्य"
    },

    "government_schemes": {
        "en": "Government Schemes",
        "hi": "सरकारी योजनाएं",
        "bn": "সরকারি প্রকল্প",
        "gu": "સરકારી યોજનાઓ",
        "mr": "सरकारी योजना",
        "ta": "அரசு திட்டங்கள்",
        "te": "ప్రభుత్వ పథకాలు",
        "kn": "ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು",
        "ml": "സർക്കാർ പദ്ധതികൾ",
        "pa": "ਸਰਕਾਰੀ ਯੋਜਨਾਵਾਂ",
        "or": "ସରକାରୀ ଯୋଜନା",
        "as": "চৰকাৰী আঁচনি",
        "ne": "सरकारी योजनाहरू"
    },

    "compensation": {
        "en": "Crop Damage Compensation",
        "hi": "फसल नुकसान मुआवजा",
        "bn": "ফসল ক্ষতিপূরণ",
        "gu": "પાક નુકસાન વળતર",
        "mr": "पीक नुकसान भरपाई",
        "ta": "பயிர் சேத இழப்பீடு",
        "te": "పంట నష్ట పరిహారం",
        "kn": "ಬೆಳೆ ಹಾನಿ ಪರಿಹಾರ",
        "ml": "വിള നാശ നഷ്ടപരിഹാരം",
        "pa": "ਫਸਲ ਨੁਕਸਾਨ ਮੁਆਵਜ਼ਾ",
        "or": "ଫସଲ କ୍ଷତିପୂରଣ",
        "as": "শস্য ক্ষতিপূৰণ",
        "ne": "बाली क्षतिपूर्ति"
    },

    "help": {
        "en": "Farmer Help",
        "hi": "किसान सहायता",
        "bn": "কৃষক সহায়তা",
        "gu": "ખેડૂત સહાય",
        "mr": "शेतकरी मदत",
        "ta": "விவசாயி உதவி",
        "te": "రైతు సహాయం",
        "kn": "ರೈತ ಸಹಾಯ",
        "ml": "കർഷക സഹായം",
        "pa": "ਕਿਸਾਨ ਸਹਾਇਤਾ",
        "or": "କୃଷକ ସହାୟତା",
        "as": "কৃষক সহায়তা",
        "ne": "किसान सहायता"
    },

    "state": {
        "en": "State / Union Territory",
        "hi": "राज्य / केंद्र शासित प्रदेश",
        "bn": "রাজ্য / কেন্দ্রশাসিত অঞ্চল",
        "gu": "રાજ્ય / કેન્દ્રશાસિત પ્રદેશ",
        "mr": "राज्य / केंद्रशासित प्रदेश",
        "ta": "மாநிலம் / யூனியன் பிரதேசம்",
        "te": "రాష్ట్రం / కేంద్ర పాలిత ప్రాంతం",
        "kn": "ರಾಜ್ಯ / ಕೇಂದ್ರಾಡಳಿತ ಪ್ರದೇಶ",
        "ml": "സംസ്ഥാനം / കേന്ദ്രഭരണ പ്രദേശം",
        "pa": "ਰਾਜ / ਕੇਂਦਰ ਸ਼ਾਸਿਤ ਪ੍ਰਦੇਸ਼",
        "or": "ରାଜ୍ୟ / କେନ୍ଦ୍ରଶାସିତ ଅଞ୍ଚଳ",
        "as": "ৰাজ্য / কেন্দ্ৰীয় শাসিত অঞ্চল",
        "ne": "राज्य / केन्द्र शासित प्रदेश"
    },

    "district": {
        "en": "District",
        "hi": "जिला",
        "bn": "জেলা",
        "gu": "જિલ્લો",
        "mr": "जिल्हा",
        "ta": "மாவட்டம்",
        "te": "జిల్లా",
        "kn": "ಜಿಲ್ಲೆ",
        "ml": "ജില്ല",
        "pa": "ਜ਼ਿਲ੍ਹਾ",
        "or": "ଜିଲ୍ଲା",
        "as": "জিলা",
        "ne": "जिल्ला"
    },

    "crop": {
        "en": "Crop",
        "hi": "फसल",
        "bn": "ফসল",
        "gu": "પાક",
        "mr": "पीक",
        "ta": "பயிர்",
        "te": "పంట",
        "kn": "ಬೆಳೆ",
        "ml": "വിള",
        "pa": "ਫਸਲ",
        "or": "ଫସଲ",
        "as": "শস্য",
        "ne": "बाली"
    },

    "damage": {
        "en": "Type of Damage",
        "hi": "नुकसान का प्रकार",
        "bn": "ক্ষতির ধরন",
        "gu": "નુકસાનનો પ્રકાર",
        "mr": "नुकसानाचा प्रकार",
        "ta": "சேதத்தின் வகை",
        "te": "నష్టం రకం",
        "kn": "ಹಾನಿಯ ವಿಧ",
        "ml": "നാശത്തിന്റെ തരം",
        "pa": "ਨੁਕਸਾਨ ਦੀ ਕਿਸਮ",
        "or": "କ୍ଷତିର ପ୍ରକାର",
        "as": "ক্ষতিৰ ধৰণ",
        "ne": "क्षतिको प्रकार"
    },

    "find_support": {
        "en": "Find Available Support",
        "hi": "उपलब्ध सहायता खोजें",
        "bn": "উপলব্ধ সহায়তা খুঁজুন",
        "gu": "ઉપલબ્ધ સહાય શોધો",
        "mr": "उपलब्ध मदत शोधा",
        "ta": "கிடைக்கும் உதவியைக் கண்டறியவும்",
        "te": "అందుబాటులో ఉన్న సహాయాన్ని కనుగొనండి",
        "kn": "ಲಭ್ಯವಿರುವ ಸಹಾಯವನ್ನು ಹುಡುಕಿ",
        "ml": "ലഭ്യമായ സഹായം കണ്ടെത്തുക",
        "pa": "ਉਪਲਬਧ ਸਹਾਇਤਾ ਲੱਭੋ",
        "or": "ଉପଲବ୍ଧ ସହାୟତା ଖୋଜନ୍ତୁ",
        "as": "উপলব্ধ সহায়তা বিচাৰক",
        "ne": "उपलब्ध सहायता खोज्नुहोस्"
    },

    "immediate_action": {
        "en": "What Should You Do First?",
        "hi": "सबसे पहले क्या करें?",
        "bn": "প্রথমে কী করবেন?",
        "gu": "સૌ પ્રથમ શું કરવું?",
        "mr": "सर्वप्रथम काय करावे?",
        "ta": "முதலில் என்ன செய்ய வேண்டும்?",
        "te": "ముందుగా ఏమి చేయాలి?",
        "kn": "ಮೊದಲು ಏನು ಮಾಡಬೇಕು?",
        "ml": "ആദ്യം എന്ത് ചെയ്യണം?",
        "pa": "ਸਭ ਤੋਂ ਪਹਿਲਾਂ ਕੀ ਕਰਨਾ ਚਾਹੀਦਾ ਹੈ?",
        "or": "ପ୍ରଥମେ କଣ କରିବେ?",
        "as": "প্ৰথমে কি কৰিব?",
        "ne": "सबैभन्दा पहिले के गर्ने?"
    },

    "eligibility": {
        "en": "Eligibility",
        "hi": "पात्रता",
        "bn": "যোগ্যতা",
        "gu": "પાત્રતા",
        "mr": "पात्रता",
        "ta": "தகுதி",
        "te": "అర్హత",
        "kn": "ಅರ್ಹತೆ",
        "ml": "യോഗ്യത",
        "pa": "ਯੋਗਤਾ",
        "or": "ଯୋଗ୍ୟତା",
        "as": "যোগ্যতা",
        "ne": "योग्यता"
    },

    "coverage": {
        "en": "Coverage / Compensation",
        "hi": "कवरेज / मुआवजा",
        "bn": "কভারেজ / ক্ষতিপূরণ",
        "gu": "કવરેજ / વળતર",
        "mr": "कव्हरेज / भरपाई",
        "ta": "காப்பீடு / இழப்பீடு",
        "te": "కవరేజ్ / పరిహారం",
        "kn": "ಕವರೇಜ್ / ಪರಿಹಾರ",
        "ml": "പരിരക്ഷ / നഷ്ടപരിഹാരം",
        "pa": "ਕਵਰੇਜ / ਮੁਆਵਜ਼ਾ",
        "or": "କଭରେଜ୍ / କ୍ଷତିପୂରଣ",
        "as": "কভাৰেজ / ক্ষতিপূৰণ",
        "ne": "कभरेज / क्षतिपूर्ति"
    },

    "claim_process": {
        "en": "Claim Process",
        "hi": "दावा प्रक्रिया",
        "bn": "দাবি প্রক্রিয়া",
        "gu": "દાવા પ્રક્રિયા",
        "mr": "दावा प्रक्रिया",
        "ta": "கோரிக்கை செயல்முறை",
        "te": "క్లెయిమ్ ప్రక్రియ",
        "kn": "ಕ್ಲೈಮ್ ಪ್ರಕ್ರಿಯೆ",
        "ml": "ക്ലെയിം നടപടിക്രമം",
        "pa": "ਦਾਅਵਾ ਪ੍ਰਕਿਰਿਆ",
        "or": "ଦାବି ପ୍ରକ୍ରିୟା",
        "as": "দাবী প্ৰক্ৰিয়া",
        "ne": "दाबी प्रक्रिया"
    },

    "important": {
        "en": "Important Information",
        "hi": "महत्वपूर्ण जानकारी",
        "bn": "গুরুত্বপূর্ণ তথ্য",
        "gu": "મહત્વપૂર્ણ માહિતી",
        "mr": "महत्त्वाची माहिती",
        "ta": "முக்கியமான தகவல்",
        "te": "ముఖ్యమైన సమాచారం",
        "kn": "ಪ್ರಮುಖ ಮಾಹಿತಿ",
        "ml": "പ്രധാനപ്പെട്ട വിവരങ്ങൾ",
        "pa": "ਮਹੱਤਵਪੂਰਨ ਜਾਣਕਾਰੀ",
        "or": "ଗୁରୁତ୍ୱପୂର୍ଣ୍ଣ ସୂଚନା",
        "as": "গুৰুত্বপূৰ্ণ তথ্য",
        "ne": "महत्त्वपूर्ण जानकारी"
    }
}


# ============================================================
# DATABASE SETUP
# ============================================================

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

print("=" * 60)
print("AGRIVISION MULTILINGUAL DATABASE SETUP")
print("=" * 60)


# ------------------------------------------------------------
# LANGUAGES TABLE
# ------------------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS languages (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    code TEXT UNIQUE NOT NULL,

    name TEXT NOT NULL,

    native_name TEXT NOT NULL,

    is_active INTEGER DEFAULT 1

)
""")


# ------------------------------------------------------------
# TRANSLATIONS TABLE
# ------------------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS translations (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    language_id INTEGER NOT NULL,

    translation_key TEXT NOT NULL,

    translated_text TEXT NOT NULL,

    FOREIGN KEY(language_id)
        REFERENCES languages(id),

    UNIQUE(language_id, translation_key)

)
""")


# ------------------------------------------------------------
# INSERT LANGUAGES
# ------------------------------------------------------------

for code, name, native_name in LANGUAGES:

    cursor.execute("""
        INSERT OR IGNORE INTO languages
        (code, name, native_name, is_active)

        VALUES (?, ?, ?, 1)
    """, (
        code,
        name,
        native_name
    ))


# ------------------------------------------------------------
# INSERT TRANSLATIONS
# ------------------------------------------------------------

inserted = 0
skipped = 0

for key, language_data in TRANSLATIONS.items():

    for language_code, text in language_data.items():

        cursor.execute("""
            SELECT id
            FROM languages
            WHERE code = ?
        """, (language_code,))

        row = cursor.fetchone()

        if not row:
            continue

        language_id = row[0]

        cursor.execute("""
            INSERT OR IGNORE INTO translations
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

        if cursor.rowcount:
            inserted += 1
        else:
            skipped += 1


conn.commit()


# ============================================================
# SUMMARY
# ============================================================

language_count = cursor.execute("""
    SELECT COUNT(*)
    FROM languages
""").fetchone()[0]

translation_count = cursor.execute("""
    SELECT COUNT(*)
    FROM translations
""").fetchone()[0]


print()
print("MULTILINGUAL DATABASE READY")
print("-" * 60)
print("Languages available :", language_count)
print("Translations stored :", translation_count)
print("New translations    :", inserted)
print("Already existed     :", skipped)
print("-" * 60)

print()
print("LANGUAGES:")

for row in cursor.execute("""
    SELECT code, name, native_name
    FROM languages
    ORDER BY id
""").fetchall():

    print(
        f"{row[0]:5} | "
        f"{row[1]:15} | "
        f"{row[2]}"
    )


conn.close()

print()
print("=" * 60)
print("SETUP COMPLETE")
print("=" * 60)
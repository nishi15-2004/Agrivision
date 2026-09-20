import sqlite3

DATABASE = "agrivision.db"


# ============================================================
# INDIAN CROP MASTER LIST
# ============================================================

CROPS = [

    # ========================================================
    # CEREALS
    # ========================================================

    ("Cereal", "Rice"),
    ("Cereal", "Wheat"),
    ("Cereal", "Maize"),
    ("Cereal", "Sorghum (Jowar)"),
    ("Cereal", "Pearl Millet (Bajra)"),
    ("Cereal", "Finger Millet (Ragi)"),
    ("Cereal", "Foxtail Millet"),
    ("Cereal", "Little Millet"),
    ("Cereal", "Kodo Millet"),
    ("Cereal", "Barnyard Millet"),
    ("Cereal", "Proso Millet"),
    ("Cereal", "Browntop Millet"),
    ("Cereal", "Cheena"),
    ("Cereal", "Barley"),
    ("Cereal", "Oats"),
    ("Cereal", "Buckwheat"),
    ("Cereal", "Job's Tears"),
    ("Cereal", "Amaranth Grain"),
    ("Cereal", "Quinoa"),
    ("Cereal", "Triticale"),
    ("Cereal", "Rye"),

    # ========================================================
    # PULSES
    # ========================================================

    ("Pulse", "Chickpea (Gram)"),
    ("Pulse", "Pigeon Pea (Arhar/Tur)"),
    ("Pulse", "Green Gram (Moong)"),
    ("Pulse", "Black Gram (Urad)"),
    ("Pulse", "Lentil (Masoor)"),
    ("Pulse", "Field Pea"),
    ("Pulse", "Cowpea (Lobia)"),
    ("Pulse", "Horse Gram"),
    ("Pulse", "Moth Bean"),
    ("Pulse", "Cluster Bean (Guar)"),
    ("Pulse", "Kidney Bean (Rajma)"),
    ("Pulse", "Lathyrus (Khesari)"),
    ("Pulse", "Faba Bean"),
    ("Pulse", "Rice Bean"),
    ("Pulse", "Mung Bean"),
    ("Pulse", "Indian Bean"),
    ("Pulse", "Black Eyed Pea"),
    ("Pulse", "Broad Bean"),
    ("Pulse", "Velvet Bean"),
    ("Pulse", "Winged Bean"),

    # ========================================================
    # OILSEEDS
    # ========================================================

    ("Oilseed", "Groundnut"),
    ("Oilseed", "Soybean"),
    ("Oilseed", "Mustard"),
    ("Oilseed", "Rapeseed"),
    ("Oilseed", "Linseed"),
    ("Oilseed", "Sesame"),
    ("Oilseed", "Sunflower"),
    ("Oilseed", "Safflower"),
    ("Oilseed", "Castor"),
    ("Oilseed", "Niger Seed"),
    ("Oilseed", "Toria"),
    ("Oilseed", "Yellow Sarson"),
    ("Oilseed", "Brown Sarson"),
    ("Oilseed", "Canola"),
    ("Oilseed", "Safflower"),
    ("Oilseed", "Perilla"),
    ("Oilseed", "Coconut"),
    ("Oilseed", "Oil Palm"),
    ("Oilseed", "Cottonseed"),

    # ========================================================
    # VEGETABLES
    # ========================================================

    ("Vegetable", "Potato"),
    ("Vegetable", "Sweet Potato"),
    ("Vegetable", "Yam"),
    ("Vegetable", "Elephant Foot Yam"),
    ("Vegetable", "Taro (Arbi)"),
    ("Vegetable", "Cassava"),
    ("Vegetable", "Onion"),
    ("Vegetable", "Garlic"),
    ("Vegetable", "Ginger"),
    ("Vegetable", "Tomato"),
    ("Vegetable", "Brinjal"),
    ("Vegetable", "Okra (Bhindi)"),
    ("Vegetable", "Cabbage"),
    ("Vegetable", "Cauliflower"),
    ("Vegetable", "Broccoli"),
    ("Vegetable", "Knol-Khol"),
    ("Vegetable", "Carrot"),
    ("Vegetable", "Radish"),
    ("Vegetable", "Turnip"),
    ("Vegetable", "Beetroot"),
    ("Vegetable", "Spinach"),
    ("Vegetable", "Amaranth Leaf"),
    ("Vegetable", "Fenugreek Leaf"),
    ("Vegetable", "Mustard Greens"),
    ("Vegetable", "Drumstick"),
    ("Vegetable", "Green Peas"),
    ("Vegetable", "French Bean"),
    ("Vegetable", "Broad Bean"),
    ("Vegetable", "Cluster Bean"),
    ("Vegetable", "Cowpea Vegetable"),
    ("Vegetable", "Bitter Gourd"),
    ("Vegetable", "Bottle Gourd"),
    ("Vegetable", "Ridge Gourd"),
    ("Vegetable", "Sponge Gourd"),
    ("Vegetable", "Snake Gourd"),
    ("Vegetable", "Pointed Gourd"),
    ("Vegetable", "Ivy Gourd"),
    ("Vegetable", "Ash Gourd"),
    ("Vegetable", "Pumpkin"),
    ("Vegetable", "Cucumber"),
    ("Vegetable", "Capsicum"),
    ("Vegetable", "Green Chilli"),
    ("Vegetable", "Red Chilli"),
    ("Vegetable", "Mushroom"),
    ("Vegetable", "Asparagus"),
    ("Vegetable", "Celery"),
    ("Vegetable", "Leek"),
    ("Vegetable", "Lettuce"),
    ("Vegetable", "Parsley"),
    ("Vegetable", "Zucchini"),
    ("Vegetable", "Sweet Corn"),
    ("Vegetable", "Baby Corn"),
    ("Vegetable", "Brussels Sprout"),

    # ========================================================
    # FRUITS
    # ========================================================

    ("Fruit", "Mango"),
    ("Fruit", "Banana"),
    ("Fruit", "Apple"),
    ("Fruit", "Guava"),
    ("Fruit", "Papaya"),
    ("Fruit", "Grapes"),
    ("Fruit", "Orange"),
    ("Fruit", "Sweet Orange (Mosambi)"),
    ("Fruit", "Mandarin"),
    ("Fruit", "Lemon"),
    ("Fruit", "Lime"),
    ("Fruit", "Pomegranate"),
    ("Fruit", "Pineapple"),
    ("Fruit", "Watermelon"),
    ("Fruit", "Muskmelon"),
    ("Fruit", "Coconut"),
    ("Fruit", "Jackfruit"),
    ("Fruit", "Litchi"),
    ("Fruit", "Ber"),
    ("Fruit", "Custard Apple"),
    ("Fruit", "Sapota (Chikoo)"),
    ("Fruit", "Aonla"),
    ("Fruit", "Bael"),
    ("Fruit", "Tamarind"),
    ("Fruit", "Fig"),
    ("Fruit", "Strawberry"),
    ("Fruit", "Peach"),
    ("Fruit", "Pear"),
    ("Fruit", "Plum"),
    ("Fruit", "Apricot"),
    ("Fruit", "Kiwi"),
    ("Fruit", "Dragon Fruit"),
    ("Fruit", "Avocado"),
    ("Fruit", "Passion Fruit"),
    ("Fruit", "Mulberry"),
    ("Fruit", "Karonda"),
    ("Fruit", "Phalsa"),
    ("Fruit", "Jamun"),
    ("Fruit", "Wood Apple"),
    ("Fruit", "Mangosteen"),
    ("Fruit", "Rambutan"),
    ("Fruit", "Longan"),
    ("Fruit", "Persimmon"),
    ("Fruit", "Cherry"),
    ("Fruit", "Nectarine"),
    ("Fruit", "Star Fruit"),
    ("Fruit", "Fig"),
    ("Fruit", "Loquat"),

    # ========================================================
    # SPICES
    # ========================================================

    ("Spice", "Black Pepper"),
    ("Spice", "Cardamom"),
    ("Spice", "Small Cardamom"),
    ("Spice", "Large Cardamom"),
    ("Spice", "Clove"),
    ("Spice", "Cinnamon"),
    ("Spice", "Nutmeg"),
    ("Spice", "Mace"),
    ("Spice", "Turmeric"),
    ("Spice", "Cumin"),
    ("Spice", "Coriander"),
    ("Spice", "Fennel"),
    ("Spice", "Fenugreek"),
    ("Spice", "Ajwain"),
    ("Spice", "Dill"),
    ("Spice", "Mustard Seed"),
    ("Spice", "Dry Chilli"),
    ("Spice", "Ginger"),
    ("Spice", "Garlic"),
    ("Spice", "Tamarind"),
    ("Spice", "Saffron"),
    ("Spice", "Star Anise"),
    ("Spice", "Bay Leaf"),
    ("Spice", "Curry Leaf"),
    ("Spice", "Kokum"),
    ("Spice", "Poppy Seed"),
    ("Spice", "Celery Seed"),
    ("Spice", "Nigella (Kalonji)"),
    ("Spice", "Vanilla"),

    # ========================================================
    # COMMERCIAL CROPS
    # ========================================================

    ("Commercial", "Sugarcane"),
    ("Commercial", "Cotton"),
    ("Commercial", "Jute"),
    ("Commercial", "Mesta"),
    ("Commercial", "Tobacco"),
    ("Commercial", "Tea"),
    ("Commercial", "Coffee"),
    ("Commercial", "Rubber"),
    ("Commercial", "Arecanut"),
    ("Commercial", "Betel Leaf"),
    ("Commercial", "Cocoa"),
    ("Commercial", "Cashew"),
    ("Commercial", "Oil Palm"),
    ("Commercial", "Coconut"),
    ("Commercial", "Bamboo"),

    # ========================================================
    # FIBRE CROPS
    # ========================================================

    ("Fibre", "Cotton"),
    ("Fibre", "Jute"),
    ("Fibre", "Mesta"),
    ("Fibre", "Flax"),
    ("Fibre", "Hemp"),
    ("Fibre", "Ramie"),
    ("Fibre", "Sunn Hemp"),
    ("Fibre", "Kenaf"),
    ("Fibre", "Sisal"),

    # ========================================================
    # FODDER
    # ========================================================

    ("Fodder", "Berseem"),
    ("Fodder", "Lucerne"),
    ("Fodder", "Napier Grass"),
    ("Fodder", "Fodder Maize"),
    ("Fodder", "Fodder Sorghum"),
    ("Fodder", "Fodder Bajra"),
    ("Fodder", "Oat Fodder"),
    ("Fodder", "Cowpea Fodder"),
    ("Fodder", "Guinea Grass"),
    ("Fodder", "Para Grass"),
    ("Fodder", "Stylo"),
    ("Fodder", "Marvel Grass"),
    ("Fodder", "Rhodes Grass"),

    # ========================================================
    # MEDICINAL CROPS
    # ========================================================

    ("Medicinal", "Ashwagandha"),
    ("Medicinal", "Aloe Vera"),
    ("Medicinal", "Isabgol"),
    ("Medicinal", "Senna"),
    ("Medicinal", "Safed Musli"),
    ("Medicinal", "Kalmegh"),
    ("Medicinal", "Brahmi"),
    ("Medicinal", "Shatavari"),
    ("Medicinal", "Sarpagandha"),
    ("Medicinal", "Stevia"),
    ("Medicinal", "Giloy"),
    ("Medicinal", "Tulsi"),
    ("Medicinal", "Lemongrass"),
    ("Medicinal", "Citronella"),
    ("Medicinal", "Vetiver"),
    ("Medicinal", "Coleus"),
    ("Medicinal", "Mentha"),

    # ========================================================
    # AROMATIC CROPS
    # ========================================================

    ("Aromatic", "Lemongrass"),
    ("Aromatic", "Citronella"),
    ("Aromatic", "Palmarosa"),
    ("Aromatic", "Vetiver"),
    ("Aromatic", "Patchouli"),
    ("Aromatic", "Rosemary"),
    ("Aromatic", "Lavender"),
    ("Aromatic", "Geranium"),
    ("Aromatic", "Mint"),
    ("Aromatic", "Basil"),

    # ========================================================
    # FLOWERS / FLORICULTURE
    # ========================================================

    ("Floriculture", "Rose"),
    ("Floriculture", "Marigold"),
    ("Floriculture", "Jasmine"),
    ("Floriculture", "Chrysanthemum"),
    ("Floriculture", "Gladiolus"),
    ("Floriculture", "Tuberose"),
    ("Floriculture", "Gerbera"),
    ("Floriculture", "Carnation"),
    ("Floriculture", "Orchid"),
    ("Floriculture", "Lilium"),
    ("Floriculture", "Crossandra"),
    ("Floriculture", "Anthurium"),
    ("Floriculture", "Aster"),
    ("Floriculture", "Dahlia"),
    ("Floriculture", "Petunia"),

    # ========================================================
    # TUBER / ROOT CROPS
    # ========================================================

    ("Tuber", "Cassava"),
    ("Tuber", "Potato"),
    ("Tuber", "Sweet Potato"),
    ("Tuber", "Taro"),
    ("Tuber", "Elephant Foot Yam"),
    ("Tuber", "Greater Yam"),
    ("Tuber", "Lesser Yam"),
    ("Tuber", "Arrowroot"),
    ("Tuber", "Colocasia"),
    ("Tuber", "Dioscorea"),

    # ========================================================
    # OTHER SPECIALTY CROPS
    # ========================================================

    ("Other", "Makhana"),
    ("Other", "Lotus"),
    ("Other", "Bamboo"),
    ("Other", "Bee Forage Crops"),
    ("Other", "Stevia"),
    ("Other", "Chia"),
    ("Other", "Flax"),
    ("Other", "Sesame Specialty"),
    ("Other", "Moringa"),
    ("Other", "Drumstick Seed"),
    ("Other", "Chia Seed"),
    ("Other", "Sunflower Specialty"),
]


# ============================================================
# DATABASE UPDATE
# ============================================================

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()


# Make sure table exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS crops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    category TEXT NOT NULL
)
""")


# Insert only crops that do not already exist
inserted = 0
skipped = 0

for category, name in CROPS:

    cursor.execute("""
        SELECT id
        FROM crops
        WHERE LOWER(name) = LOWER(?)
    """, (name,))

    existing = cursor.fetchone()

    if existing:

        skipped += 1

    else:

        cursor.execute("""
            INSERT INTO crops (name, category)
            VALUES (?, ?)
        """, (name, category))

        inserted += 1


conn.commit()


# ============================================================
# DISPLAY RESULT
# ============================================================

total = cursor.execute(
    "SELECT COUNT(*) FROM crops"
).fetchone()[0]


print()
print("=" * 50)
print("AGRIVISION CROP DATABASE UPDATED")
print("=" * 50)
print("New crops inserted :", inserted)
print("Already existed    :", skipped)
print("TOTAL CROPS NOW    :", total)
print("=" * 50)


conn.close()
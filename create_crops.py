import sqlite3

DATABASE = "agrivision.db"

crops = [

    # Cereals
    ("Rice", "Cereal"),
    ("Wheat", "Cereal"),
    ("Maize", "Cereal"),
    ("Sorghum (Jowar)", "Cereal"),
    ("Pearl Millet (Bajra)", "Cereal"),
    ("Finger Millet (Ragi)", "Cereal"),
    ("Foxtail Millet", "Cereal"),
    ("Little Millet", "Cereal"),
    ("Kodo Millet", "Cereal"),
    ("Proso Millet", "Cereal"),
    ("Barnyard Millet", "Cereal"),
    ("Barley", "Cereal"),
    ("Oats", "Cereal"),
    ("Buckwheat", "Cereal"),

    # Pulses
    ("Chickpea (Gram)", "Pulse"),
    ("Pigeon Pea (Arhar)", "Pulse"),
    ("Green Gram (Moong)", "Pulse"),
    ("Black Gram (Urad)", "Pulse"),
    ("Lentil (Masoor)", "Pulse"),
    ("Field Pea", "Pulse"),
    ("Cowpea", "Pulse"),
    ("Moth Bean", "Pulse"),
    ("Horse Gram", "Pulse"),
    ("Kidney Bean (Rajma)", "Pulse"),
    ("Cluster Bean (Guar)", "Pulse"),

    # Oilseeds
    ("Mustard", "Oilseed"),
    ("Rapeseed", "Oilseed"),
    ("Soybean", "Oilseed"),
    ("Groundnut", "Oilseed"),
    ("Sunflower", "Oilseed"),
    ("Sesame", "Oilseed"),
    ("Safflower", "Oilseed"),
    ("Castor", "Oilseed"),
    ("Linseed", "Oilseed"),
    ("Niger Seed", "Oilseed"),
    ("Oil Palm", "Oilseed"),
    ("Coconut", "Oilseed"),

    # Vegetables
    ("Potato", "Vegetable"),
    ("Tomato", "Vegetable"),
    ("Onion", "Vegetable"),
    ("Garlic", "Vegetable"),
    ("Ginger", "Vegetable"),
    ("Carrot", "Vegetable"),
    ("Radish", "Vegetable"),
    ("Turnip", "Vegetable"),
    ("Beetroot", "Vegetable"),
    ("Sweet Potato", "Vegetable"),
    ("Colocasia (Arbi)", "Vegetable"),
    ("Yam", "Vegetable"),
    ("Cabbage", "Vegetable"),
    ("Cauliflower", "Vegetable"),
    ("Broccoli", "Vegetable"),
    ("Brinjal", "Vegetable"),
    ("Okra (Bhindi)", "Vegetable"),
    ("Capsicum", "Vegetable"),
    ("Green Chilli", "Vegetable"),
    ("Peas", "Vegetable"),
    ("Cucumber", "Vegetable"),
    ("Bottle Gourd", "Vegetable"),
    ("Bitter Gourd", "Vegetable"),
    ("Ridge Gourd", "Vegetable"),
    ("Sponge Gourd", "Vegetable"),
    ("Pumpkin", "Vegetable"),
    ("Snake Gourd", "Vegetable"),
    ("French Bean", "Vegetable"),
    ("Drumstick", "Vegetable"),
    ("Spinach", "Vegetable"),
    ("Fenugreek", "Vegetable"),

    # Fruits
    ("Apple", "Fruit"),
    ("Banana", "Fruit"),
    ("Mango", "Fruit"),
    ("Guava", "Fruit"),
    ("Papaya", "Fruit"),
    ("Grapes", "Fruit"),
    ("Orange", "Fruit"),
    ("Sweet Orange (Mosambi)", "Fruit"),
    ("Mandarin", "Fruit"),
    ("Lemon", "Fruit"),
    ("Lime", "Fruit"),
    ("Pomegranate", "Fruit"),
    ("Watermelon", "Fruit"),
    ("Muskmelon", "Fruit"),
    ("Pineapple", "Fruit"),
    ("Jackfruit", "Fruit"),
    ("Lychee", "Fruit"),
    ("Peach", "Fruit"),
    ("Plum", "Fruit"),
    ("Pear", "Fruit"),
    ("Apricot", "Fruit"),
    ("Strawberry", "Fruit"),
    ("Ber", "Fruit"),
    ("Custard Apple", "Fruit"),
    ("Dragon Fruit", "Fruit"),
    ("Kiwi", "Fruit"),
    ("Chikoo (Sapota)", "Fruit"),
    ("Fig", "Fruit"),
    ("Avocado", "Fruit"),

    # Commercial crops
    ("Cotton", "Commercial"),
    ("Sugarcane", "Commercial"),
    ("Jute", "Commercial"),
    ("Tobacco", "Commercial"),
    ("Tea", "Commercial"),
    ("Coffee", "Commercial"),
    ("Rubber", "Commercial"),
    ("Arecanut", "Commercial"),
    ("Betel Leaf", "Commercial"),

    # Spices
    ("Black Pepper", "Spice"),
    ("Cardamom", "Spice"),
    ("Turmeric", "Spice"),
    ("Dry Chilli", "Spice"),
    ("Coriander", "Spice"),
    ("Cumin", "Spice"),
    ("Fennel", "Spice"),
    ("Fenugreek Seed", "Spice"),
    ("Ajwain", "Spice"),
    ("Clove", "Spice"),
    ("Cinnamon", "Spice"),
    ("Nutmeg", "Spice"),
    ("Tamarind", "Spice"),
    ("Bay Leaf", "Spice"),

    # Fibre
    ("Mesta", "Fibre"),
    ("Flax", "Fibre"),
    ("Hemp", "Fibre"),

    # Fodder
    ("Berseem", "Fodder"),
    ("Lucerne", "Fodder"),
    ("Fodder Maize", "Fodder"),
    ("Fodder Sorghum", "Fodder"),
    ("Napier Grass", "Fodder"),

    # Other
    ("Medicinal Crops", "Other"),
    ("Aromatic Crops", "Other"),
    ("Floriculture Crops", "Other"),
]


conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS crops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    category TEXT
)
""")

for name, category in crops:
    cursor.execute("""
        INSERT OR IGNORE INTO crops (name, category)
        VALUES (?, ?)
    """, (name, category))

conn.commit()

count = cursor.execute(
    "SELECT COUNT(*) FROM crops"
).fetchone()[0]

conn.close()

print("=" * 40)
print("CROP DATABASE CREATED")
print("=" * 40)
print("Total crops:", count)
print("=" * 40)
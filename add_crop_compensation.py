import sqlite3

DATABASE = "agrivision.db"

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()


# ============================================================
# CROP CATEGORY RULES
# ============================================================

category_rules = {

    "Cereal": {
        "eligibility": "Eligibility depends on the notified crop, insured area, season and applicable government/insurance scheme conditions.",
        "coverage": "Coverage depends on the notified cereal crop, insured area, season, notified risks and applicable policy conditions.",
    },

    "Pulse": {
        "eligibility": "Eligibility depends on the notified pulse crop, insured area, season and applicable scheme conditions.",
        "coverage": "Coverage depends on the notified pulse crop, insured area, season and applicable policy conditions.",
    },

    "Oilseed": {
        "eligibility": "Eligibility depends on the notified oilseed crop, insured area, season and applicable scheme conditions.",
        "coverage": "Coverage depends on the notified oilseed crop, insured area, season and applicable policy conditions.",
    },

    "Vegetable": {
        "eligibility": "Eligibility depends on crop notification, location, season and applicable insurance or compensation conditions.",
        "coverage": "Coverage depends on whether the vegetable crop and affected area are covered under the applicable scheme.",
    },

    "Fruit": {
        "eligibility": "Eligibility depends on the notified fruit crop, location, season and applicable scheme conditions.",
        "coverage": "Coverage depends on the notified fruit crop, affected area, season and applicable insurance conditions.",
    },

    "Commercial": {
        "eligibility": "Eligibility depends on the notified commercial crop and applicable government or insurance scheme.",
        "coverage": "Coverage depends on the notified commercial crop, season, insured area and policy conditions.",
    },

    "Spice": {
        "eligibility": "Eligibility depends on the notified spice crop, location, season and applicable scheme.",
        "coverage": "Coverage depends on the notified spice crop and applicable insurance or compensation provisions.",
    },

    "Fibre": {
        "eligibility": "Eligibility depends on the notified fibre crop and applicable government scheme.",
        "coverage": "Coverage depends on crop notification, insured area, season and applicable policy.",
    },

    "Fodder": {
        "eligibility": "Eligibility depends on local notification and applicable agricultural compensation provisions.",
        "coverage": "Coverage depends on the applicable government notification and crop-loss programme.",
    },

    "Other": {
        "eligibility": "Eligibility depends on the applicable government notification and scheme conditions.",
        "coverage": "Coverage depends on crop notification, location, season and applicable provisions.",
    }
}


# ============================================================
# DAMAGE RULES
# ============================================================

damage_rules = {

    1: (
        "Flood",
        "Flood or inundation damage may be covered where the crop and area are notified under the applicable scheme.",
        "Report the affected field promptly and provide supporting evidence."
    ),

    2: (
        "Drought",
        "Drought-related loss depends on the notified area, crop, season and applicable scheme.",
        "Loss assessment may depend on official crop-yield assessment."
    ),

    3: (
        "Hailstorm",
        "Hailstorm damage may be covered where the crop and risk are notified.",
        "Photographs and timely reporting can assist official assessment."
    ),

    4: (
        "Cyclone / Storm",
        "Storm or cyclone damage may be covered subject to applicable notified risks.",
        "Report damage promptly and preserve evidence."
    ),

    5: (
        "Fire / Lightning",
        "Fire or lightning damage may be considered where the applicable scheme provides coverage.",
        "Provide incident details and supporting evidence."
    ),

    6: (
        "Pest Attack",
        "Pest-related loss is considered only where covered under the applicable scheme.",
        "Official assessment may be required to establish the cause and extent of damage."
    ),

    7: (
        "Crop Disease",
        "Disease-related crop loss depends on the applicable notified risks and scheme conditions.",
        "Keep photographs and evidence and report the damage."
    ),

    8: (
        "Prevented Sowing",
        "Prevented-sowing claims are subject to notified crop, area, season and scheme provisions.",
        "Report the situation according to the applicable claim procedure."
    ),

    9: (
        "Post-Harvest Loss",
        "Post-harvest losses may be covered for applicable crops and specified circumstances.",
        "Report the loss within the applicable reporting period."
    ),

    10: (
        "Localized Calamity",
        "Localized calamity coverage depends on the notified crop, area and applicable provisions.",
        "Report the localized loss for official assessment."
    )
}


# ============================================================
# GET CROPS
# ============================================================

crops = cursor.execute("""
    SELECT id, name, category
    FROM crops
    ORDER BY id
""").fetchall()


# ============================================================
# GET STATES
# ============================================================

states = cursor.execute("""
    SELECT id, name
    FROM states
    ORDER BY id
""").fetchall()


# ============================================================
# GET DISTRICTS
# ============================================================

districts = cursor.execute("""
    SELECT id, name, state_id
    FROM districts
    ORDER BY id
""").fetchall()


# ============================================================
# GET SCHEME
# ============================================================

scheme = cursor.execute("""
    SELECT id, name
    FROM schemes
    ORDER BY id
    LIMIT 1
""").fetchone()


if not scheme:
    print("ERROR: No scheme exists in the schemes table.")
    conn.close()
    exit()


scheme_id = scheme[0]
scheme_name = scheme[1]


print("=" * 60)
print("ADDING CROP-SPECIFIC COMPENSATION RECORDS")
print("=" * 60)

print("Crops:", len(crops))
print("States:", len(states))
print("Districts:", len(districts))
print("Scheme:", scheme_name)


inserted = 0
skipped = 0


# ============================================================
# CREATE CROP + STATE + DISTRICT + DAMAGE RECORDS
# ============================================================

for crop_id, crop_name, category in crops:

    category_data = category_rules.get(
        category,
        category_rules["Other"]
    )

    for state_id, state_name in states:

        # ----------------------------------------------------
        # Find districts belonging to this state
        # ----------------------------------------------------

        state_districts = [
            d for d in districts
            if d[2] == state_id
        ]

        # If a state has no district, skip it
        if not state_districts:
            continue

        for district_id, district_name, _ in state_districts:

            for damage_type_id, damage_data in damage_rules.items():

                damage_name = damage_data[0]
                damage_description = damage_data[1]
                claim_advice = damage_data[2]


                # ------------------------------------------------
                # CHECK EXISTING RECORD
                # ------------------------------------------------

                existing = cursor.execute("""
                    SELECT id
                    FROM compensation
                    WHERE state_id = ?
                    AND district_id = ?
                    AND damage_type_id = ?
                    AND crop_id = ?
                """, (
                    state_id,
                    district_id,
                    damage_type_id,
                    crop_id
                )).fetchone()


                if existing:

                    skipped += 1
                    continue


                # ------------------------------------------------
                # CREATE CROP-SPECIFIC INFORMATION
                # ------------------------------------------------

                eligibility = (
                    f"{crop_name} ({category}) in "
                    f"{district_name}, {state_name}. "
                    f"{category_data['eligibility']}"
                )


                coverage = (
                    f"{crop_name} - {damage_name}. "
                    f"{damage_description} "
                    f"{category_data['coverage']}"
                )


                claim_process = (
                    f"{claim_advice} "
                    f"Farmer should follow the applicable official "
                    f"claim reporting and assessment procedure."
                )


                source = (
                    "Agrivision crop-specific compensation database. "
                    "Verify the latest State/Season notification, "
                    "insurance policy and official government guidance."
                )


                # ------------------------------------------------
                # INSERT
                # ------------------------------------------------

                cursor.execute("""
                    INSERT INTO compensation (
                        state_id,
                        district_id,
                        damage_type_id,
                        scheme_id,
                        eligibility,
                        coverage,
                        claim_process,
                        source,
                        crop_id
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    state_id,
                    district_id,
                    damage_type_id,
                    scheme_id,
                    eligibility,
                    coverage,
                    claim_process,
                    source,
                    crop_id
                ))


                inserted += 1


                if inserted % 1000 == 0:

                    print(
                        "Records inserted:",
                        inserted
                    )


# ============================================================
# SAVE
# ============================================================

conn.commit()


# ============================================================
# FINAL COUNT
# ============================================================

total_records = cursor.execute("""
    SELECT COUNT(*)
    FROM compensation
    WHERE crop_id IS NOT NULL
""").fetchone()[0]


conn.close()


print()
print("=" * 60)
print("CROP COMPENSATION DATABASE UPDATED")
print("=" * 60)

print("Total crops:", len(crops))
print("New records inserted:", inserted)
print("Already existed:", skipped)
print("Crop-specific records:", total_records)

print("=" * 60)
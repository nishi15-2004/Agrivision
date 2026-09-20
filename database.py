import sqlite3
import csv
import os

DB_NAME = "agrivision.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# =========================================================
# CREATE DATABASE TABLES
# =========================================================

def create_database():

    conn = get_connection()
    cursor = conn.cursor()

    # STATES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS states (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    # DISTRICTS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS districts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            state_id INTEGER NOT NULL,
            name TEXT NOT NULL,

            UNIQUE(state_id, name),

            FOREIGN KEY(state_id)
            REFERENCES states(id)
        )
    """)

    # DAMAGE TYPES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS damage_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT
        )
    """)

    # GOVERNMENT SCHEMES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schemes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            official_url TEXT
        )
    """)

    # COMPENSATION / SCHEME MAPPING
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS compensation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            state_id INTEGER NOT NULL,
            district_id INTEGER,

            damage_type_id INTEGER NOT NULL,
            scheme_id INTEGER NOT NULL,

            eligibility TEXT,
            coverage TEXT,
            claim_process TEXT,
            source TEXT,

            FOREIGN KEY(state_id)
            REFERENCES states(id),

            FOREIGN KEY(district_id)
            REFERENCES districts(id),

            FOREIGN KEY(damage_type_id)
            REFERENCES damage_types(id),

            FOREIGN KEY(scheme_id)
            REFERENCES schemes(id)
        )
    """)

    # =====================================================
    # 36 STATES / UNION TERRITORIES
    # =====================================================

    states = [
        "Andhra Pradesh",
        "Arunachal Pradesh",
        "Assam",
        "Bihar",
        "Chhattisgarh",
        "Goa",
        "Gujarat",
        "Haryana",
        "Himachal Pradesh",
        "Jharkhand",
        "Karnataka",
        "Kerala",
        "Madhya Pradesh",
        "Maharashtra",
        "Manipur",
        "Meghalaya",
        "Mizoram",
        "Nagaland",
        "Odisha",
        "Punjab",
        "Rajasthan",
        "Sikkim",
        "Tamil Nadu",
        "Telangana",
        "Tripura",
        "Uttar Pradesh",
        "Uttarakhand",
        "West Bengal",

        "Andaman and Nicobar Islands",
        "Chandigarh",
        "Dadra and Nagar Haveli and Daman and Diu",
        "Delhi",
        "Jammu and Kashmir",
        "Ladakh",
        "Lakshadweep",
        "Puducherry"
    ]

    for state in states:

        cursor.execute(
            """
            INSERT OR IGNORE INTO states(name)
            VALUES(?)
            """,
            (state,)
        )

    # =====================================================
    # DAMAGE TYPES
    # =====================================================

    damage_types = [

        (
            "Flood",
            "Crop damage caused by flooding or excessive water."
        ),

        (
            "Drought",
            "Crop loss caused by drought or prolonged moisture deficiency."
        ),

        (
            "Hailstorm",
            "Crop damage caused by hailstorm."
        ),

        (
            "Cyclone / Storm",
            "Crop damage caused by cyclone, storm or strong winds."
        ),

        (
            "Fire / Lightning",
            "Eligible crop damage caused by natural fire or lightning, subject to applicable conditions."
        ),

        (
            "Pest Attack",
            "Crop damage caused by notified pests where applicable."
        ),

        (
            "Crop Disease",
            "Crop loss caused by notified crop diseases where covered."
        ),

        (
            "Prevented Sowing",
            "Loss where sowing or planting could not take place because of notified adverse conditions."
        ),

        (
            "Post-Harvest Loss",
            "Eligible crop loss occurring during the specified post-harvest period."
        ),

        (
            "Localized Calamity",
            "Localized crop damage subject to applicable rules."
        )
    ]

    for name, description in damage_types:

        cursor.execute(
            """
            INSERT OR IGNORE INTO damage_types
            (name, description)
            VALUES (?, ?)
            """,
            (name, description)
        )

    # =====================================================
    # PMFBY
    # =====================================================

    cursor.execute(
        """
        INSERT OR IGNORE INTO schemes
        (name, description, official_url)

        VALUES (?, ?, ?)
        """,
        (
            "Pradhan Mantri Fasal Bima Yojana (PMFBY)",

            "Government crop insurance scheme providing insurance protection for notified crops and areas subject to applicable conditions.",

            "https://pmfby.gov.in/"
        )
    )

    conn.commit()
    conn.close()

    print()
    print("===================================")
    print("   AGRIVISION DATABASE CREATED")
    print("===================================")
    print("States / UTs:", len(states))
    print("Damage Types:", len(damage_types))
    print("Database:", DB_NAME)
    print("===================================")


# =========================================================
# IMPORT ALL INDIA DISTRICTS
# =========================================================

def import_districts_from_csv(csv_file):

    if not os.path.exists(csv_file):

        print()
        print("ERROR: District CSV file not found.")
        print("Expected file:", csv_file)
        print()
        return

    conn = get_connection()
    cursor = conn.cursor()

    added = 0
    skipped = 0

    with open(
        csv_file,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        print()
        print("CSV COLUMNS:")
        print(reader.fieldnames)

        for row in reader:

            # -------------------------------------------------
            # Try common LGD column names
            # -------------------------------------------------

            state_name = (
                row.get("stateNameEnglish")
                or row.get("State Name")
                or row.get("state_name")
                or row.get("State")
                or ""
            ).strip()

            district_name = (
                row.get("districtNameEnglish")
                or row.get("District Name")
                or row.get("district_name")
                or row.get("District")
                or ""
            ).strip()

            if not state_name or not district_name:
                skipped += 1
                continue

            # -------------------------------------------------
            # Find state
            # -------------------------------------------------

            state = cursor.execute(
                """
                SELECT id
                FROM states
                WHERE LOWER(name) = LOWER(?)
                """,
                (state_name,)
            ).fetchone()

            if not state:

                skipped += 1
                continue

            state_id = state["id"]

            # -------------------------------------------------
            # Add district
            # -------------------------------------------------

            cursor.execute(
                """
                INSERT OR IGNORE INTO districts
                (state_id, name)

                VALUES (?, ?)
                """,
                (state_id, district_name)
            )

            if cursor.rowcount > 0:
                added += 1
            else:
                skipped += 1

    conn.commit()

    total = cursor.execute(
        "SELECT COUNT(*) FROM districts"
    ).fetchone()[0]

    conn.close()

    print()
    print("===================================")
    print("   ALL INDIA DISTRICTS IMPORTED")
    print("===================================")
    print("New districts:", added)
    print("Skipped:", skipped)
    print("Total districts:", total)
    print("===================================")


# =========================================================
# ADD PMFBY GENERAL COMPENSATION INFORMATION
# =========================================================

def add_compensation_information():

    conn = get_connection()
    cursor = conn.cursor()

    # -----------------------------------------------------
    # Get PMFBY scheme
    # -----------------------------------------------------

    scheme = cursor.execute(
        """
        SELECT id
        FROM schemes
        WHERE name = ?
        """,
        ("Pradhan Mantri Fasal Bima Yojana (PMFBY)",)
    ).fetchone()

    if not scheme:
        conn.close()
        return

    scheme_id = scheme["id"]

    # -----------------------------------------------------
    # General PMFBY information
    # -----------------------------------------------------

    information = {

        "Flood": (
            "Coverage applies to notified crops and areas subject to PMFBY conditions.",
            "Flood, inundation and related notified risks may be covered under applicable PMFBY provisions.",
            "Farmer should report the loss through the prescribed reporting channel within the applicable time limit and follow assessment requirements.",
            "PMFBY Official Portal"
        ),

        "Drought": (
            "Coverage applies to notified crops and areas subject to PMFBY conditions.",
            "Drought and dry-spell related yield losses may be covered under applicable PMFBY provisions.",
            "Loss reporting and claim assessment are carried out according to applicable PMFBY and State notification procedures.",
            "PMFBY Official Portal"
        ),

        "Hailstorm": (
            "Coverage applies where the crop, area and peril are notified under the applicable scheme.",
            "Hailstorm may be covered under yield-loss or localized calamity provisions depending on the circumstances.",
            "Loss should be reported promptly through the prescribed channel for assessment.",
            "PMFBY Official Portal"
        ),

        "Cyclone / Storm": (
            "Coverage applies to notified crops and areas subject to applicable conditions.",
            "Storm, cyclone and related notified risks may be covered.",
            "Farmer should report the occurrence and cooperate with the prescribed assessment process.",
            "PMFBY Official Portal"
        ),

        "Fire / Lightning": (
            "Coverage is subject to the applicable notified peril, crop, area and insurance conditions.",
            "Natural fire due to lightning may be covered under applicable PMFBY provisions.",
            "Loss should be reported through the prescribed channel and supported by the required assessment/reporting information.",
            "PMFBY Official Portal"
        ),

        "Pest Attack": (
            "Coverage is available only where the relevant crop, area and pest/disease risk is covered under the applicable notification.",
            "Notified pest-related crop losses may be covered under applicable PMFBY provisions.",
            "Claim assessment follows the applicable crop insurance notification and assessment process.",
            "PMFBY Official Portal"
        ),

        "Crop Disease": (
            "Coverage depends on the notified crop, area and applicable insurance conditions.",
            "Notified pest and disease related losses may be covered where applicable.",
            "Farmer should follow the applicable State and insurance company reporting procedure.",
            "PMFBY Official Portal"
        ),

        "Prevented Sowing": (
            "Applicable to eligible insured farmers in notified areas where sowing/planting is prevented due to specified adverse conditions.",
            "Indemnity may be available subject to PMFBY conditions and the applicable notified area.",
            "Eligibility and claim processing are determined according to the applicable notification and scheme procedure.",
            "PMFBY Official Portal"
        ),

        "Post-Harvest Loss": (
            "Available to eligible insured farmers and notified crops subject to applicable conditions.",
            "Specified post-harvest losses may be covered for eligible crops kept in the field for drying for the prescribed period.",
            "Loss should be reported promptly according to the prescribed procedure.",
            "PMFBY Official Portal"
        ),

        "Localized Calamity": (
            "Applicable to eligible insured farmers where the localized calamity is a notified covered peril.",
            "Identified localized risks such as hailstorm, landslide and inundation may be covered subject to applicable conditions.",
            "Individual farm loss assessment is carried out according to the applicable procedure.",
            "PMFBY Official Portal"
        )
    }

    # -----------------------------------------------------
    # Add information for every state
    # -----------------------------------------------------

    states = cursor.execute(
        "SELECT id FROM states"
    ).fetchall()

    damage_types = cursor.execute(
        "SELECT id, name FROM damage_types"
    ).fetchall()

    inserted = 0

    for state in states:

        state_id = state["id"]

        for damage in damage_types:

            damage_id = damage["id"]
            damage_name = damage["name"]

            if damage_name not in information:
                continue

            eligibility, coverage, claim_process, source = \
                information[damage_name]

            # Avoid duplicate records
            existing = cursor.execute(
                """
                SELECT id
                FROM compensation
                WHERE state_id = ?
                AND district_id IS NULL
                AND damage_type_id = ?
                AND scheme_id = ?
                """,
                (
                    state_id,
                    damage_id,
                    scheme_id
                )
            ).fetchone()

            if existing:
                continue

            cursor.execute(
                """
                INSERT INTO compensation
                (
                    state_id,
                    district_id,
                    damage_type_id,
                    scheme_id,
                    eligibility,
                    coverage,
                    claim_process,
                    source
                )

                VALUES (?, NULL, ?, ?, ?, ?, ?, ?)
                """,
                (
                    state_id,
                    damage_id,
                    scheme_id,
                    eligibility,
                    coverage,
                    claim_process,
                    source
                )
            )

            inserted += 1

    conn.commit()
    conn.close()

    print()
    print("===================================")
    print(" COMPENSATION INFORMATION ADDED")
    print("===================================")
    print("Records added:", inserted)
    print("===================================")


# =========================================================
# DATABASE SUMMARY
# =========================================================

def show_database_summary():

    conn = get_connection()
    cursor = conn.cursor()

    states = cursor.execute(
        "SELECT COUNT(*) FROM states"
    ).fetchone()[0]

    districts = cursor.execute(
        "SELECT COUNT(*) FROM districts"
    ).fetchone()[0]

    damage_types = cursor.execute(
        "SELECT COUNT(*) FROM damage_types"
    ).fetchone()[0]

    schemes = cursor.execute(
        "SELECT COUNT(*) FROM schemes"
    ).fetchone()[0]

    compensation = cursor.execute(
        "SELECT COUNT(*) FROM compensation"
    ).fetchone()[0]

    conn.close()

    print()
    print("===================================")
    print("       AGRIVISION DATABASE")
    print("===================================")
    print("States / UTs       :", states)
    print("Districts          :", districts)
    print("Damage Types       :", damage_types)
    print("Government Schemes :", schemes)
    print("Compensation Data  :", compensation)
    print("===================================")


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    create_database()

    # -----------------------------------------------------
    # IMPORTANT:
    # Put the official LGD district CSV in this folder
    # with this name:
    #
    # lgd_districts.csv
    # -----------------------------------------------------

    csv_file = "lgd_districts.csv"

    if os.path.exists(csv_file):

        import_districts_from_csv(csv_file)

    else:

        print()
        print("===================================")
        print("LGD DISTRICT CSV NOT FOUND")
        print("===================================")
        print("Create/download:")
        print("lgd_districts.csv")
        print()
        print("The database will NOT pretend that")
        print("84 districts are all-India coverage.")
        print("===================================")

    add_compensation_information()

    show_database_summary()
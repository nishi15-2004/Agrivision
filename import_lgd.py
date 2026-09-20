import sqlite3
import csv

DB_NAME = "agrivision.db"
CSV_FILE = "lgd_districts.csv"


def clean(value):
    if value is None:
        return ""
    return value.strip()


conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# State-name differences between our database and LGD dataset
state_name_map = {
    "Jammu And Kashmir": "Jammu and Kashmir",
    "Andaman And Nicobar Islands": "Andaman and Nicobar Islands",
    "Dadra And Nagar Haveli And Daman And Diu":
        "Dadra and Nagar Haveli and Daman and Diu",
    "The Dadra And Nagar Haveli And Daman And Diu":
        "Dadra and Nagar Haveli and Daman and Diu"
}

inserted = 0
skipped = 0

with open(CSV_FILE, "r", encoding="utf-8-sig", newline="") as file:

    reader = csv.DictReader(file)

    print("CSV columns:")
    print(reader.fieldnames)
    print()

    for row in reader:

        lgd_state = clean(row.get("state_name_english"))
        district = clean(row.get("district_name_english"))

        if not lgd_state or not district:
            skipped += 1
            continue

        state_name = state_name_map.get(
            lgd_state,
            lgd_state
        )

        # Find state already present in agrivision.db
        state = cursor.execute(
            """
            SELECT id
            FROM states
            WHERE LOWER(TRIM(name)) = LOWER(TRIM(?))
            """,
            (state_name,)
        ).fetchone()

        if not state:
            print("STATE NOT FOUND:", lgd_state)
            skipped += 1
            continue

        state_id = state[0]

        # Insert district
        cursor.execute(
            """
            INSERT OR IGNORE INTO districts
            (state_id, name)
            VALUES (?, ?)
            """,
            (state_id, district)
        )

        if cursor.rowcount > 0:
            inserted += 1


conn.commit()

# Final statistics
total_districts = cursor.execute(
    "SELECT COUNT(*) FROM districts"
).fetchone()[0]

total_states = cursor.execute(
    "SELECT COUNT(*) FROM states"
).fetchone()[0]

print()
print("===================================")
print("   LGD DISTRICT IMPORT COMPLETE")
print("===================================")
print("States:", total_states)
print("New districts inserted:", inserted)
print("Skipped:", skipped)
print("Total districts in database:", total_districts)
print("===================================")

conn.close()
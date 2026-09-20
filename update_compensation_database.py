import sqlite3

DATABASE = "agrivision.db"

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()


# ============================================================
# CHECK COMPENSATION TABLE
# ============================================================

cursor.execute("""
PRAGMA table_info(compensation)
""")

columns = [
    row[1]
    for row in cursor.fetchall()
]


# ============================================================
# ADD crop_id IF NOT EXISTS
# ============================================================

if "crop_id" not in columns:

    print("Adding crop_id column...")

    cursor.execute("""
        ALTER TABLE compensation
        ADD COLUMN crop_id INTEGER
    """)

    conn.commit()

    print("crop_id added successfully.")

else:

    print("crop_id already exists.")


# ============================================================
# CREATE INDEX
# ============================================================

cursor.execute("""
CREATE INDEX IF NOT EXISTS
idx_compensation_crop
ON compensation(crop_id)
""")


cursor.execute("""
CREATE INDEX IF NOT EXISTS
idx_compensation_lookup
ON compensation(
    state_id,
    district_id,
    crop_id,
    damage_type_id
)
""")


conn.commit()


print()
print("=" * 50)
print("COMPENSATION DATABASE STRUCTURE UPDATED")
print("=" * 50)


# Show columns
cursor.execute("""
PRAGMA table_info(compensation)
""")

for row in cursor.fetchall():

    print(
        row[1],
        " | ",
        row[2]
    )


conn.close()
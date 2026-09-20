import os
import shutil

# ==========================================
# PLANTVILLAGE ORGANIZER
# ==========================================

SOURCE_DIR = "plantvillage_data/raw/segmented"
DEST_DIR = "datasets/multicrop"

print("\n======================================")
print("   ORGANIZING PLANTVILLAGE DATASET")
print("======================================\n")

if not os.path.exists(SOURCE_DIR):
    print("ERROR: PlantVillage dataset folder not found!")
    print("Expected:", SOURCE_DIR)
    exit()

os.makedirs(DEST_DIR, exist_ok=True)

class_count = 0
image_count = 0

# Go through all disease/healthy folders
for class_name in sorted(os.listdir(SOURCE_DIR)):

    class_path = os.path.join(SOURCE_DIR, class_name)

    if not os.path.isdir(class_path):
        continue

    # PlantVillage format:
    # Crop___Disease
    if "___" not in class_name:
        print("Skipping:", class_name)
        continue

    crop, disease = class_name.split("___", 1)

    # Make folder names cleaner
    crop = crop.strip()
    disease = disease.replace("_", " ").strip()

    destination = os.path.join(
        DEST_DIR,
        crop,
        disease
    )

    os.makedirs(destination, exist_ok=True)

    class_count += 1

    print(f"\n[{class_count}] {crop} -> {disease}")

    for filename in os.listdir(class_path):

        source_file = os.path.join(
            class_path,
            filename
        )

        if not os.path.isfile(source_file):
            continue

        if not filename.lower().endswith(
            (".jpg", ".jpeg", ".png")
        ):
            continue

        destination_file = os.path.join(
            destination,
            filename
        )

        # Copy image
        shutil.copy2(
            source_file,
            destination_file
        )

        image_count += 1

print("\n======================================")
print("       ORGANIZATION COMPLETE")
print("======================================")

print("Total disease/healthy classes:", class_count)
print("Total images copied:", image_count)

print("\nData saved inside:")
print(DEST_DIR)

print("\n======================================")
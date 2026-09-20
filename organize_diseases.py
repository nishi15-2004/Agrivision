import os
import json

DATASET_DIR = "datasets/multicrop"
OUTPUT_FILE = "crop_disease_classes.json"

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".bmp")

print("\n======================================")
print("   AGRIMITRA DISEASE CLASS MAPPER")
print("======================================\n")

if not os.path.exists(DATASET_DIR):
    print("ERROR: datasets/multicrop folder nahi mila!")
    exit()

result = {}
total_images = 0
total_classes = 0

for crop in sorted(os.listdir(DATASET_DIR)):

    crop_path = os.path.join(DATASET_DIR, crop)

    if not os.path.isdir(crop_path):
        continue

    images = []

    for root, dirs, files in os.walk(crop_path):
        for file in files:
            if file.lower().endswith(IMAGE_EXTENSIONS):
                images.append(os.path.join(root, file))

    if len(images) == 0:
        continue

    # Disease folders ke naam
    classes = []

    # Agar crop ke andar subfolders hain
    subfolders = [
        folder
        for folder in os.listdir(crop_path)
        if os.path.isdir(os.path.join(crop_path, folder))
    ]

    if subfolders:

        for disease in sorted(subfolders):

            disease_path = os.path.join(crop_path, disease)

            disease_images = []

            for root, dirs, files in os.walk(disease_path):
                for file in files:
                    if file.lower().endswith(IMAGE_EXTENSIONS):
                        disease_images.append(file)

            if disease_images:
                classes.append({
                    "disease": disease,
                    "images": len(disease_images)
                })

                total_classes += 1
                total_images += len(disease_images)

    else:
        # Agar images directly crop folder ke andar hain
        classes.append({
            "disease": "Unknown",
            "images": len(images)
        })

        total_images += len(images)
        total_classes += 1

    result[crop] = {
        "total_images": len(images),
        "classes": classes
    }

# JSON save
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=4, ensure_ascii=False)

print("======================================")
print("         MAPPING COMPLETE")
print("======================================")

print("Crops with images :", len(result))
print("Disease classes   :", total_classes)
print("Total images      :", total_images)

print("\nSaved as:")
print(OUTPUT_FILE)

print("\n======================================")
import os

DATASET_DIR = "plantvillage_data"

print("\n===================================")
print("PLANTVILLAGE DATASET INSPECTION")
print("===================================\n")

found = []

for root, dirs, files in os.walk(DATASET_DIR):

    image_files = [
        f for f in files
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    if image_files:
        found.append(
            (root, len(image_files))
        )

print("Image-containing folders found:")
print("-----------------------------------")

for folder, count in found:
    print(f"{folder}  -->  {count} images")

print("\n===================================")
print("TOTAL IMAGE FOLDERS:", len(found))
print("===================================")
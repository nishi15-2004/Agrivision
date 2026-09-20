import os

DATASET_DIR = "datasets/multicrop"

print("\n======================================")
print("       AGRIMITRA DATASET REPORT")
print("======================================\n")

if not os.path.exists(DATASET_DIR):
    print("ERROR: datasets/multicrop folder nahi mila!")
    exit()

crop_folders = sorted(
    [
        folder
        for folder in os.listdir(DATASET_DIR)
        if os.path.isdir(os.path.join(DATASET_DIR, folder))
    ]
)

print("Total crop folders:", len(crop_folders))
print()

total_images = 0
non_empty = 0
empty = 0

print("--------------- DATASET STATUS ---------------")

for crop in crop_folders:

    crop_path = os.path.join(DATASET_DIR, crop)

    image_count = 0

    for root, dirs, files in os.walk(crop_path):
        for file in files:

            if file.lower().endswith(
                (".jpg", ".jpeg", ".png", ".webp", ".bmp")
            ):
                image_count += 1

    total_images += image_count

    if image_count > 0:
        non_empty += 1
        print(f"✓ {crop:<30} {image_count:>6} images")

    else:
        empty += 1
        print(f"✗ {crop:<30} EMPTY")


print("\n======================================")
print("              SUMMARY")
print("======================================")

print("Total crop folders :", len(crop_folders))
print("Folders with images:", non_empty)
print("Empty folders      :", empty)
print("Total images       :", total_images)

print("\n======================================")
print("             REPORT COMPLETE")
print("======================================")
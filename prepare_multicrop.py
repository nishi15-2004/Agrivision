import os
import shutil

SOURCE = "datasets/multicrop"
DEST = "datasets/multicrop_clean"

VALID_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp",
    ".tif",
    ".tiff"
)

print("======================================")
print("   AGRIMITRA DATASET PREPARATION")
print("======================================")

print("Source:", SOURCE)
print("Destination:", DEST)

if not os.path.exists(SOURCE):
    print("ERROR: Dataset folder not found!")
    exit()

# Create destination
os.makedirs(DEST, exist_ok=True)

total_images = 0
total_classes = 0
total_crops = 0

print("\nScanning dataset...")

for crop in sorted(os.listdir(SOURCE)):

    crop_path = os.path.join(SOURCE, crop)

    if not os.path.isdir(crop_path):
        continue

    crop_has_images = False

    for disease in sorted(os.listdir(crop_path)):

        disease_path = os.path.join(
            crop_path,
            disease
        )

        if not os.path.isdir(disease_path):
            continue

        images = []

        for filename in os.listdir(disease_path):

            file_path = os.path.join(
                disease_path,
                filename
            )

            if (
                os.path.isfile(file_path)
                and filename.lower().endswith(
                    VALID_EXTENSIONS
                )
            ):
                images.append(filename)

        # Ignore empty folders
        if len(images) == 0:
            continue

        crop_has_images = True

        # Normalize class name
        clean_crop = crop.strip()
        clean_disease = disease.strip()

        # Make one combined class
        class_name = (
            clean_crop
            + "___"
            + clean_disease
        )

        class_path = os.path.join(
            DEST,
            class_name
        )

        os.makedirs(
            class_path,
            exist_ok=True
        )

        for filename in images:

            source_file = os.path.join(
                disease_path,
                filename
            )

            destination_file = os.path.join(
                class_path,
                filename
            )

            # Avoid duplicate filename
            if os.path.exists(destination_file):

                base, ext = os.path.splitext(
                    filename
                )

                counter = 1

                while os.path.exists(
                    destination_file
                ):

                    new_name = (
                        base
                        + "_"
                        + str(counter)
                        + ext
                    )

                    destination_file = os.path.join(
                        class_path,
                        new_name
                    )

                    counter += 1

            shutil.copy2(
                source_file,
                destination_file
            )

        total_classes += 1
        total_images += len(images)

        print(
            "Copied:",
            class_name,
            "->",
            len(images),
            "images"
        )

    if crop_has_images:
        total_crops += 1


print("\n======================================")
print("       PREPARATION COMPLETE")
print("======================================")

print("Crops with images:", total_crops)
print("Training classes:", total_classes)
print("Total images:", total_images)

print("Clean dataset:")
print(DEST)

print("======================================")
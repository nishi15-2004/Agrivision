import os
import shutil


# ==========================
# WHEAT DATASET LOCATION
# ==========================

SOURCE_FOLDER = "datasets/wheat"


# ==========================
# DISEASE FOLDERS
# ==========================

folders = [
    "BrownRust",
    "YellowRust",
    "Septoria",
    "Mildew",
    "Healthy"
]


# ==========================
# CREATE FOLDERS
# ==========================

for folder in folders:

    folder_path = os.path.join(
        SOURCE_FOLDER,
        folder
    )

    os.makedirs(
        folder_path,
        exist_ok=True
    )


# ==========================
# SORT IMAGES
# ==========================

for filename in os.listdir(SOURCE_FOLDER):

    file_path = os.path.join(
        SOURCE_FOLDER,
        filename
    )


    # Ignore folders
    if os.path.isdir(file_path):
        continue


    name = filename.lower()


    if name.startswith("brownrust"):

        destination = "BrownRust"


    elif name.startswith("yellowrust"):

        destination = "YellowRust"


    elif name.startswith("septoria"):

        destination = "Septoria"


    elif name.startswith("mildew"):

        destination = "Mildew"


    elif name.startswith("healthy"):

        destination = "Healthy"


    else:

        print("Skipped:", filename)

        continue


    destination_path = os.path.join(

        SOURCE_FOLDER,

        destination,

        filename

    )


    shutil.move(
        file_path,
        destination_path
    )


    print(
        "Moved:",
        filename,
        "→",
        destination
    )


print("\n================================")
print("✅ Wheat dataset organized!")
print("================================")
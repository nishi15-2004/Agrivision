import os
import json
import time

import torch
import torch.nn as nn
import torch.optim as optim

from PIL import Image
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision import transforms, models


# =========================================================
# AGRIMITRA MULTICROP DISEASE TRAINING
# =========================================================

DATASET_DIR = "datasets/multicrop"
MODEL_DIR = "models"

IMAGE_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 1
LEARNING_RATE = 0.0001

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


print("\n======================================")
print("     AGRIMITRA MULTICROP TRAINING")
print("======================================")
print("Device:", DEVICE)


# =========================================================
# IMAGE TRANSFORMS
# =========================================================

transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ToTensor()
])


# =========================================================
# CUSTOM DATASET
# Structure:
#
# datasets/multicrop/
#     Apple/
#         Apple scab/
#             image1.jpg
#         Black rot/
#             image2.jpg
#         Healthy/
#             image3.jpg
#
#     Wheat/
#         Healthy/
#             image.jpg
# =========================================================

class MultiCropDataset(Dataset):

    def __init__(self, root_dir, transform=None):

        self.root_dir = root_dir
        self.transform = transform

        self.samples = []
        self.classes = []

        print("\nScanning dataset...")

        for crop in sorted(os.listdir(root_dir)):

            crop_path = os.path.join(
                root_dir,
                crop
            )

            if not os.path.isdir(crop_path):
                continue

            for disease in sorted(os.listdir(crop_path)):

                disease_path = os.path.join(
                    crop_path,
                    disease
                )

                if not os.path.isdir(disease_path):
                    continue

                class_name = crop + "___" + disease

                class_index = len(self.classes)

                self.classes.append(class_name)

                for filename in os.listdir(disease_path):

                    file_path = os.path.join(
                        disease_path,
                        filename
                    )

                    if not os.path.isfile(file_path):
                        continue

                    if filename.lower().endswith(
                        (
                            ".jpg",
                            ".jpeg",
                            ".png",
                            ".bmp",
                            ".webp",
                            ".tif",
                            ".tiff"
                        )
                    ):

                        self.samples.append(
                            (
                                file_path,
                                class_index
                            )
                        )

        print("\nDataset scanning complete!")

        print(
            "Total images:",
            len(self.samples)
        )

        print(
            "Total classes:",
            len(self.classes)
        )


    def __len__(self):

        return len(self.samples)


    def __getitem__(self, index):

        image_path, label = self.samples[index]

        try:

            image = Image.open(
                image_path
            ).convert("RGB")

        except Exception as e:

            print(
                "\nError loading:",
                image_path
            )

            raise e

        if self.transform:

            image = self.transform(image)

        return image, label


# =========================================================
# LOAD DATASET
# =========================================================

print("\nLoading dataset...")

dataset = MultiCropDataset(
    DATASET_DIR,
    transform=transform
)


# =========================================================
# DATASET INFORMATION
# =========================================================

print("\n======================================")
print("       DATASET INFORMATION")
print("======================================")

print(
    "Total images:",
    len(dataset)
)

print(
    "Total classes:",
    len(dataset.classes)
)


print("\nFirst 20 classes:")

for i, class_name in enumerate(
    dataset.classes[:20]
):

    print(
        i,
        "->",
        class_name
    )


# =========================================================
# TRAIN / VALIDATION SPLIT
# =========================================================

train_size = int(
    0.8 * len(dataset)
)

val_size = (
    len(dataset)
    - train_size
)


train_dataset, val_dataset = random_split(
    dataset,
    [
        train_size,
        val_size
    ],
    generator=torch.Generator().manual_seed(42)
)


print("\nTraining images:", len(train_dataset))

print(
    "Validation images:",
    len(val_dataset)
)


# =========================================================
# DATA LOADERS
# =========================================================

train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    num_workers=0
)

val_loader = DataLoader(
    val_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=0
)


print(
    "Training batches:",
    len(train_loader)
)

print(
    "Validation batches:",
    len(val_loader)
)


# =========================================================
# CREATE RESNET18 MODEL
# =========================================================

print("\nCreating ResNet18 model...")

model = models.resnet18(
    weights=None
)


model.fc = nn.Linear(
    model.fc.in_features,
    len(dataset.classes)
)


model = model.to(DEVICE)


# =========================================================
# LOSS + OPTIMIZER
# =========================================================

criterion = nn.CrossEntropyLoss()


optimizer = optim.Adam(
    model.parameters(),
    lr=LEARNING_RATE
)


# =========================================================
# TRAINING
# =========================================================

print("\n======================================")
print("          TRAINING STARTED")
print("======================================")


for epoch in range(EPOCHS):

    print("\n--------------------------------------")

    print(
        f"Epoch {epoch + 1}/{EPOCHS}"
    )

    print("--------------------------------------")


    model.train()


    running_loss = 0.0

    correct = 0

    total = 0


    start_time = time.time()


    for batch_index, (
        images,
        labels
    ) in enumerate(train_loader):


        images = images.to(DEVICE)

        labels = labels.to(DEVICE)


        optimizer.zero_grad()


        outputs = model(images)


        loss = criterion(
            outputs,
            labels
        )


        loss.backward()


        optimizer.step()


        running_loss += loss.item()


        _, predicted = torch.max(
            outputs,
            1
        )


        total += labels.size(0)


        correct += (
            predicted == labels
        ).sum().item()


        if batch_index % 25 == 0:

            accuracy = (
                100 * correct / total
            )


            print(
                f"Batch "
                f"{batch_index + 1}/"
                f"{len(train_loader)} "
                f"| Loss: "
                f"{loss.item():.4f} "
                f"| Accuracy: "
                f"{accuracy:.2f}%"
            )


    epoch_loss = (
        running_loss
        / len(train_loader)
    )


    epoch_accuracy = (
        100 * correct / total
    )


    print("\nEpoch completed!")


    print(
        "Average Loss:",
        round(epoch_loss, 4)
    )


    print(
        "Training Accuracy:",
        round(epoch_accuracy, 2),
        "%"
    )


    print(
        "Time:",
        round(
            (time.time() - start_time) / 60,
            2
        ),
        "minutes"
    )


# =========================================================
# VALIDATION
# =========================================================

print("\n======================================")
print("             VALIDATION")
print("======================================")


model.eval()


correct = 0

total = 0


with torch.no_grad():

    for images, labels in val_loader:

        images = images.to(DEVICE)

        labels = labels.to(DEVICE)


        outputs = model(images)


        _, predicted = torch.max(
            outputs,
            1
        )


        total += labels.size(0)


        correct += (
            predicted == labels
        ).sum().item()


validation_accuracy = (
    100 * correct / total
)


print(
    "\nValidation Accuracy:",
    round(
        validation_accuracy,
        2
    ),
    "%"
)


# =========================================================
# SAVE MODEL
# =========================================================

if not os.path.exists(MODEL_DIR):

    os.makedirs(MODEL_DIR)


model_path = os.path.join(
    MODEL_DIR,
    "multicrop_model.pth"
)


torch.save(
    {
        "model_state":
            model.state_dict(),

        "classes":
            dataset.classes
    },
    model_path
)


# =========================================================
# SAVE CLASS NAMES
# =========================================================

classes_path = (
    "multicrop_classes.json"
)


with open(
    classes_path,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        dataset.classes,
        file,
        indent=4,
        ensure_ascii=False
    )


# =========================================================
# COMPLETE
# =========================================================

print("\n======================================")
print("       TRAINING COMPLETE")
print("======================================")


print(
    "Model saved at:",
    model_path
)


print(
    "Classes saved at:",
    classes_path
)


print(
    "Total classes:",
    len(dataset.classes)
)


print("======================================")
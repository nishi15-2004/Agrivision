import os
import time
import random
import torch
import torch.nn as nn

from PIL import Image
from torch.utils.data import Dataset, DataLoader, WeightedRandomSampler
from torchvision import transforms, models


# ============================================================
# AGRIMITRA — 14 CROPS + WHEAT
# ============================================================

BASE_DATASET = "datasets/multicrop_clean"
WHEAT_DATASET = "datasets/wheat"

OLD_MODEL = "models/multicrop_model_best.pth"

NEW_MODEL = "models/multicrop_wheat_best.pth"

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


print("======================================")
print(" AGRIMITRA 14 CROPS + WHEAT")
print("======================================")
print("Device:", DEVICE)


# ============================================================
# TRANSFORMS
# ============================================================

train_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(
        brightness=0.2,
        contrast=0.2,
        saturation=0.2
    ),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    )
])


val_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    )
])


# ============================================================
# COLLECT DATA
# ============================================================

samples = []
class_names = []


# Existing 14-crop dataset
for class_folder in sorted(os.listdir(BASE_DATASET)):

    class_path = os.path.join(
        BASE_DATASET,
        class_folder
    )

    if not os.path.isdir(class_path):
        continue

    class_names.append(class_folder)

    for filename in os.listdir(class_path):

        file_path = os.path.join(
            class_path,
            filename
        )

        if (
            os.path.isfile(file_path)
            and filename.lower().endswith(
                (".jpg", ".jpeg", ".png", ".webp", ".bmp")
            )
        ):
            samples.append(
                (file_path, class_folder)
            )


# ============================================================
# WHEAT
# ============================================================

wheat_mapping = {
    "BrownRust": "Wheat___BrownRust",
    "Healthy": "Wheat___Healthy",
    "Mildew": "Wheat___Mildew",
    "Septoria": "Wheat___Septoria",
    "YellowRust": "Wheat___YellowRust"
}


for folder, class_name in wheat_mapping.items():

    folder_path = os.path.join(
        WHEAT_DATASET,
        folder
    )

    if not os.path.isdir(folder_path):
        continue

    class_names.append(class_name)

    for filename in os.listdir(folder_path):

        file_path = os.path.join(
            folder_path,
            filename
        )

        if (
            os.path.isfile(file_path)
            and filename.lower().endswith(
                (".jpg", ".jpeg", ".png", ".webp", ".bmp")
            )
        ):
            samples.append(
                (file_path, class_name)
            )


class_names = sorted(set(class_names))

class_to_index = {
    name: i
    for i, name in enumerate(class_names)
}


print()
print("Total classes:", len(class_names))
print("Total images:", len(samples))


print()
print("WHEAT DATA:")

for name in class_names:

    if name.startswith("Wheat___"):

        count = sum(
            1
            for _, label in samples
            if label == name
        )

        print(
            name,
            "->",
            count,
            "images"
        )


# ============================================================
# DATASET CLASS
# ============================================================

class CropDataset(Dataset):

    def __init__(
        self,
        samples,
        class_to_index,
        transform
    ):

        self.samples = samples
        self.class_to_index = class_to_index
        self.transform = transform

    def __len__(self):

        return len(self.samples)

    def __getitem__(self, index):

        path, class_name = self.samples[index]

        image = Image.open(
            path
        ).convert("RGB")

        image = self.transform(image)

        label = self.class_to_index[
            class_name
        ]

        return image, label


# ============================================================
# TRAIN / VALIDATION SPLIT
# ============================================================

random.seed(42)

random.shuffle(samples)

split = int(
    len(samples) * 0.80
)

train_samples = samples[:split]
val_samples = samples[split:]


train_dataset = CropDataset(
    train_samples,
    class_to_index,
    train_transform
)

val_dataset = CropDataset(
    val_samples,
    class_to_index,
    val_transform
)


print()
print("Training images:", len(train_dataset))
print("Validation images:", len(val_dataset))


# ============================================================
# BALANCED SAMPLER
# ============================================================

train_labels = [
    class_to_index[label]
    for _, label in train_samples
]


class_counts = {}

for label in train_labels:

    class_counts[label] = (
        class_counts.get(label, 0) + 1
    )


weights = [
    1.0 / class_counts[label]
    for label in train_labels
]


sampler = WeightedRandomSampler(
    weights,
    num_samples=len(weights),
    replacement=True
)


# ============================================================
# DATALOADER
# ============================================================

train_loader = DataLoader(
    train_dataset,
    batch_size=32,
    sampler=sampler,
    num_workers=0
)


val_loader = DataLoader(
    val_dataset,
    batch_size=32,
    shuffle=False,
    num_workers=0
)


# ============================================================
# LOAD OLD MODEL
# ============================================================

print()
print("Loading existing model...")


checkpoint = torch.load(
    OLD_MODEL,
    map_location=DEVICE
)


old_classes = checkpoint["classes"]

print(
    "Existing model classes:",
    len(old_classes)
)


# ============================================================
# CREATE NEW MODEL
# ============================================================

model = models.resnet18(
    weights=None
)


model.fc = nn.Linear(
    model.fc.in_features,
    len(class_names)
)


# Copy compatible weights
old_state = checkpoint["model_state"]

new_state = model.state_dict()


for key in old_state:

    if (
        key in new_state
        and old_state[key].shape == new_state[key].shape
    ):

        new_state[key] = old_state[key]


model.load_state_dict(
    new_state
)


model = model.to(DEVICE)


# ============================================================
# LOSS / OPTIMIZER
# ============================================================

criterion = nn.CrossEntropyLoss()

optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=0.0001,
    weight_decay=0.0001
)


# ============================================================
# TRAINING
# ============================================================

EPOCHS = 5

best_accuracy = 0.0

total_batches = len(train_loader)


print()
print("======================================")
print("       TRAINING STARTED")
print("======================================")

print(
    "Total training batches per epoch:",
    total_batches
)


for epoch in range(EPOCHS):

    epoch_start = time.time()

    model.train()

    running_loss = 0.0

    correct = 0
    total = 0


    print()
    print(
        "========== EPOCH",
        epoch + 1,
        "/",
        EPOCHS,
        "=========="
    )


    # ========================================================
    # TRAIN
    # ========================================================

    for batch_number, (images, labels) in enumerate(
        train_loader,
        start=1
    ):

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


        running_loss += (
            loss.item()
            * images.size(0)
        )


        _, predicted = torch.max(
            outputs,
            1
        )


        total += labels.size(0)

        correct += (
            predicted == labels
        ).sum().item()


        # Progress every 50 batches
        if (
            batch_number % 50 == 0
            or batch_number == total_batches
        ):

            percent = (
                batch_number
                / total_batches
                * 100
            )

            print(
                f"Batch {batch_number}/{total_batches}"
                f" ({percent:.1f}%)",
                flush=True
            )


    train_loss = (
        running_loss / total
    )

    train_accuracy = (
        correct / total * 100
    )


    # ========================================================
    # VALIDATION
    # ========================================================

    print()
    print("Running validation...")


    model.eval()

    val_correct = 0
    val_total = 0

    val_loss_total = 0.0


    with torch.no_grad():

        for images, labels in val_loader:

            images = images.to(DEVICE)
            labels = labels.to(DEVICE)


            outputs = model(images)


            loss = criterion(
                outputs,
                labels
            )


            val_loss_total += (
                loss.item()
                * images.size(0)
            )


            _, predicted = torch.max(
                outputs,
                1
            )


            val_total += labels.size(0)

            val_correct += (
                predicted == labels
            ).sum().item()


    val_loss = (
        val_loss_total / val_total
    )

    val_accuracy = (
        val_correct / val_total * 100
    )


    elapsed = (
        time.time() - epoch_start
    )


    # ========================================================
    # EPOCH RESULT
    # ========================================================

    print()
    print("--------------------------------------")

    print(
        "Epoch:",
        epoch + 1
    )

    print(
        "Training Loss:",
        round(train_loss, 4)
    )

    print(
        "Training Accuracy:",
        round(train_accuracy, 2),
        "%"
    )

    print(
        "Validation Loss:",
        round(val_loss, 4)
    )

    print(
        "Validation Accuracy:",
        round(val_accuracy, 2),
        "%"
    )

    print(
        "Time:",
        round(elapsed / 60, 2),
        "minutes"
    )

    print("--------------------------------------")


    # ========================================================
    # SAVE BEST
    # ========================================================

    if val_accuracy > best_accuracy:

        best_accuracy = val_accuracy


        torch.save(
            {
                "model_state": model.state_dict(),
                "classes": class_names,
                "validation_accuracy": val_accuracy
            },
            NEW_MODEL
        )


        print()
        print("***** BEST MODEL SAVED *****")

        print(
            "Path:",
            NEW_MODEL
        )

        print(
            "Accuracy:",
            round(best_accuracy, 2),
            "%"
        )


# ============================================================
# COMPLETE
# ============================================================

print()
print("======================================")
print("       TRAINING COMPLETE")
print("======================================")

print(
    "Best Validation Accuracy:",
    round(best_accuracy, 2),
    "%"
)

print(
    "Model saved:",
    NEW_MODEL
)

print(
    "Total classes:",
    len(class_names)
)

print("======================================")
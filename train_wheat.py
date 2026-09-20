import torch
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.optim as optim


# ==========================
# SETTINGS
# ==========================

DATA_DIR = "datasets/wheat"

BATCH_SIZE = 16
EPOCHS = 5
IMAGE_SIZE = 224


# ==========================
# IMAGE TRANSFORMS
# ==========================

transform = transforms.Compose([

    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),

    transforms.RandomHorizontalFlip(),

    transforms.RandomRotation(10),

    transforms.ToTensor(),

])


# ==========================
# LOAD DATASET
# ==========================

dataset = datasets.ImageFolder(
    DATA_DIR,
    transform=transform
)


print("Classes found:")
print(dataset.classes)

print("Total images:", len(dataset))


# ==========================
# DATA LOADER
# ==========================

loader = DataLoader(
    dataset,
    batch_size=BATCH_SIZE,
    shuffle=True
)


# ==========================
# MODEL
# ==========================

model = models.resnet18(weights=None)

model.fc = nn.Linear(
    model.fc.in_features,
    len(dataset.classes)
)


# ==========================
# LOSS + OPTIMIZER
# ==========================

criterion = nn.CrossEntropyLoss()

optimizer = optim.Adam(
    model.parameters(),
    lr=0.001
)


# ==========================
# TRAINING
# ==========================

print("\nStarting training...\n")


for epoch in range(EPOCHS):

    model.train()

    running_loss = 0.0


    for images, labels in loader:

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(
            outputs,
            labels
        )

        loss.backward()

        optimizer.step()

        running_loss += loss.item()


    print(
        f"Epoch {epoch + 1}/{EPOCHS} "
        f"- Loss: {running_loss / len(loader):.4f}"
    )


# ==========================
# SAVE MODEL
# ==========================

import os

os.makedirs("models", exist_ok=True)


torch.save({

    "model_state":
    model.state_dict(),

    "classes":
    dataset.classes

}, "models/wheat_model.pth")


print("\n✅ Wheat model saved!")

print(
    "Location: models/wheat_model.pth"
)
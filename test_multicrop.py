import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import json
import os


# ==============================
# AGRIMITRA MODEL TEST
# ==============================

MODEL_PATH = "models/multicrop_model.pth"
CLASSES_PATH = "multicrop_classes.json"

IMAGE_SIZE = 224

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


print("======================================")
print("       AGRIMITRA DISEASE TEST")
print("======================================")

print("Device:", DEVICE)


# ==============================
# LOAD CLASSES
# ==============================

with open(
    CLASSES_PATH,
    "r",
    encoding="utf-8"
) as file:

    classes = json.load(file)


print("Total classes:", len(classes))


# ==============================
# LOAD MODEL
# ==============================

model = models.resnet18(
    weights=None
)

model.fc = nn.Linear(
    model.fc.in_features,
    len(classes)
)


checkpoint = torch.load(
    MODEL_PATH,
    map_location=DEVICE
)


model.load_state_dict(
    checkpoint["model_state"]
)


model = model.to(DEVICE)

model.eval()


# ==============================
# IMAGE TRANSFORM
# ==============================

transform = transforms.Compose([
    transforms.Resize(
        (IMAGE_SIZE, IMAGE_SIZE)
    ),
    transforms.ToTensor()
])


# ==============================
# ASK IMAGE PATH
# ==============================

image_path = input(
    "\nEnter image path: "
).strip()


if not os.path.exists(image_path):

    print("\nERROR: Image not found!")

    print(
        "Please check the image path."
    )

    exit()


# ==============================
# LOAD IMAGE
# ==============================

image = Image.open(
    image_path
).convert("RGB")


image = transform(image)


image = image.unsqueeze(0)


image = image.to(DEVICE)


# ==============================
# PREDICTION
# ==============================

with torch.no_grad():

    output = model(image)

    probabilities = torch.softmax(
        output,
        dim=1
    )

    confidence, predicted = torch.max(
        probabilities,
        1
    )


predicted_class = classes[
    predicted.item()
]


confidence_value = (
    confidence.item() * 100
)


# ==============================
# RESULT
# ==============================

print("\n======================================")
print("             RESULT")
print("======================================")

print(
    "Prediction:",
    predicted_class
)

print(
    "Confidence:",
    round(
        confidence_value,
        2
    ),
    "%"
)

print("======================================")
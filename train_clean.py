import os
import json
import torch
from PIL import Image
from torchvision import transforms, models
import torch.nn as nn


# ==========================================
# AGRIMITRA MODEL TESTING
# ==========================================

MODEL_PATH = "models/multicrop_model_best.pth"

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


print("======================================")
print("       AGRIMITRA MODEL TEST")
print("======================================")

print("Device:", DEVICE)


# ==========================================
# LOAD MODEL CHECKPOINT
# ==========================================

checkpoint = torch.load(
    MODEL_PATH,
    map_location=DEVICE
)

classes = checkpoint["classes"]

print("Total classes:", len(classes))


# ==========================================
# CREATE MODEL
# ==========================================

model = models.resnet18(
    weights=None
)

model.fc = nn.Linear(
    model.fc.in_features,
    len(classes)
)

model.load_state_dict(
    checkpoint["model_state"]
)

model = model.to(DEVICE)

model.eval()


# ==========================================
# IMAGE TRANSFORM
# ==========================================

transform = transforms.Compose([

    transforms.Resize(
        (224, 224)
    ),

    transforms.ToTensor(),

    transforms.Normalize(
        mean=[
            0.485,
            0.456,
            0.406
        ],

        std=[
            0.229,
            0.224,
            0.225
        ]
    )
])


# ==========================================
# IMAGE PATH
# ==========================================

image_path = input(
    "\nEnter image path: "
).strip().strip('"')


if not os.path.exists(image_path):

    print("\nERROR: Image not found!")

    exit()


# ==========================================
# LOAD IMAGE
# ==========================================

try:

    image = Image.open(
        image_path
    ).convert("RGB")

except Exception as e:

    print(
        "\nERROR opening image:",
        e
    )

    exit()


# ==========================================
# PREDICTION
# ==========================================

image_tensor = transform(
    image
).unsqueeze(0)


image_tensor = image_tensor.to(
    DEVICE
)


with torch.no_grad():

    output = model(
        image_tensor
    )

    probabilities = torch.softmax(
        output,
        dim=1
    )[0]


# ==========================================
# TOP 5 RESULTS
# ==========================================

top_probabilities, top_indices = torch.topk(
    probabilities,
    min(5, len(classes))
)


print("\n======================================")
print("             TOP 5 RESULTS")
print("======================================")


for probability, index in zip(
    top_probabilities,
    top_indices
):

    class_name = classes[
        index.item()
    ]

    confidence = (
        probability.item()
        * 100
    )

    print(
        class_name,
        "->",
        round(
            confidence,
            2
        ),
        "%"
    )


# ==========================================
# FINAL RESULT
# ==========================================

best_index = (
    top_indices[0].item()
)

best_class = classes[
    best_index
]

best_confidence = (
    top_probabilities[0].item()
    * 100
)


print("\n======================================")
print("             FINAL RESULT")
print("======================================")

print(
    "Prediction:",
    best_class
)

print(
    "Confidence:",
    round(
        best_confidence,
        2
    ),
    "%"
)

print("======================================")
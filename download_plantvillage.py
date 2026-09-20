from datasets import load_dataset

print("Downloading PlantVillage dataset...")
print("This may take some time.")

dataset = load_dataset(
    "mohanty/PlantVillage"
)

print("\n===================================")
print("PlantVillage downloaded successfully!")
print("===================================")

print("Train images:", len(dataset["train"]))
print("Test images:", len(dataset["test"]))
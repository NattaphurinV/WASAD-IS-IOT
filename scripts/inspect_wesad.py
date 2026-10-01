import pickle

path = "data/raw/WESAD/S2/S2.pkl"

with open(path, "rb") as f:
    data = pickle.load(f)

print("Type:", type(data))

if isinstance(data, dict):
    print("Keys:", data.keys())

    for key, value in data.items():
        print(f"{key}: {type(value)}")
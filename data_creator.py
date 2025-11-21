import json
import random

# generate 1000 rows of data for you to results yourself

rows = []
for i in range(1, 1001):
    rows.append({
        "id": i,
        "name": f"User_{i:04d}",
        "age": random.randint(18, 65),
        "role": random.choice(["developer", "designer", "manager", "analyst", "engineer"]),
        "city": random.choice(["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Chennai"])
    })

data = {"users": rows}

# save file
path = "test_data_1000.json"
with open(path, "w") as f:
    json.dump(data, f, indent=2)

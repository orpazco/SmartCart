import json
import random

# Load the original JSON file
with open("../resources/products/grocery_prices.json", "r") as f:
    grocery_prices = json.load(f)

# Create a dictionary to store the random aisle and shelf for each grocery
grocery_aisle_shelf = {}
aisles = "ABCDEFG"

for grocery, price in grocery_prices.items():
    aisle = random.choice(aisles)
    shelf = random.randint(1, 8)
    grocery_aisle_shelf[grocery] = {"aisle": aisle, "shelf": shelf}

# Save the new JSON file with random aisle and shelf for each grocery
with open("../resources/products/grocery_location.json", "w") as f:
    json.dump(grocery_aisle_shelf, f, indent=4)
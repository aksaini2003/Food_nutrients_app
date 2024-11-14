# import requests

# # Step 1: Get your API Key from USDA and replace "YOUR_API_KEY"
# API_KEY = "mlBeiOYwe2flMncvE0qBDiZQoXRKs11yS6fJtcGB"
# API_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"

# def get_nutrient_info(food_item):
#     # Step 2: Prepare the parameters for API request
#     params = {
#         "api_key": API_KEY,
#         "query": food_item,
#         "dataType": ["Foundation", "Branded"],
#         "pageSize": 1  # Limit to 1 result for simplicity
#     }

#     # Step 3: Send API request
#     response = requests.get(API_URL, params=params)
#     if response.status_code == 200:
#         # Step 4: Parse the response data
#         data = response.json()
#         foods = data.get("foods", [])
#         if not foods:
#             return f"No data found for '{food_item}'"
        
#         food = foods[0]
#         description = food.get("description", "No description available")
#         nutrients = food.get("foodNutrients", [])
        
#         # Step 5: Display food item name and its nutrients
#         nutrient_info = f"Nutrient composition of {description}:\n"
#         for nutrient in nutrients:
#             name = nutrient.get("nutrientName", "Unknown")
#             value = nutrient.get("value", "N/A")
#             unit = nutrient.get("unitName", "")
#             nutrient_info += f"{name}: {value} {unit}\n"
        
#         return nutrient_info
#     else:
#         return "Failed to fetch data from USDA API"

# # Step 6: Take input from user and display nutrient composition
# food_item = input("Enter a food item name: ")
# print(get_nutrient_info(food_item))
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Replace this with your actual API key
API_KEY = "mlBeiOYwe2flMncvE0qBDiZQoXRKs11yS6fJtcGB"
API_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"

def get_nutrient_info(food_item):
    params = {
        "api_key": API_KEY,
        "query": food_item,
        "dataType": ["Foundation", "Branded"],
        "pageSize": 1
    }
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        foods = data.get("foods", [])
        if not foods:
            return None
        food = foods[0]
        description = food.get("description", "No description available")
        nutrients = food.get("foodNutrients", [])
        return {
            "description": description,
            "nutrients": nutrients
        }
    return None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        food_item = request.form.get("food_item")
        nutrient_info = get_nutrient_info(food_item)
        if nutrient_info:
            return render_template("index.html", nutrient_info=nutrient_info)
        else:
            error = f"No data found for '{food_item}'. Please try another item."
            return render_template("index.html", error=error)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, redirect
import json
from datetime import datetime

app = Flask(__name__)

FILE_NAME = "plants.json"


# --------------------------------
# Load plants from JSON file
# --------------------------------
def load_plants():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        return []


# --------------------------------
# Save plants to JSON file
# --------------------------------
def save_plants(plants):
    with open(FILE_NAME, "w") as file:
        json.dump(plants, file, indent=4)


# --------------------------------
# Home page
# --------------------------------
@app.route("/")
def home():

    plants = load_plants()

    return render_template(
        "index.html",
        plants=plants,
        search=""
    )


# --------------------------------
# Add plant
# --------------------------------
@app.route("/add", methods=["POST"])
def add_plant():

    plants = load_plants()

    name = request.form["name"]
    water = request.form["water"]
    sunlight = request.form["sunlight"]

    plant = {
        "name": name,
        "water": water,
        "sunlight": sunlight,
        "status": "Not watered today",
        "last_watered": "Never"
    }

    plants.append(plant)

    save_plants(plants)

    return redirect("/")


# --------------------------------
# Search plant
# --------------------------------
@app.route("/search")
def search():

    plants = load_plants()

    search_text = request.args.get("q", "").lower()

    if search_text:

        plants = [
            plant for plant in plants
            if search_text in plant["name"].lower()
        ]

    return render_template(
        "index.html",
        plants=plants,
        search=search_text
    )


# --------------------------------
# Water plant
# --------------------------------
@app.route("/water/<int:index>")
def water_plant(index):

    plants = load_plants()

    if 0 <= index < len(plants):

        current_time = datetime.now()

        formatted_time = current_time.strftime(
            "%d-%m-%Y %I:%M %p"
        )

        plants[index]["status"] = "Watered today ✓"

        plants[index]["last_watered"] = formatted_time

    save_plants(plants)

    return redirect("/")


# --------------------------------
# Edit plant page
# --------------------------------
@app.route("/edit/<int:index>")
def edit_plant(index):

    plants = load_plants()

    if 0 <= index < len(plants):

        return render_template(
            "index.html",
            plants=plants,
            edit_index=index,
            edit_plant=plants[index],
            search=""
        )

    return redirect("/")


# --------------------------------
# Update plant
# --------------------------------
@app.route("/update/<int:index>", methods=["POST"])
def update_plant(index):

    plants = load_plants()

    if 0 <= index < len(plants):

        plants[index]["name"] = request.form["name"]

        plants[index]["water"] = request.form["water"]

        plants[index]["sunlight"] = request.form["sunlight"]

    save_plants(plants)

    return redirect("/")


# --------------------------------
# Delete plant
# --------------------------------
@app.route("/delete/<int:index>")
def delete_plant(index):

    plants = load_plants()

    if 0 <= index < len(plants):

        plants.pop(index)

    save_plants(plants)

    return redirect("/")


# --------------------------------
# Run application
# --------------------------------
if __name__ == "__main__":
    app.run(debug=True)

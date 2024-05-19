from flask import Flask, request, redirect
from data import *

app = Flask(__name__)

@app.route("/", methods = ["GET"])
def index():
    return "Hello" #TODO: figure out if this should lead to anything

@app.route("/recipes")
def recipes():
    return jsonify([get_data(i) for i in recipe_collection.find()])

@app.route("/recipes/<recipe_id>")
def recipeID(recipe_id):
    return jsonify(get_recipe(str(recipe_id)))

@app.route("/submit", methods = ["GET","POST"])
def newRecipe():
    try:
        Recipe(**request.get_json())
    except:
        return "ERROR! Recipe couldn't be added. Please check format."
    else:
        add_recipe(request.get_json())
        return "Recipe added!"

if __name__ == "__main__":
    app.run(debug=True)


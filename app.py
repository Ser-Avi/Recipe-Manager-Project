from dataclasses import dataclass
from flask import Flask, request, redirect
from flask_mongoengine import MongoEngine
import json

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'recipe_database',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)

db.createCollection('Bananas')


@dataclass
class Ingredient:
    """
    The Ingredient class holds all the information for a single ingredient.
    Has a method to initialize and one to convert itself to a dictionary.
    """
    name: str
    amount: int
    measurement: str

@dataclass
class Recipe:
    """
    The Recipe class holds all the information about a recipe.
    Has methods for initializing and turning into a dict.
    """
    #idKey: int                  #IDs are currently simple integer indexes
    name: str
    tags: [str]
    timeToMake: float
    servings: int
    ingredients: []
    steps: [str]

#Vars currently holding all the data
Recipes = []

#Testing code
#Recipe for a simple pasta dish
testIngredient1 = Ingredient("Pasta", 1, "bunch")
testIngredient2 = Ingredient("Sauce", 1, "can")
testIngredient3 = Ingredient("Water", 8, "cups")
testIngredients = []
testIngredients.extend([testIngredient1, testIngredient2, testIngredient3])
testSteps = ["Bring the water to a boil and start heating up the sauce", "Put the past in the water for 6 minutes",
             "Drain the pasta and mix it into the sauce", "Serve with some grated Parmigiano Reggiano"]
testRecipe = Recipe("Pasta with Sauce", ["entree", "Italian"], 0.20, 2, testIngredients, testSteps)

#Recipe for a reliable meal
testIngredient4 = Ingredient("Cereal", 2, "cups")
testIngredient5 = Ingredient("Whole Milk", 0.4, "liters")
testIngredients2 = []
testIngredients2.extend([testIngredient4, testIngredient5])
testSteps2 = ["Put cereal in bowl.", "Pour milk over cereal until the milk level is slightly below the top of the cereal.",
             "Serve immediately."]
testRecipe2 = Recipe("Cereal", ["breakfast", "dinner", "lunch"], 0.1, 1, testIngredients2, testSteps2)

Recipes.append(testRecipe)
Recipes.append(testRecipe2)


@app.route("/", methods = ["GET"])
def index():
    return "Hello" #TODO: figure out if this should lead to anything

@app.route("/recipes")
def recipes():
    return Recipes #TODO: should be a list or smth of the names from the database

@app.route("/recipes/<recipe_id>")
def recipeID(recipe_id):
    return Recipes[int(recipe_id)].__dict__

@app.route("/submit", methods = ["Get","POST"])
def newRecipe():
    j = request.get_json()
    Recipes.append(Recipe(**j))
    return "Recipe added!"

if __name__ == "__main__":
    app.run(debug=True)
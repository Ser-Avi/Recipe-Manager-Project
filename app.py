from dataclasses import dataclass
from flask import Flask, request, redirect, jsonify
from pymongo import MongoClient
from bson import ObjectId
import json

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client['recipe_db']

tags_collection = db['tags']
recipe_collection = db['recipes']

tags_collection.delete_many({})

def get_data(data):
    """
    got this method/solution for mongoDB->json convertion from https://stackoverflow.com/a/63206156
    :param data: a MongoDB document
    :return: the document in a jsonify-able format
    """
    data['_id'] = str(data['_id'])
    return data

def tagManager(tag:str, recipe_id):
    curr = tags_collection.find_one({'tag':tag})
    if curr is None:
        tags_collection.insert_one({'tag': tag, 'ids': [recipe_id]})
    else:
        tags_collection.update_one({'tag':tag},{"$set":{"ids": curr.get('ids') + [recipe_id]}})

@dataclass
class Ingredient:
    """
    The Ingredient class holds all the information for a single ingredient.
    """
    name: str
    amount: int
    measurement: str

@dataclass
class Recipe:
    """
    The Recipe class holds all the information about a recipe.
    Has custom method for  turning into a dict.
    """
    #idKey: int                  #IDs are currently simple integer indexes
    name: str
    tags: [str]
    timeToMake: float
    servings: int
    ingredients: []
    steps: [str]

    def dictify(self):
        ingredientsDictList = []
        for ingredient in self.ingredients:
            ingredientsDictList.append(ingredient.__dict__)

        dictVersion = {
            "name": self.name,
            "tags": self.tags,
            "timeToMake": self.timeToMake,
            "servings": self.servings,
            "ingredients": ingredientsDictList,
            "steps": self.steps
        }
        return dictVersion

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

#used for adding/removing the two test recipes
#recipe_collection.delete_many({'servings':{"$exists": True}})
#recipe_collection.insert_many([x.dictify() for x in Recipes])

@app.route("/", methods = ["GET"])
def index():
    return "Hello" #TODO: figure out if this should lead to anything

@app.route("/recipes")
def recipes():
    return jsonify([get_data(i) for i in recipe_collection.find()])

@app.route("/recipes/<recipe_id>")
def recipeID(recipe_id):
    return jsonify(get_data(recipe_collection.find_one(ObjectId(str(recipe_id)))))

@app.route("/submit", methods = ["Get","POST"])
def newRecipe():
    j = request.get_json()
    recipe_collection.insert_one(j)
    curr_id = get_data(recipe_collection.find_one(j)).get('_id')
    for tag in j.get('tags'):
        tagManager(tag, curr_id)
    return "Recipe added!"

if __name__ == "__main__":
    app.run(debug=True)
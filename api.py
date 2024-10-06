from flask import Flask, request, jsonify
from data import RecipeRepository, Recipe
import json

app = Flask(__name__)

recipe_repository = RecipeRepository()


@app.route("/", methods=["GET"])
def index():
    return "Hello"  # TODO: figure out if this should lead to anything


@app.route("/recipes")
def recipes():
    all_recipes = recipe_repository.get_all_recipes()
    return jsonify(all_recipes)


@app.route("/recipes/<recipe_id>")
def recipeID(recipe_id: str):
    recipe = recipe_repository.get_recipe(recipe_id)

    if not recipe:
        return jsonify("Recipe not found"), 404

    return jsonify(recipe)



@app.route("/submit", methods=["Get", "POST"])
def newRecipe():
    json_map = json.loads(request.get_json())
    recipe = Recipe(id=None, **json_map)
    recipe_repository.add_recipe(recipe)
    return ""


if __name__ == "__main__":
    app.run(debug=True)
    del recipe_repository

from flask import Flask, url_for, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#db = SQLAlchemy(app)


"""
The Ingredient class holds all the information for a single ingredient.
Has a method to initialize and one to convert itself to a dictionary.
"""
class Ingredient:
    def __init__(self, name, amount, measurement):
        self.name = name                        #Str - name of ingredient
        self.amount = amount                    #Int - amount needed
        self.measurement = measurement          #Str - string of measurement

    """
    toDict turns Ingredients into a dictionary where the key are the var names and the values are their values
    """
    def toDict(self):
        dictVersion = {
            "name": self.name,
            "amount": self.amount,
            "measurement": self.measurement
        }
        return dictVersion

"""
The Recipe class holds all the information about a recipe.
Has methods for initializing and turning into a dict.
"""
class Recipe:
    def __init__(self, idKey, name: str, tags: [str], timeToMake: float, servings: int,
                 ingredients: [], steps: [str]):
        self.idKey = idKey                          #unique key identifier
        self.name = name                            #String - The recipe name used as the title
        self.tags = tags                            #List of Strings - any tags
        self.timeToMake = timeToMake                #Int - time it takes to make dish in hours(?)
        self.servings = servings                    #Int - # of meals it makes
        self.ingredients = ingredients              #List of Ingredient class - ingredients of the recipe
        self.steps = steps                          #List of Strings - the steps of the recipe

    """
    toDict turns Recipes into a dictionary where the key are the var names and the values are their values
    """
    def toDict(self):
        ingredientsDictList = []
        for ingredient in self.ingredients:
            ingredientsDictList.append(ingredient.toDict())

        dictVersion = {
            "idKey": self.idKey,
            "name": self.name,
            "tags": self.tags,
            "timeToMake": self.timeToMake,
            "servings": self.servings,
            "ingredients": ingredientsDictList,
            "steps": self.steps
        }
        return dictVersion

"""
jsonify uses the toDict methods to translate a list of recipes into nested lists and dictionaries akin to a JSON file
"""
def jsonify(recipeList):
    jsonList = []
    for i in range(len(recipeList)):
        jsonList.append(recipeList[i].toDict())
    return jsonList

#Vars currently holding all the data
Recipes = []
jsonRecipes = jsonify(Recipes)

#Testing code
#Recipe for a simple pasta dish
testIngredient1 = Ingredient("Pasta", 1, "bunch")
testIngredient2 = Ingredient("Sauce", 1, "can")
testIngredient3 = Ingredient("Water", 8, "cups")
testIngredients = []
testIngredients.extend([testIngredient1, testIngredient2, testIngredient3])
testSteps = ["Bring the water to a boil and start heating up the sauce", "Put the past in the water for 6 minutes",
             "Drain the pasta and mix it into the sauce", "Serve with some grated Parmigiano Reggiano"]
testRecipe = Recipe(0, "Pasta with Sauce", ["entree", "Italian"], 0.20, 2, testIngredients, testSteps)
Recipes.append(testRecipe)
jsonRecipes.append(testRecipe.toDict())

"""
Index page
Shows a highlight of all the recipes.
"""
@app.route("/", methods = ["GET"])
def index():
    return jsonRecipes


@app.route("/recipes")
def recipes():
    return "recipes" #should be a list or smth of the names from the database

if __name__ == "__main__":
    app.run(debug=True)


"""
OLD CODE NOT USED

OLD CODE REFERRING TO DATABASE
class DBRecipe(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    recipeName = db.Column(db.String(200), nullable = False)
    


    if request.method == "POST":
        #recipe_content = request.form["content"]
        #new_recipe = DBRecipe(recipeName = recipe_content)

        try:
            #db.session.add(new_recipe)
            #db.session.commit()
            return redirect("/")

        except:
            return "Issue adding recipe"

    else:
        #recipes = DBRecipe.query.order_by(DBRecipe.id).all()
        #return render_template("index.html", recipes = recipes)
        return "Home page"
"""
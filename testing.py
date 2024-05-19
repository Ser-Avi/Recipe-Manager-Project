from data import *
from api import *

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

def reset_db_to_tests():
    recipe_collection.delete_many({})
    recipe_collection.insert_many([x.dictify() for x in Recipes])

def clear_tags():
    tags_collection.delete_many({})

#used for adding the recipes
#recipe_collection.insert_many([x.dictify() for x in Recipes])

#used for removing *ALL* recipes that have a serving time
#recipe_collection.delete_many({'servings':{"$exists": True}})

clear_tags()
reset_db_to_tests()

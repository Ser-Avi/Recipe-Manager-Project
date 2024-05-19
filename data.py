from dataclasses import dataclass
from flask import jsonify
from pymongo import MongoClient
from bson import ObjectId

#Initializing vars
client = MongoClient('mongodb', 27017)
db = client['recipe_db']

tags_collection = db['tags']
recipe_collection = db['recipes']

#Methods
def get_data(data):
    """
    got this method/solution for mongoDB->json convertion from https://stackoverflow.com/a/63206156
    :param data: a MongoDB document
    :return: the document in a jsonify-able format
    """
    data['_id'] = str(data['_id'])
    return data

def get_recipe(id:str):
    return get_data(recipe_collection.find_one(ObjectId(id)))

def add_recipe(recipe_json):
    recipe_collection.insert_one(recipe_json)
    curr_id = get_data(recipe_collection.find_one(recipe_json)).get('_id')
    for tag in recipe_json.get('tags'):
        tag_adder(tag, curr_id)

def tag_adder(tag:str, recipe_id):
    curr = tags_collection.find_one({'tag':tag})
    if curr is None:
        tags_collection.insert_one({'tag': tag, 'ids': [recipe_id]})
    else:
        tags_collection.update_one({'tag':tag},{"$set":{"ids": curr.get('ids') + [recipe_id]}})

#Classes
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

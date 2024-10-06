from dataclasses import dataclass, field
from pymongo import MongoClient
from bson import ObjectId
from typing import List


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
    # idKey: int                  #IDs are currently simple integer indexes
    id: str | None
    name: str
    tags: List[str]
    timeToMake: int
    servings: int
    steps: List[str]
    ingredients: List[Ingredient] = field(default_factory=list)

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if k != 'id'}


class RecipeRepository:

    def __init__(self) -> None:
        self.client = MongoClient('localhost', 27017)
        db = self.client['recipe_db']
        self.tags_collection = db['tags']
        self.recipe_collection = db['recipes']

    def __del__(self) -> None:
        self.client.close()

    def get_recipe(self, id: str) -> Recipe | None:
        recipe_map = self.recipe_collection.find_one({'_id': ObjectId(id)})
        return Recipe(id=str(recipe_map.pop("_id")), **recipe_map) if recipe_map else None

    def get_all_recipes(self) -> List[Recipe]:
        recipe_maps = self.recipe_collection.find()
        recipes = map(
            lambda r: Recipe(id=str(r.pop('_id')), **r),
            recipe_maps)

        return list(recipes)

    def add_recipe(self, recipe: Recipe) -> None:
        recipe_map = recipe.to_dict()
        recipe_id = self.recipe_collection.insert_one(recipe_map).inserted_id
        # TODO: bulk update
        for t in recipe.tags:
            self.__create_or_update_tag(t, recipe_id)

    def __create_or_update_tag(self, tag_value: str, recipe_id: str) -> None:
        tag = self.tags_collection.find_one({'tag': tag_value}) or {'ids': []}
        self.tags_collection.update_one(
            {'tag': tag_value},
            {"$set": {'tag': tag_value, "ids": tag['ids'] + [recipe_id]}},
            upsert=True)

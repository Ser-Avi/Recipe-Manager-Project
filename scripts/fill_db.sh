#!/bin/sh

mongoimport --host mongodb --db recipedb --collection recipes --file ./recipe_db.recipes.json --jsonArray

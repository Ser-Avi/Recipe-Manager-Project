from flask import Flask, send_from_directory, render_template, request, abort
import requests
import json
import uuid

app = Flask(__name__, static_url_path='/static')

@app.route("/", methods = ["GET"])
def index():
    recipes = requests.get("http://backend:4200/recipes").json()

    return render_template("recipe_list_page.html", recipes=recipes)


@app.route("/add_recipe/steps/1", methods = ["GET"])
def add_recipe_step_1():
    return render_template("add_recipe_form_1.html", form_title="Please provide the name of the recipe and add tags to it")


@app.route("/add_recipe/steps/2", methods = ["POST"])
def add_recipe_step_2():
    tags = request.form.getlist("tag")
    tags.pop(0) # Removes the tag written in the text input at the time of the delete
    name = request.form.get("name")

    return render_template('add_recipe_form_2.html', tags=tags, name=name, form_title="Please add the ingredients")


@app.route("/add_tag", methods = ["POST"])
def add_tag():
    tags = request.form.getlist('tag')

    return render_template('tags.html', tags=tags)


@app.route("/delete_tag/<tag_name>", methods = ["DELETE"])
def delete_tag(tag_name):
    tags = request.form.getlist('tag')

    tags.remove(tag_name)
    tags.pop(0) # Removes the tag written in the text input at the time of the delete

    return render_template('tags.html', tags=tags)


@app.route("/add_ingredient", methods = ["POST"])
def add_ingredient():
    name = request.form.get("ingredient_name")
    amount = request.form.get("amount")
    measurement = request.form.get("measurement")

    ingredient = f"{name} - {amount} {measurement}"

    ingredients = request.form.getlist('ingredient')

    if name != "" and amount != "":
        ingredients.append(ingredient)

    return render_template('ingredients.html', ingredients=ingredients, ingredient_name=name, amount=amount)


@app.route("/delete_ingredient/<ingredient>", methods = ["DELETE"])
def delete_ingredient(ingredient):
    ingredients = request.form.getlist('ingredient')
    ingredients.remove(ingredient)

    return render_template('ingredients.html', ingredients=ingredients)


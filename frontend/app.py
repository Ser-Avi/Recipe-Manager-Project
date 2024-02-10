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

    return render_template('add_recipe_form_2.html', form_title="Please add the ingredients")


from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__, static_url_path='/static')

host = "http://localhost:4200"
# host = "http://raspberrypi:4200"


@app.route("/", methods=["GET"])
def index():
    recipes = requests.get(f"{host}/recipes").json()

    return render_template("recipe_list_page.html", recipes=recipes)


@app.route("/recipes/<recipe_id>", methods=["GET"])
def get_recipes(recipe_id):

    recipe = requests.get(
        f"{host}/recipes/{recipe_id}")
    print(recipe.content)

    return render_template("recipe_details.html", recipe=recipe.json())


@app.route("/add_recipe/steps/1", methods=["GET"])
def add_recipe_step_1():
    return render_template("add_recipe_form_1.html",
                           form_title="Please provide the name of the recipe and add tags to it")


@app.route("/add_recipe/steps/2", methods=["POST"])
def add_recipe_step_2():
    tags = request.form.getlist("tag")
    # Remove tag currently written in the text input
    tags.pop(0)
    name = request.form.get("name")

    return render_template('add_recipe_form_2.html',
                           form_title="Please add the ingredients",
                           tags=tags,
                           name=name)


@app.route("/add_recipe/steps/3", methods=["POST"])
def add_recipe_step_3():
    tags = request.form.getlist("tag")
    name = request.form.get("name")
    ingredients = request.form.getlist("ingredients")

    return render_template('add_recipe_form_3.html',
                           form_title="Please add servings and the time to make",
                           tags=tags,
                           name=name,
                           ingredients=ingredients)


@app.route("/add_recipe/steps/4", methods=["POST", "GET"])
def add_recipe_step_4():
    tags = request.form.getlist("tag")
    name = request.form.get("name")
    ingredients = request.form.getlist("ingredients")
    servings = request.form.get("servings")
    time_to_make_hours = request.form.get("hours")
    time_to_make_minutes = request.form.get("minutes")

    return render_template('add_recipe_form_4.html',
                           form_title="Please provide the steps to create the recipe",
                           tags=tags,
                           name=name,
                           ingredients=ingredients,
                           servings=servings,
                           time_to_make_hours=time_to_make_hours,
                           time_to_make_minutes=time_to_make_minutes)


@app.route("/add_recipe/overview", methods=["POST", "GET"])
def add_recipe_overview():
    tags = request.form.getlist("tag")
    name = request.form.get("name")
    ingredients = request.form.getlist("ingredients")
    servings = request.form.get("servings")
    time_to_make_hours = request.form.get("hours")
    time_to_make_minutes = request.form.get("minutes")
    steps = request.form.getlist("step")
    # Remove step currently written in the text input
    steps.pop(0)

    return render_template('add_recipe_overview.html',
                           form_title="Check your recipe before submitting",
                           tags=tags,
                           name=name,
                           ingredients=ingredients,
                           servings=servings,
                           time_to_make_hours=time_to_make_hours,
                           time_to_make_minutes=time_to_make_minutes,
                           steps=steps)


@app.route("/add_recipe/add", methods=["POST"])
def add_recipe_add():
    # tags = request.form.getlist("tag")
    # tags.pop(0) # Removes the tag written in the text input at the time of the delete
    #    name = request.form.get("name")
    #    ingredients = request.form.getlist("ingredients")
    #    servings = request.form.get("servings")
    #    time_to_make_hours = request.form.get("hours")
    #    time_to_make_minutes = request.form.get("minutes")
    #    steps = request.form.getlist("step")
    name = "Chungusz"
    tags = ["cica", "mica"]
    ingredients = [{"name": "alma", "amount": "1", "measurement": "kg"},
                   {"name": "körte", "amount": "4", "measurement": "l"}]
    servings = 7
    # time_to_make_hours = "9"
    time_to_make_minutes = 59
    steps = ["főzd meg", "edd meg"]

    alma = {
        "name": name,
        "tags": tags,
        "ingredients": ingredients,
        "servings": servings,
        "timeToMake": time_to_make_minutes,
        "steps": steps,
    }

    try:
        response = requests.post(
            f"{host}/submit", json=json.dumps(alma))
        print(response)
        return render_template('add_recipe_success.html',
                               success=response.reason)
    except Exception as e:
        return render_template('add_recipe_error.html', error=e)

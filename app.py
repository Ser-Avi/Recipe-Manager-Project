from flask import Flask, url_for, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class DBRecipe(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    recipeName = db.Column(db.String(200), nullable = False)


@app.route("/", methods = ["POST", "GET"])
def index():
    if request.method == "POST":
        recipe_content = request.form["content"]
        new_recipe = DBRecipe(recipeName = recipe_content)

        try:
            db.session.add(new_recipe)
            db.session.commit()
            return redirect("/")

        except:
            return "Issue adding recipe"

    else:
        recipes = DBRecipe.query.order_by(DBRecipe.id).all()
        return render_template("index.html", recipes = recipes)

@app.route("/recipes")
def recipes():
    recipes = DBRecipe.query.order_by(DBRecipe.id).all()
    return "recipes" #should be a list or smth of the names from the database

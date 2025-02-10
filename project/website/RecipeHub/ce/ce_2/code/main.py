from flask import Flask, render_template, request, redirect, url_for
from UserManager import UserManager
from RecipeManager import RecipeManager
from User import User
from Recipe import Recipe

app = Flask(__name__)
user_manager = UserManager()
recipe_manager = RecipeManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_manager.add_user(User(username, password))
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/submit_recipe', methods=['GET', 'POST'])
def submit_recipe():
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        recipe_manager.add_recipe(Recipe(title, ingredients, instructions))
        return redirect(url_for('home'))
    return render_template('recipe_submission.html')

@app.route('/browse_recipes')
def browse_recipes():
    recipes = recipe_manager.load_recipes()
    return render_template('recipe_browsing.html', recipes=recipes)

@app.route('/user_profile')
def user_profile():
    return render_template('user_profile.html')

@app.route('/recipe_details/<title>')
def recipe_details(title):
    recipes = recipe_manager.load_recipes()
    recipe = next((r for r in recipes if r.title == title), None)
    return render_template('recipe_details.html', recipe=recipe)

if __name__ == '__main__':
    app.run(port=8688, debug=False)

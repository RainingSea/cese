from flask import Flask, render_template, request, redirect, url_for, session
from UserManager import UserManager
from RecipeManager import RecipeManager

app = Flask(__name__)
app.secret_key = 'supersecretkey'
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
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        return "Username already exists!"
    return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('recipe_browsing'))
        return "Invalid credentials!"
    return render_template('home.html')

@app.route('/recipe_submission', methods=['GET', 'POST'])
def recipe_submission():
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        recipe = Recipe(title, ingredients, instructions)
        recipe_manager.submit_recipe(recipe)
        return redirect(url_for('recipe_browsing'))
    return render_template('recipe_submission.html')

@app.route('/recipe_browsing')
def recipe_browsing():
    recipes = recipe_manager.recipes.values()
    return render_template('recipe_browsing.html', recipes=recipes)

@app.route('/recipe_details/<title>')
def recipe_details(title):
    recipe = recipe_manager.get_recipe_details(title)
    return render_template('recipe_details.html', recipe=recipe)

@app.route('/user_profile')
def user_profile():
    username = session.get('username')
    return render_template('user_profile.html', username=username)

if __name__ == '__main__':
    app.run(port=8687, debug=False)

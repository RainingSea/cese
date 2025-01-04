from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from recipe import Recipe
from file_handler import FileHandler

app = Flask(__name__)
app.secret_key = 'your_secret_key'

file_handler = FileHandler()
users = file_handler.read_from_file('users.txt')
recipes = file_handler.read_from_file('recipes.txt')
user_recipes = file_handler.read_from_file('user_recipes.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    user = User(username, password)
    if user.login(username, password):
        session['username'] = username
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.register(username, password):
            file_handler.write_to_file('users.txt', f"{username}|{password}")
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/submit_recipe', methods=['GET', 'POST'])
def submit_recipe():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        recipe = Recipe(title, ingredients, instructions)
        if recipe.submit_recipe(title, ingredients, instructions):
            file_handler.write_to_file('recipes.txt', f"{title}|{ingredients}|{instructions}")
            user_recipes.append(f"{session['username']}|{title}")
            file_handler.write_to_file('user_recipes.txt', f"{session['username']}|{title}")
            return redirect(url_for('home'))
    return render_template('recipe_submission.html')

@app.route('/browse_recipes')
def browse_recipes():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('recipe_browsing.html', recipes=recipes)

@app.route('/recipe/<title>')
def recipe_details(title):
    if 'username' not in session:
        return redirect(url_for('login'))
    recipe = Recipe(title, '', '')
    details = recipe.fetch_recipe_details(title)
    return render_template('recipe_details.html', recipe=details)

@app.route('/profile')
def user_profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    user_recipes = [recipe for recipe in file_handler.read_from_file('user_recipes.txt') if recipe.startswith(session['username'])]
    return render_template('user_profile.html', user_recipes=user_recipes)

if __name__ == '__main__':
    app.run(debug=False)
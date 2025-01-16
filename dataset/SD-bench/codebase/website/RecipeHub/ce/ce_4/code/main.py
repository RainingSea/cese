from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from recipe import Recipe

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this in production

def load_users():
    users = {}
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split(',')
            users[username] = password
    return users

def load_recipes():
    recipes = []
    with open('recipes.txt', 'r') as file:
        for line in file:
            title, ingredients, instructions, username = line.strip().split(',')
            recipes.append(Recipe(title, ingredients, instructions, username))
    return recipes

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        user.save()
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
        username = session.get('username')
        recipe = Recipe(title, ingredients, instructions, username)
        recipe.save()
        return redirect(url_for('browse_recipes'))
    return render_template('submit_recipe.html')

@app.route('/browse_recipes')
def browse_recipes():
    recipes = load_recipes()
    return render_template('browse_recipes.html', recipes=recipes)

@app.route('/user_profile')
def user_profile():
    username = session.get('username')
    recipes = [recipe for recipe in load_recipes() if recipe.username == username]
    return render_template('user_profile.html', recipes=recipes)

if __name__ == '__main__':
    app.run(port=8690, debug=False)

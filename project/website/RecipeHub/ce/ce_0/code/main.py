from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from recipe import Recipe

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Load users and recipes from files
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
            username, title, ingredients, instructions = line.strip().split(',')
            recipes.append({
                'username': username,
                'title': title,
                'ingredients': ingredients,
                'instructions': instructions
            })
    return recipes

users = load_users()
recipes = load_recipes()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username not in users:
            users[username] = password
            with open('users.txt', 'a') as file:
                file.write(f'{username},{password}\n')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/submit_recipe', methods=['GET', 'POST'])
def submit_recipe():
    if request.method == 'POST':
        username = request.form['username']
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        recipes.append({
            'username': username,
            'title': title,
            'ingredients': ingredients,
            'instructions': instructions
        })
        with open('recipes.txt', 'a') as file:
            file.write(f'{username},{title},{ingredients},{instructions}\n')
        return redirect(url_for('home'))
    return render_template('recipe_submission.html')

@app.route('/browse_recipes')
def browse_recipes():
    return render_template('recipe_browsing.html', recipes=recipes)

@app.route('/user_profile/<username>')
def user_profile(username):
    user_recipes = [recipe for recipe in recipes if recipe['username'] == username]
    return render_template('user_profile.html', recipes=user_recipes, username=username)

@app.route('/recipe/<title>')
def recipe_details(title):
    recipe = next((recipe for recipe in recipes if recipe['title'] == title), None)
    return render_template('recipe_details.html', recipe=recipe)

if __name__ == '__main__':
    app.run(port=8686, debug=False)

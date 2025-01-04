from flask import Flask, render_template, request, redirect, session
from user import User
from recipe import Recipe
from session import Session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users and recipes from files
def load_users():
    users = {}
    with open('users.txt', 'r') as file:
        for line in file:
            username, password, entries = line.strip().split('|')
            users[username] = {'password': password, 'entries': entries.split(',')}
    return users

def load_recipes():
    recipes = []
    with open('recipes.txt', 'r') as file:
        for line in file:
            title, ingredients, instructions = line.strip().split('|')
            recipes.append({'title': title, 'ingredients': ingredients, 'instructions': instructions})
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
        user = User()
        if user.register(username, password):
            return redirect('/')
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
        recipe = Recipe()
        recipe.submit_recipe(title, ingredients, instructions)
        return redirect('/home')
    return render_template('recipe_submission.html')

@app.route('/browse_recipes')
def browse_recipes():
    return render_template('recipe_browsing.html', recipes=recipes)

@app.route('/user_profile')
def user_profile():
    return render_template('user_profile.html')

if __name__ == '__main__':
    app.run(port=8174, debug=False)

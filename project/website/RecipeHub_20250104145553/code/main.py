from flask import Flask, render_template, request, redirect, url_for, session
from typing import List

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

class Recipe:
    def __init__(self, title: str, ingredients: str, instructions: str):
        self.title = title
        self.ingredients = ingredients
        self.instructions = instructions

def load_users() -> List[User]:
    users = []
    try:
        with open('users.txt', 'r') as file:
            for line in file:
                username, password, _ = line.strip().split('|')
                users.append(User(username, password))
    except FileNotFoundError:
        pass
    return users

def load_recipes() -> List[Recipe]:
    recipes = []
    try:
        with open('recipes.txt', 'r') as file:
            for line in file:
                title, ingredients, instructions = line.strip().split('|')
                recipes.append(Recipe(title, ingredients, instructions))
    except FileNotFoundError:
        pass
    return recipes

def save_user(username: str, password: str) -> bool:
    with open('users.txt', 'a') as file:
        file.write(f"{username}|{password}|\n")
    return True

def save_recipe(title: str, ingredients: str, instructions: str) -> bool:
    with open('recipes.txt', 'a') as file:
        file.write(f"{title}|{ingredients}|{instructions}\n")
    return True

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        save_user(username, password)
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
        save_recipe(title, ingredients, instructions)
        return redirect(url_for('home'))
    return render_template('recipe_submission.html')

@app.route('/browse_recipes')
def browse_recipes():
    recipes = load_recipes()
    return render_template('recipe_browsing.html', recipes=recipes)

@app.route('/user_profile')
def user_profile():
    return render_template('user_profile.html')

if __name__ == '__main__':
    app.run(port=8177, debug=False)

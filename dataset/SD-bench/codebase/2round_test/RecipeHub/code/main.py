from flask import Flask, render_template, request, redirect, url_for, session
from typing import List

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def to_string(self) -> str:
        return f"{self.username}|{self.password}"

class Recipe:
    def __init__(self, title: str, ingredients: str, instructions: str):
        self.title = title
        self.ingredients = ingredients
        self.instructions = instructions

    def to_string(self) -> str:
        return f"{self.title}|{self.ingredients}|{self.instructions}"

def load_users() -> List[User]:
    users = []
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')[:2]
            users.append(User(username, password))
    return users

def load_recipes() -> List[Recipe]:
    recipes = []
    with open('recipes.txt', 'r') as file:
        for line in file:
            title, ingredients, instructions = line.strip().split('|')
            recipes.append(Recipe(title, ingredients, instructions))
    return recipes

def save_user(user: User) -> None:
    with open('users.txt', 'a') as file:
        file.write(user.to_string() + '\n')

def save_recipe(recipe: Recipe) -> None:
    with open('recipes.txt', 'a') as file:
        file.write(recipe.to_string() + '\n')

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
        new_user = User(username, password)
        save_user(new_user)
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
        new_recipe = Recipe(title, ingredients, instructions)
        save_recipe(new_recipe)
        return redirect(url_for('home'))
    return render_template('recipe_submission.html')

@app.route('/browse_recipes', methods=['GET'])
def browse_recipes():
    recipes = load_recipes()
    return render_template('recipe_browsing.html', recipes=recipes)

@app.route('/user_profile')
def user_profile():
    username = session.get('username')
    return render_template('user_profile.html', username=username)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8078, debug=False)

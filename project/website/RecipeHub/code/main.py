from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

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

class RecipeHub:
    def __init__(self, users_file: str, recipes_file: str):
        self.users_file = users_file
        self.recipes_file = recipes_file
        self.users = self.load_users()
        self.recipes = self.load_recipes()

    def load_users(self):
        users = []
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')[:2]
                    users.append(User(username, password))
        return users

    def load_recipes(self):
        recipes = []
        if os.path.exists(self.recipes_file):
            with open(self.recipes_file, 'r') as file:
                for line in file:
                    title, ingredients, instructions = line.strip().split('|')
                    recipes.append(Recipe(title, ingredients, instructions))
        return recipes

    def register_user(self, username: str, password: str) -> bool:
        if any(user.username == username for user in self.users):
            return False
        new_user = User(username, password)
        self.users.append(new_user)
        with open(self.users_file, 'a') as file:
            file.write(new_user.to_string() + '\n')
        return True

    def login_user(self, username: str, password: str) -> bool:
        return any(user.username == username and user.password == password for user in self.users)

    def submit_recipe(self, recipe: Recipe) -> bool:
        self.recipes.append(recipe)
        with open(self.recipes_file, 'a') as file:
            file.write(recipe.to_string() + '\n')
        return True

    def search_recipes(self, keyword: str) -> list:
        return [recipe for recipe in self.recipes if keyword.lower() in recipe.title.lower()]

    def get_user_recipes(self, username: str) -> list:
        return [recipe for recipe in self.recipes if recipe.title.startswith(username)]

    def delete_user(self, username: str) -> bool:
        self.users = [user for user in self.users if user.username != username]
        self.save_users()
        return True

    def save_users(self):
        with open(self.users_file, 'w') as file:
            for user in self.users:
                file.write(user.to_string() + '\n')

# Initialize RecipeHub
recipe_hub = RecipeHub('users.txt', 'recipes.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if recipe_hub.login_user(username, password):
        session['username'] = username
        flash("Login successful!", "success")
        return redirect(url_for('home'))
    flash("Invalid username or password!", "error")
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if recipe_hub.register_user(username, password):
            flash("Registration successful!", "success")
            return redirect(url_for('login'))
        flash("Username already exists!", "error")
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
        recipe = Recipe(title, ingredients, instructions)
        if recipe_hub.submit_recipe(recipe):
            flash("Recipe submitted successfully!", "success")
            return redirect(url_for('home'))
        flash("Error submitting recipe!", "error")
    return render_template('recipe_submission.html')

@app.route('/browse_recipes', methods=['GET', 'POST'])
def browse_recipes():
    if request.method == 'POST':
        keyword = request.form['keyword']
        recipes = recipe_hub.search_recipes(keyword)
        return render_template('recipe_browsing.html', recipes=recipes)
    return render_template('recipe_browsing.html', recipes=recipe_hub.recipes)

@app.route('/recipe_details/<title>')
def recipe_details(title):
    recipe = recipe_hub.get_recipe_details(title)
    if recipe:
        return render_template('recipe_details.html', recipe=recipe)
    flash("Recipe not found!", "error")
    return redirect(url_for('browse_recipes'))

@app.route('/user_profile', methods=['GET', 'POST'])
def user_profile():
    if request.method == 'POST':
        if 'delete_account' in request.form:
            username = session.get('username')
            recipe_hub.delete_user(username)
            session.clear()
            flash("Account deleted successfully!", "success")
            return redirect(url_for('login'))
    user_recipes = recipe_hub.get_user_recipes(session.get('username', ''))
    return render_template('user_profile.html', user_recipes=user_recipes)

if __name__ == '__main__':
    app.run(port=8163, debug=True)

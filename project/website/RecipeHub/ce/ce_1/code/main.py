from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        if not os.path.exists('users.txt'):
            return []
        with open('users.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def register(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username:
                return False
        self.users.append([username, password])
        self.save_users()
        return True

    def save_users(self):
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write('|'.join(user) + '\n')

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username and user[1] == password:
                return True
        return False

    def delete_account(self, username: str) -> bool:
        for user in self.users:
            if user[0] == username:
                self.users.remove(user)
                self.save_users()
                return True
        return False

class RecipeManager:
    def __init__(self):
        self.recipes = self.load_recipes()

    def load_recipes(self):
        if not os.path.exists('recipes.txt'):
            return []
        with open('recipes.txt', 'r') as file:
            return [line.strip().split('|') for line in file.readlines()]

    def submit_recipe(self, title: str, ingredients: str, instructions: str) -> bool:
        self.recipes.append([title, ingredients, instructions])
        self.save_recipes()
        return True

    def save_recipes(self):
        with open('recipes.txt', 'w') as file:
            for recipe in self.recipes:
                file.write('|'.join(recipe) + '\n')

    def search_recipes(self, keyword: str):
        return [recipe for recipe in self.recipes if keyword.lower() in recipe[0].lower()]

    def get_recipe_details(self, title: str):
        for recipe in self.recipes:
            if recipe[0] == title:
                return recipe
        return None

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
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        else:
            flash('Username already exists. Please choose a different one.')
    return render_template('registration.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            return render_template('home.html', username=username)
        else:
            flash('Invalid credentials. Please try again.')
    return render_template('home.html')

@app.route('/submit_recipe', methods=['GET', 'POST'])
def submit_recipe():
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        recipe_manager.submit_recipe(title, ingredients, instructions)
        flash('Recipe submitted successfully!')
    return render_template('recipe_submission.html')

@app.route('/browse_recipes', methods=['GET'])
def browse_recipes():
    return render_template('recipe_browsing.html', recipes=recipe_manager.recipes)

@app.route('/recipe_details/<title>', methods=['GET'])
def recipe_details(title):
    recipe = recipe_manager.get_recipe_details(title)
    return render_template('recipe_details.html', recipe=recipe)

@app.route('/user_profile', methods=['GET'])
def user_profile():
    return render_template('user_profile.html')

if __name__ == '__main__':
    app.run(port=8403, debug=False)

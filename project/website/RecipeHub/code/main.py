from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'dev'

class FileStorage:
    def read_users(self):
        if not os.path.exists('users.txt'):
            return []
        with open('users.txt', 'r', encoding='utf-8') as f:
            return [line.strip().split('|') for line in f.readlines()]

    def write_users(self, data):
        with open('users.txt', 'w', encoding='utf-8') as f:
            for user in data:
                f.write(f"{user[0]}|{user[1]}\n")

    def read_recipes(self):
        if not os.path.exists('recipes.txt'):
            return []
        with open('recipes.txt', 'r', encoding='utf-8') as f:
            return [line.strip().split('|') for line in f.readlines()]

    def write_recipes(self, data):
        with open('recipes.txt', 'w', encoding='utf-8') as f:
            for recipe in data:
                f.write(f"{recipe[0]}|{recipe[1]}|{recipe[2]}|{recipe[3]}|{recipe[4]}\n")

class AuthManager:
    def __init__(self):
        self.storage = FileStorage()

    def login(self, username, password):
        users = self.storage.read_users()
        for user in users:
            if user[0] == username and user[1] == password:
                return True
        return False

    def register(self, username, password):
        users = self.storage.read_users()
        for user in users:
            if user[0] == username:
                return False
        users.append([username, password])
        self.storage.write_users(users)
        return True

    def delete_user(self, username):
        users = self.storage.read_users()
        recipes = self.storage.read_recipes()
        users = [user for user in users if user[0] != username]
        self.storage.write_users(users)
        recipes = [recipe for recipe in recipes if recipe[4] != username]
        self.storage.write_recipes(recipes)
        return True

class RecipeManager:
    def __init__(self):
        self.storage = FileStorage()

    def add_recipe(self, title, ingredients, instructions, author):
        recipes = self.storage.read_recipes()
        recipe_id = str(len(recipes) + 1)
        recipes.append([recipe_id, title, ingredients, instructions, author])
        self.storage.write_recipes(recipes)
        return True

    def get_recipes(self):
        return self.storage.read_recipes()

    def search_recipes(self, query):
        recipes = self.storage.read_recipes()
        return [recipe for recipe in recipes if query.lower() in recipe[1].lower()]

    def get_recipe_details(self, recipe_id):
        recipes = self.storage.read_recipes()
        for recipe in recipes:
            if recipe[0] == recipe_id:
                return {
                    'id': recipe[0],
                    'title': recipe[1],
                    'ingredients': recipe[2],
                    'instructions': recipe[3],
                    'author': recipe[4]
                }
        return None

auth_manager = AuthManager()
recipe_manager = RecipeManager()

@app.route('/')
def root():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('home'))
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth_manager.register(username, password):
            return redirect(url_for('login'))
        return render_template('register.html', error="Username already exists")
    return render_template('register.html')

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', username=session['username'])

@app.route('/submit_recipe', methods=['GET', 'POST'])
def submit_recipe():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        recipe_manager.add_recipe(title, ingredients, instructions, session['username'])
        return redirect(url_for('home'))
    return render_template('submit_recipe.html')

@app.route('/browse_recipes', methods=['GET', 'POST'])
def browse_recipes():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        query = request.form['query']
        recipes = recipe_manager.search_recipes(query)
    else:
        recipes = recipe_manager.get_recipes()
    return render_template('browse_recipes.html', recipes=recipes)

@app.route('/recipe_details/<recipe_id>')
def recipe_details(recipe_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    recipe = recipe_manager.get_recipe_details(recipe_id)
    if not recipe:
        return redirect(url_for('browse_recipes'))
    return render_template('recipe_details.html', recipe=recipe)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        auth_manager.delete_user(session['username'])
        session.pop('username', None)
        return redirect(url_for('login'))
    username = session['username']
    recipes = recipe_manager.get_recipes()
    user_recipes = [recipe for recipe in recipes if recipe[4] == username]
    return render_template('profile.html', username=username, recipes=user_recipes)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8560, debug=False)

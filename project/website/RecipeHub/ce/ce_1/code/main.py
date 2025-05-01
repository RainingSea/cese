from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash
import json
import os

app = Flask(__name__)
app.secret_key = 'dev'  # For development only

class FileStorage:
    def __init__(self):
        self.users_file = 'users.txt'
        self.recipes_file = 'recipes.txt'
        self.user_recipes_file = 'user_recipes.txt'
        
        # Initialize files if they don't exist
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                f.write('')
        if not os.path.exists(self.recipes_file):
            with open(self.recipes_file, 'w') as f:
                f.write('')
        if not os.path.exists(self.user_recipes_file):
            with open(self.user_recipes_file, 'w') as f:
                f.write('{}')

    def read_users(self):
        users = {}
        with open(self.users_file, 'r') as f:
            for line in f:
                if line.strip():
                    username, password = line.strip().split(',')
                    users[username] = password
        return users

    def write_users(self, users):
        with open(self.users_file, 'w') as f:
            for username, password in users.items():
                f.write(f"{username},{password}\n")

    def read_recipes(self):
        recipes = []
        with open(self.recipes_file, 'r') as f:
            for line in f:
                if line.strip():
                    recipes.append(json.loads(line.strip()))
        return recipes

    def write_recipes(self, recipes):
        with open(self.recipes_file, 'w') as f:
            for recipe in recipes:
                f.write(json.dumps(recipe) + '\n')

    def read_user_recipes(self):
        with open(self.user_recipes_file, 'r') as f:
            return json.load(f)

    def write_user_recipes(self, user_recipes):
        with open(self.user_recipes_file, 'w') as f:
            json.dump(user_recipes, f)

class AuthManager:
    def __init__(self, storage):
        self.storage = storage

    def login(self, username, password):
        users = self.storage.read_users()
        return username in users and users[username] == password

    def register(self, username, password):
        users = self.storage.read_users()
        if username in users:
            return False
        users[username] = password
        self.storage.write_users(users)
        
        # Initialize user's recipe list
        user_recipes = self.storage.read_user_recipes()
        user_recipes[username] = []
        self.storage.write_user_recipes(user_recipes)
        return True

    def delete_account(self, username):
        users = self.storage.read_users()
        if username not in users:
            return False
        
        del users[username]
        self.storage.write_users(users)
        
        # Remove user's recipes mapping
        user_recipes = self.storage.read_user_recipes()
        if username in user_recipes:
            del user_recipes[username]
            self.storage.write_user_recipes(user_recipes)
        return True

class RecipeManager:
    def __init__(self, storage):
        self.storage = storage

    def submit_recipe(self, username, title, ingredients, instructions):
        recipes = self.storage.read_recipes()
        recipe_id = len(recipes) + 1
        new_recipe = {
            'id': recipe_id,
            'title': title,
            'ingredients': ingredients,
            'instructions': instructions,
            'author': username
        }
        recipes.append(new_recipe)
        self.storage.write_recipes(recipes)
        
        # Update user's recipe list
        user_recipes = self.storage.read_user_recipes()
        if username not in user_recipes:
            user_recipes[username] = []
        user_recipes[username].append(recipe_id)
        self.storage.write_user_recipes(user_recipes)
        return True

    def get_recipes(self, search_term=None):
        recipes = self.storage.read_recipes()
        if search_term:
            return [r for r in recipes if search_term.lower() in r['title'].lower()]
        return recipes

    def get_recipe_details(self, recipe_id):
        recipes = self.storage.read_recipes()
        for recipe in recipes:
            if recipe['id'] == recipe_id:
                return recipe
        return None

    def get_user_recipes(self, username):
        user_recipes = self.storage.read_user_recipes()
        if username not in user_recipes:
            return []
        
        recipes = self.storage.read_recipes()
        return [r for r in recipes if r['id'] in user_recipes[username]]

# Initialize components
storage = FileStorage()
auth_manager = AuthManager(storage)
recipe_manager = RecipeManager(storage)

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', username=session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('home'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth_manager.register(username, password):
            session['username'] = username
            return redirect(url_for('home'))
        return render_template('register.html', error='Username already exists')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/submit_recipe', methods=['GET', 'POST'])
def submit_recipe():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        recipe_manager.submit_recipe(session['username'], title, ingredients, instructions)
        return redirect(url_for('home'))
    return render_template('submit_recipe.html')

@app.route('/browse_recipes', methods=['GET', 'POST'])
def browse_recipes():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    search_term = request.args.get('search', '') if request.method == 'GET' else request.form.get('search', '')
    recipes = recipe_manager.get_recipes(search_term)
    return render_template('browse_recipes.html', recipes=recipes, search_term=search_term)

@app.route('/recipe_details/<int:recipe_id>')
def recipe_details(recipe_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    recipe = recipe_manager.get_recipe_details(recipe_id)
    if not recipe:
        return redirect(url_for('browse_recipes'))
    return render_template('recipe_details.html', recipe=recipe)

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user_recipes = recipe_manager.get_user_recipes(session['username'])
    return render_template('profile.html', username=session['username'], recipes=user_recipes)

@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    auth_manager.delete_account(username)
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8559, debug=False)

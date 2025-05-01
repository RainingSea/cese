from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

class UserManager:
    def __init__(self, users_file='users.txt'):
        self.users_file = users_file
        if not os.path.exists(self.users_file):
            open(self.users_file, 'w').close()

    def register_user(self, username, password):
        with open(self.users_file, 'r') as f:
            for line in f:
                if line.startswith(username + '|'):
                    return False
        
        with open(self.users_file, 'a') as f:
            f.write(f"{username}|{password}\n")
        return True

    def authenticate(self, username, password):
        with open(self.users_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 2 and parts[0] == username and parts[1] == password:
                    return True
        return False

    def delete_user(self, username):
        lines = []
        with open(self.users_file, 'r') as f:
            lines = f.readlines()
        
        with open(self.users_file, 'w') as f:
            for line in lines:
                if not line.startswith(username + '|'):
                    f.write(line)
        return True

class RecipeManager:
    def __init__(self, recipes_file='recipes.txt', user_recipes_dir='user_recipes'):
        self.recipes_file = recipes_file
        self.user_recipes_dir = user_recipes_dir
        
        if not os.path.exists(self.recipes_file):
            open(self.recipes_file, 'w').close()
        
        if not os.path.exists(self.user_recipes_dir):
            os.makedirs(self.user_recipes_dir)

    def _get_next_id(self):
        try:
            with open(self.recipes_file, 'r') as f:
                lines = f.readlines()
                if not lines:
                    return 1
                last_id = int(lines[-1].split('|')[0])
                return last_id + 1
        except:
            return 1

    def add_recipe(self, title, ingredients, instructions, author):
        recipe_id = self._get_next_id()
        with open(self.recipes_file, 'a') as f:
            f.write(f"{recipe_id}|{title}|{ingredients}|{instructions}|{author}\n")
        
        user_recipe_file = os.path.join(self.user_recipes_dir, author + '.txt')
        with open(user_recipe_file, 'a') as f:
            f.write(f"{recipe_id}\n")
        
        return True

    def get_recipe(self, recipe_id):
        with open(self.recipes_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if parts[0] == str(recipe_id):
                    return {
                        'id': parts[0],
                        'title': parts[1],
                        'ingredients': parts[2],
                        'instructions': parts[3],
                        'author': parts[4]
                    }
        return None

    def search_recipes(self, query):
        results = []
        with open(self.recipes_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if query.lower() in parts[1].lower() or query.lower() in parts[2].lower():
                    results.append({
                        'id': parts[0],
                        'title': parts[1],
                        'ingredients': parts[2],
                        'author': parts[4]
                    })
        return results

    def get_user_recipes(self, username):
        user_recipe_file = os.path.join(self.user_recipes_dir, username + '.txt')
        if not os.path.exists(user_recipe_file):
            return []
        
        recipe_ids = []
        with open(user_recipe_file, 'r') as f:
            recipe_ids = [line.strip() for line in f]
        
        recipes = []
        with open(self.recipes_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if parts[0] in recipe_ids:
                    recipes.append({
                        'id': parts[0],
                        'title': parts[1],
                        'ingredients': parts[2],
                        'instructions': parts[3]
                    })
        return recipes

user_manager = UserManager()
recipe_manager = RecipeManager()

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
        
        if user_manager.authenticate(username, password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if user_manager.register_user(username, password):
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error="Username already exists")
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
        author = session['username']
        
        recipe_manager.add_recipe(title, ingredients, instructions, author)
        return redirect(url_for('home'))
    
    return render_template('submit_recipe.html')

@app.route('/browse_recipes', methods=['GET', 'POST'])
def browse_recipes():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    recipes = []
    if request.method == 'POST':
        query = request.form['query']
        recipes = recipe_manager.search_recipes(query)
    else:
        with open('recipes.txt', 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                recipes.append({
                    'id': parts[0],
                    'title': parts[1],
                    'ingredients': parts[2],
                    'author': parts[4]
                })
    
    return render_template('browse_recipes.html', recipes=recipes)

@app.route('/recipe_details/<recipe_id>')
def recipe_details(recipe_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    recipe = recipe_manager.get_recipe(recipe_id)
    if not recipe:
        return redirect(url_for('browse_recipes'))
    
    return render_template('recipe_details.html', recipe=recipe)

@app.route('/user_profile')
def user_profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    recipes = recipe_manager.get_user_recipes(username)
    return render_template('user_profile.html', username=username, recipes=recipes)

@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    user_manager.delete_user(username)
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8558, debug=False)

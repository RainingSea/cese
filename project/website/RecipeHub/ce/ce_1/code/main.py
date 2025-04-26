import os
from html import escape
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.load_users()

    def load_users(self):
        self.users = {}
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = password

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open(self.users_file, 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def delete_account(self, username: str) -> bool:
        if username in self.users:
            del self.users[username]
            with open(self.users_file, 'w') as file:
                for user, pwd in self.users.items():
                    file.write(f"{user}|{pwd}\n")
            return True
        return False

class RecipeManager:
    def __init__(self, recipes_file: str):
        self.recipes_file = recipes_file
        self.load_recipes()

    def load_recipes(self):
        self.recipes = []
        if os.path.exists(self.recipes_file):
            with open(self.recipes_file, 'r') as file:
                for line in file:
                    title, ingredients, instructions = line.strip().split('|')
                    self.recipes.append({
                        'title': title,
                        'ingredients': ingredients,
                        'instructions': instructions
                    })

    def submit_recipe(self, title: str, ingredients: str, instructions: str) -> bool:
        self.recipes.append({'title': title, 'ingredients': ingredients, 'instructions': instructions})
        with open(self.recipes_file, 'a') as file:
            file.write(f"{title}|{ingredients}|{instructions}\n")
        return True

    def search_recipes(self, query: str):
        return [recipe for recipe in self.recipes if query.lower() in recipe['title'].lower()]

    def get_recipe_details(self, title: str):
        for recipe in self.recipes:
            if recipe['title'] == title:
                return recipe
        return None

user_manager = UserManager('users.txt')
recipe_manager = RecipeManager('recipes.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = escape(request.form['username'])
        password = escape(request.form['password'])
        if user_manager.register(username, password):
            flash('Registration successful!')
            return redirect(url_for('login'))
        else:
            flash('Username already exists!')
    return render_template('registration.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/submit_recipe', methods=['GET', 'POST'])
def submit_recipe():
    if request.method == 'POST':
        title = escape(request.form['title'])
        ingredients = escape(request.form['ingredients'])
        instructions = escape(request.form['instructions'])
        recipe_manager.submit_recipe(title, ingredients, instructions)
        flash('Recipe submitted successfully!')
        return redirect(url_for('home'))
    return render_template('recipe_submission.html')

@app.route('/browse_recipes', methods=['GET'])
def browse_recipes():
    query = request.args.get('query', '')
    recipes = recipe_manager.search_recipes(query)
    return render_template('recipe_browsing.html', recipes=recipes)

@app.route('/recipe_details/<title>', methods=['GET'])
def recipe_details(title):
    recipe = recipe_manager.get_recipe_details(title)
    return render_template('recipe_details.html', recipe=recipe)

@app.route('/user_profile', methods=['GET'])
def user_profile():
    return render_template('user_profile.html')

if __name__ == '__main__':
    app.run(port=8231, debug=False)

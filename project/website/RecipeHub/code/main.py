from flask import Flask, render_template, request, redirect, session, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self, users_file: str):
        self.users_file = users_file
        self.load_users()

    def load_users(self):
        self.users = {}
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password = line.strip().split(',')
                    self.users[username] = password

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open(self.users_file, 'a') as file:
            file.write(f"{username},{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def delete_account(self, username: str) -> bool:
        if username in self.users:
            del self.users[username]
            with open(self.users_file, 'w') as file:
                for user, pwd in self.users.items():
                    file.write(f"{user},{pwd}\n")
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

    def search_recipes(self, keyword: str) -> list:
        return [recipe for recipe in self.recipes if keyword.lower() in recipe['title'].lower()]

    def get_recipe_details(self, title: str) -> dict:
        for recipe in self.recipes:
            if recipe['title'] == title:
                return recipe
        return None

user_manager = UserManager('users.txt')
recipe_manager = RecipeManager('recipes.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect('/home')
        else:
            flash('Invalid username or password.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash('Registration successful!')
            return redirect('/')
        else:
            flash('Username already exists!')
    return render_template('register.html')

@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html')
    return redirect('/')

@app.route('/submit_recipe', methods=['GET', 'POST'])
def submit_recipe():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        recipe_manager.submit_recipe(title, ingredients, instructions)
        return redirect('/home')
    return render_template('recipe_submission.html')

@app.route('/browse_recipes', methods=['GET', 'POST'])
def browse_recipes():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        keyword = request.form['keyword']
        recipes = recipe_manager.search_recipes(keyword)
        return render_template('recipe_browsing.html', recipes=recipes)
    return render_template('recipe_browsing.html', recipes=recipe_manager.recipes)

@app.route('/user_profile')
def user_profile():
    if 'username' not in session:
        return redirect('/')
    return render_template('user_profile.html', recipes=recipe_manager.recipes)

@app.route('/recipe_details/<title>')
def recipe_details(title):
    recipe = recipe_manager.get_recipe_details(title)
    return render_template('recipe_details.html', recipe=recipe)

@app.route('/delete_account', methods=['POST'])
def delete_account():
    username = session.get('username')
    if user_manager.delete_account(username):
        session.pop('username', None)
        flash('Account deleted successfully.')
        return redirect('/')
    return redirect('/user_profile')

if __name__ == '__main__':
    app.run(port=8233, debug=False)

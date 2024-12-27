from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'
users_file = 'users.txt'
recipes_file = 'recipes.txt'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open(users_file, 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    def delete(self):
        users = []
        with open(users_file, 'r') as f:
            users = f.readlines()
        with open(users_file, 'w') as f:
            for user in users:
                if user.split('|')[0] != self.username:
                    f.write(user)

class Recipe:
    def __init__(self, title: str, ingredients: str, instructions: str):
        self.title = title
        self.ingredients = ingredients
        self.instructions = instructions

    def save(self):
        with open(recipes_file, 'a') as f:
            f.write(f"{self.title}|{self.ingredients}|{self.instructions}\n")

class RecipeHub:
    def register(self, username: str, password: str) -> bool:
        with open(users_file, 'r') as f:
            users = f.readlines()
            for user in users:
                if user.split('|')[0] == username:
                    return False  # User already exists
        new_user = User(username, password)
        new_user.save()
        return True

    def login(self, username: str, password: str) -> bool:
        with open(users_file, 'r') as f:
            users = f.readlines()
            for user in users:
                if user.split('|')[0] == username and user.split('|')[1].strip() == password:
                    return True  # Login successful
        return False

    def submit_recipe(self, title: str, ingredients: str, instructions: str) -> bool:
        new_recipe = Recipe(title, ingredients, instructions)
        new_recipe.save()
        return True

    def search_recipes(self, keyword: str) -> list:
        with open(recipes_file, 'r') as f:
            recipes = f.readlines()
            matching_recipes = []
            for recipe in recipes:
                if keyword.lower() in recipe.split('|')[0].lower():
                    matching_recipes.append(recipe.strip())
            return matching_recipes

    def get_user_recipes(self, username: str) -> list:
        user_recipes = []
        with open(recipes_file, 'r') as f:
            recipes = f.readlines()
            for recipe in recipes:
                if recipe.split('|')[0] == username:  # Assuming the title is the username for simplicity
                    user_recipes.append(recipe.strip())
        return user_recipes

    def delete_account(self, username: str) -> bool:
        user = User(username, "")
        user.delete()
        return True

    def get_recipe_details(self, title: str) -> Recipe:
        with open(recipes_file, 'r') as f:
            recipes = f.readlines()
            for recipe in recipes:
                if recipe.split('|')[0] == title:
                    title, ingredients, instructions = recipe.strip().split('|')
                    return Recipe(title, ingredients, instructions)
        return None

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hub = RecipeHub()
        if hub.login(username, password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return "Invalid credentials, please try again."
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hub = RecipeHub()
        if hub.register(username, password):
            return redirect(url_for('login'))
        else:
            return "Username already exists, please choose another."
    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/recipe_submission', methods=['GET', 'POST'])
def recipe_submission():
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        hub = RecipeHub()
        if hub.submit_recipe(title, ingredients, instructions):
            return "Recipe submitted successfully!"
        else:
            return "Error submitting recipe."
    return render_template('recipe_submission.html')

@app.route('/recipe_browsing', methods=['GET', 'POST'])
def recipe_browsing():
    if request.method == 'POST':
        keyword = request.form['keyword']
        hub = RecipeHub()
        recipes = hub.search_recipes(keyword)
        return render_template('recipe_browsing.html', recipes=recipes)
    return render_template('recipe_browsing.html', recipes=[])

@app.route('/recipe_details/<title>')
def recipe_details(title):
    hub = RecipeHub()
    recipe = hub.get_recipe_details(title)
    if recipe:
        return render_template('recipe_details.html', recipe=recipe)
    return "Recipe not found."

@app.route('/user_profile')
def user_profile():
    username = session.get('username')
    hub = RecipeHub()
    user_recipes = hub.get_user_recipes(username)
    return render_template('user_profile.html', username=username, recipes=user_recipes)

@app.route('/delete_account', methods=['POST'])
def delete_account():
    username = session.get('username')
    hub = RecipeHub()
    hub.delete_account(username)
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
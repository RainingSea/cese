from flask import Flask, render_template, request, redirect, session
from user import User
from recipe import Recipe
from file_manager import FileManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

file_manager = FileManager()
users = file_manager.read_file('users.txt')
recipes = file_manager.read_file('recipes.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    user = User(username, password)
    if user.login(username, password):
        session['username'] = username
        return redirect('/home')
    return render_template('login.html', error="Invalid username or password.")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.register(username, password):
            return redirect('/')
    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/submit_recipe', methods=['GET', 'POST'])
def submit_recipe():
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients'].split(',')
        instructions = request.form['instructions']
        recipe = Recipe(title, ingredients, instructions)
        if recipe.submit_recipe(title, ingredients, instructions):
            return render_template('recipe_submission.html', success="Recipe submitted successfully!")
        return render_template('recipe_submission.html', error="Recipe submission failed. Title may already exist.")
    return render_template('recipe_submission.html')

@app.route('/browse_recipes', methods=['GET', 'POST'])
def browse_recipes():
    recipe = Recipe('', [], '')
    all_recipes = recipe.fetch_recipes()
    if request.method == 'POST':
        search_query = request.form['search']
        filtered_recipes = [r for r in all_recipes if search_query.lower() in r.lower()]
        return render_template('recipe_browsing.html', recipes=filtered_recipes)
    return render_template('recipe_browsing.html', recipes=all_recipes)

@app.route('/recipe/<title>')
def recipe_details(title):
    recipe = Recipe('', [], '')
    details = recipe.fetch_recipe_details(title)
    return render_template('recipe_details.html', recipe=details)

@app.route('/profile')
def user_profile():
    username = session.get('username')
    user = User(username, '')
    submitted_recipes = user.load_user_recipes(username)
    return render_template('user_profile.html', recipes=submitted_recipes)

@app.route('/delete_account', methods=['POST'])
def delete_account():
    username = session.get('username')
    user = User(username, '')
    if user.delete_account(username):
        session.pop('username', None)
        return redirect('/')
    return render_template('user_profile.html', error="Account deletion failed.")

if __name__ == '__main__':
    app.run(port=8150, debug=True)

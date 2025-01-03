from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from recipe import Recipe
from file_manager import FileManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

file_manager = FileManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    user = User()
    if user.login(username, password):
        session['username'] = username
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User()
        if user.register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/recipe_submission', methods=['GET', 'POST'])
def recipe_submission():
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients'].split(',')
        instructions = request.form['instructions']
        recipe = Recipe()
        if recipe.submit_recipe(title, ingredients, instructions):
            return render_template('recipe_submission.html', message="Recipe submitted successfully!")
        else:
            return render_template('recipe_submission.html', message="Error submitting recipe.")
    return render_template('recipe_submission.html')

@app.route('/recipe_browsing', methods=['GET', 'POST'])
def recipe_browsing():
    recipe = Recipe()
    recipes = recipe.fetch_recipes()
    if request.method == 'POST':
        keyword = request.form['keyword']
        recipes = [r for r in recipes if keyword.lower() in r.split('|')[0].lower()]
    return render_template('recipe_browsing.html', recipes=recipes)

@app.route('/recipe_details/<title>')
def recipe_details(title):
    recipe = Recipe()
    details = recipe.fetch_recipe_details(title)
    return render_template('recipe_details.html', details=details)

@app.route('/user_profile', methods=['GET', 'POST'])
def user_profile():
    user = User()
    submitted_recipes = user.fetch_user_recipes(session['username'])
    if request.method == 'POST':
        user.delete_account(session['username'])
        session.pop('username', None)
        return redirect(url_for('login'))
    return render_template('user_profile.html', recipes=submitted_recipes)

if __name__ == '__main__':
    app.run(port=8149, debug=True)

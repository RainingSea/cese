from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from recipe_manager import RecipeManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

user_manager = UserManager()
recipe_manager = RecipeManager()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        else:
            return "Registration failed"
    return render_template('registration.html')

@app.route('/recipe_submission', methods=['GET', 'POST'])
def recipe_submission():
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        recipe_manager.submit_recipe(title, ingredients, instructions)
        return redirect(url_for('recipe_browsing'))
    return render_template('recipe_submission.html')

@app.route('/recipe_browsing', methods=['GET'])
def recipe_browsing():
    recipes = recipe_manager.recipes
    return render_template('recipe_browsing.html', recipes=recipes)

@app.route('/user_profile', methods=['GET'])
def user_profile():
    username = session.get('username')
    return render_template('user_profile.html', username=username)

@app.route('/recipe_details/<title>', methods=['GET'])
def recipe_details(title):
    recipe = recipe_manager.get_recipe_details(title)
    return render_template('recipe_details.html', recipe=recipe)

if __name__ == '__main__':
    app.run(port=8176, debug=False)

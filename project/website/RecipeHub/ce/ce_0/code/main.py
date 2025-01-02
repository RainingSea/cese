from flask import Flask, render_template, request, redirect, url_for, flash
from user import User
from recipe_hub import RecipeHub
from recipe import Recipe

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key in production

# Initialize RecipeHub with data files
recipe_hub = RecipeHub('users.txt', 'recipes.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if recipe_hub.login_user(username, password):
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if recipe_hub.register_user(username, password):
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username already exists. Please choose a different one.', 'error')
    return render_template('register.html')

@app.route('/submit_recipe', methods=['GET', 'POST'])
def submit_recipe():
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        recipe = Recipe(title, ingredients, instructions)
        if recipe_hub.submit_recipe(recipe):
            flash('Recipe submitted successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Error submitting recipe. Please try again.', 'error')
    return render_template('recipe_submission.html')

@app.route('/browse_recipes', methods=['GET', 'POST'])
def browse_recipes():
    recipes = []
    if request.method == 'POST':
        keyword = request.form['keyword']
        recipes = recipe_hub.search_recipes(keyword)
    return render_template('recipe_browsing.html', recipes=recipes)

if __name__ == '__main__':
    app.run(port=8161, debug=True)

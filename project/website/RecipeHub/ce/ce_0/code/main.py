from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from recipe_manager import RecipeManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key

user_manager = UserManager()
recipe_manager = RecipeManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/submit_recipe', methods=['GET', 'POST'])
def submit_recipe():
    if request.method == 'POST':
        username = session.get('username')
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        recipe = Recipe(username, title, ingredients, instructions)
        recipe_manager.submit_recipe(recipe)
        return redirect(url_for('home'))
    return render_template('recipe_submission.html')

@app.route('/browse_recipes')
def browse_recipes():
    recipes = recipe_manager.search_recipes('')
    return render_template('recipe_browsing.html', recipes=recipes)

@app.route('/profile')
def profile():
    username = session.get('username')
    return render_template('user_profile.html', username=username)

@app.route('/recipe/<title>')
def recipe_details(title):
    recipe = recipe_manager.get_recipe_details(title)
    return render_template('recipe_details.html', recipe=recipe)

if __name__ == '__main__':
    app.run(port=8171, debug=True)

from flask import Flask, render_template, request, redirect, url_for, flash
from user_manager import UserManager
from recipe_manager import RecipeManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager('users.txt')
recipe_manager = RecipeManager('recipes.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Registration failed. Username may already exist.', 'error')
    return render_template('registration.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/submit_recipe', methods=['GET', 'POST'])
def submit_recipe():
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        if recipe_manager.submit_recipe(title, ingredients, instructions):
            flash('Recipe submitted successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Recipe submission failed.', 'error')
    return render_template('recipe_submission.html')

@app.route('/browse_recipes', methods=['GET', 'POST'])
def browse_recipes():
    if request.method == 'POST':
        keyword = request.form['keyword']
        recipes = recipe_manager.search_recipes(keyword)
        return render_template('recipe_browsing.html', recipes=recipes)
    return render_template('recipe_browsing.html')

@app.route('/recipe/<title>')
def recipe_details(title):
    details = recipe_manager.get_recipe_details(title)
    return render_template('recipe_details.html', details=details)

@app.route('/profile')
def user_profile():
    # Placeholder for user profile logic
    return render_template('user_profile.html')

if __name__ == '__main__':
    app.run(port=8404, debug=False)

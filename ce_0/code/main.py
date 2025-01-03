from flask import Flask, render_template, request, redirect, session, url_for
from user_manager import UserManager
from recipe_manager import RecipeManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Initialize UserManager and RecipeManager
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
            return redirect(url_for('login'))
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
        if recipe_manager.submit_recipe(title, ingredients, instructions):
            return redirect(url_for('home'))
        else:
            error_message = "Recipe submission failed. Title may already exist."
            return render_template('recipe_submission.html', error=error_message)
    return render_template('recipe_submission.html')

@app.route('/recipe_browsing', methods=['GET', 'POST'])
def recipe_browsing():
    recipes = []
    if request.method == 'POST':
        keyword = request.form['keyword']
        recipes = recipe_manager.search_recipes(keyword)
    return render_template('recipe_browsing.html', recipes=recipes)

@app.route('/user_profile', methods=['GET', 'POST'])
def user_profile():
    if request.method == 'POST':
        username = session.get('username')
        if user_manager.delete_account(username):
            session.clear()  # Clear session on account deletion
            return redirect(url_for('login'))
    submitted_recipes = recipe_manager.get_user_recipes(session.get('username', ''))
    return render_template('user_profile.html', submitted_recipes=submitted_recipes)

@app.route('/recipe_details/<title>')
def recipe_details(title):
    recipe = recipe_manager.get_recipe_details(title)
    return render_template('recipe_details.html', recipe=recipe)

if __name__ == '__main__':
    app.run(port=8167, debug=True)

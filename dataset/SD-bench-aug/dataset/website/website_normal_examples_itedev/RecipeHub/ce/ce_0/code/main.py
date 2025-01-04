from flask import Flask, render_template, request, redirect, url_for
from user_manager import UserManager
from recipe_manager import RecipeManager

app = Flask(__name__)

# Initialize UserManager and RecipeManager
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
            return redirect(url_for('user_profile', username=username))
        else:
            return "Login Failed"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        else:
            return "Registration Failed"
    return render_template('register.html')

@app.route('/recipe_submission', methods=['GET', 'POST'])
def recipe_submission():
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients'].split('|')
        instructions = request.form['instructions']
        recipe_manager.submit_recipe(title, ingredients, instructions)
        return redirect(url_for('recipe_browsing'))
    return render_template('recipe_submission.html')

@app.route('/recipe_browsing', methods=['GET', 'POST'])
def recipe_browsing():
    if request.method == 'POST':
        keyword = request.form['keyword']
        recipes = recipe_manager.search_recipes(keyword)
    else:
        recipes = recipe_manager.recipes
    return render_template('recipe_browsing.html', recipes=recipes)

@app.route('/user_profile/<username>', methods=['GET'])
def user_profile(username):
    user_recipes = [recipe for recipe in recipe_manager.recipes if recipe.title in user_manager.users[username].submitted_recipes]
    return render_template('user_profile.html', username=username, recipes=user_recipes)

@app.route('/delete_account/<username>', methods=['POST'])
def delete_account(username):
    user_manager.delete_account(username)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
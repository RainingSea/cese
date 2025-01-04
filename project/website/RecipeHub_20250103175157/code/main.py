from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from recipe_manager import RecipeManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

user_manager = UserManager('users.txt')
recipe_manager = RecipeManager('recipes.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error='Username already exists')
    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/submit_recipe', methods=['GET', 'POST'])
def submit_recipe():
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        recipe = Recipe(title, ingredients, instructions)
        recipe_manager.submit_recipe(recipe)
        return redirect(url_for('home'))
    return render_template('recipe_submission.html')

@app.route('/browse_recipes', methods=['GET', 'POST'])
def browse_recipes():
    recipes = recipe_manager.search_recipes(request.form.get('keyword', ''))
    return render_template('recipe_browsing.html', recipes=recipes)

@app.route('/user_profile')
def user_profile():
    username = session.get('username')
    return render_template('user_profile.html', username=username)

if __name__ == '__main__':
    app.run(debug=False)
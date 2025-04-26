from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from user_manager import UserManager
from recipe_manager import RecipeManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

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
        user_manager.register(username, password)
        return redirect('/')
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
        recipe_manager.submit_recipe(title, ingredients, instructions)
        return redirect('/home')
    return render_template('recipe_submission.html')

@app.route('/browse_recipes', methods=['GET', 'POST'])
def browse_recipes():
    if request.method == 'POST':
        keyword = request.form['keyword']
        recipes = recipe_manager.search_recipes(keyword)
        return render_template('recipe_browsing.html', recipes=recipes)
    return render_template('recipe_browsing.html')

@app.route('/user_profile')
def user_profile():
    return render_template('user_profile.html')

@app.route('/recipe_details/<title>')
def recipe_details(title):
    details = recipe_manager.get_recipe_details(title)
    return render_template('recipe_details.html', details=details)

if __name__ == '__main__':
    app.run(port=8230, debug=False)

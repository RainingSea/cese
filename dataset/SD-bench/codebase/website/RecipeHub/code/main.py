from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from recipe import Recipe

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load data from files
def load_users():
    users = {}
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users[username] = password
    return users

def load_recipes():
    recipes = []
    with open('recipes.txt', 'r') as file:
        for line in file:
            title, ingredients, instructions = line.strip().split('|')
            recipes.append({'title': title, 'ingredients': ingredients, 'instructions': instructions})
    return recipes

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

@app.route('/submit_recipe', methods=['GET', 'POST'])
def submit_recipe():
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        recipe = Recipe()
        recipe.submit_recipe(title, ingredients, instructions)
        return redirect(url_for('home'))
    return render_template('recipe_submission.html')

@app.route('/browse_recipes', methods=['GET'])
def browse_recipes():
    recipes = load_recipes()
    return render_template('recipe_browsing.html', recipes=recipes)

@app.route('/user_profile', methods=['GET', 'POST'])
def user_profile():
    if request.method == 'POST':
        username = session.get('username')
        user = User()
        user.delete_account(username)
        session.pop('username', None)
        return redirect(url_for('login'))
    return render_template('user_profile.html')

if __name__ == '__main__':
    app.run(port=8316, debug=False)

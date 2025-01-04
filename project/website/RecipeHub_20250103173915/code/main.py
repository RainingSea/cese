from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from recipe_manager import RecipeManager
from message_manager import MessageManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager('users.txt')
recipe_manager = RecipeManager('recipes.txt')
message_manager = MessageManager('messages.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_manager.add_user(User(username, password))
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
        recipe_manager.add_recipe(Recipe(title, ingredients, instructions))
        message_manager.log_message("Recipe submitted successfully.")
        return redirect(url_for('home'))
    return render_template('recipe_submission.html')

@app.route('/browse_recipes')
def browse_recipes():
    recipes = recipe_manager.load_recipes()
    return render_template('recipe_browsing.html', recipes=recipes)

@app.route('/user_profile')
def user_profile():
    username = session.get('username')
    user_recipes = recipe_manager.search_recipes(username)
    return render_template('user_profile.html', username=username, recipes=user_recipes)

if __name__ == '__main__':
    app.run(debug=True)
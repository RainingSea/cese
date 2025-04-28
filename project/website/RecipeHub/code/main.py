from flask import Flask, render_template, request, redirect, url_for, session, flash
from user_manager import UserManager
from recipe_manager import RecipeManager
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager()
recipe_manager = RecipeManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username  # Store username in session
        flash('Login successful!')  # Provide feedback
        return redirect(url_for('home'))
    else:
        flash('Invalid credentials. Please try again.')
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        else:
            flash('Username already exists. Please choose another one.')
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
        flash('Recipe submitted successfully!')  # Provide feedback
        return redirect(url_for('home'))
    return render_template('recipe_submission.html')

@app.route('/browse_recipes')
def browse_recipes():
    recipes = recipe_manager.recipes
    return render_template('recipe_browsing.html', recipes=recipes)

@app.route('/user_profile')
def user_profile():
    return render_template('user_profile.html')

if __name__ == '__main__':
    app.run(port=8405, debug=False)

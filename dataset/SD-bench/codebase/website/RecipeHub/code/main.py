from flask import Flask, request, redirect, render_template, session
from user_manager import UserManager
from recipe_manager import RecipeManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'
user_manager = UserManager('users.txt')
recipe_manager = RecipeManager('recipes.txt')

@app.route('/')
def login():
    """Render the login page."""
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect('/')
    return render_template('register.html')

@app.route('/submit_recipe', methods=['GET', 'POST'])
def submit_recipe():
    """Handle recipe submission."""
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        username = session['username']
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        recipe_manager.submit_recipe(username, title, ingredients, instructions)
        return redirect('/browse_recipes')
    return render_template('recipe_submission.html')

@app.route('/browse_recipes')
def browse_recipes():
    """Render the page to browse recipes."""
    recipes = recipe_manager.get_recipes()
    return render_template('recipe_browsing.html', recipes=recipes)

@app.route('/view_recipe/<title>')
def view_recipe(title):
    """Render the details of a specific recipe."""
    recipe = recipe_manager.get_recipe_details(title)
    if not recipe:
        return "Recipe not found", 404
    return render_template('recipe_details.html', recipe=recipe)

@app.route('/profile')
def view_profile():
    """Render the user profile page."""
    if 'username' not in session:
        return redirect('/')
    username = session['username']
    return render_template('user_profile.html', username=username)

@app.route('/delete_account', methods=['POST'])
def delete_account():
    """Handle account deletion."""
    if 'username' not in session:
        return redirect('/')
    username = session['username']
    user_manager.delete_account(username)
    session.pop('username', None)
    return redirect('/')

@app.route('/login', methods=['POST'])
def do_login():
    """Handle user login."""
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect('/browse_recipes')
    return redirect('/')

@app.route('/logout')
def logout():
    """Handle user logout."""
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8691, debug=False)

from flask import Flask, render_template, request, redirect, session, url_for
from user import User
from recipe import Recipe

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = User()
recipe_manager = Recipe()

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
        if recipe_manager.submit_recipe(session['username'], title, ingredients, instructions):
            return redirect(url_for('home'))
    return render_template('recipe_submission.html')

@app.route('/browse_recipes', methods=['GET', 'POST'])
def browse_recipes():
    if request.method == 'POST':
        keyword = request.form['keyword']
        recipes = recipe_manager.search_recipes(keyword)
        return render_template('recipe_browsing.html', recipes=recipes)
    return render_template('recipe_browsing.html', recipes=[])

@app.route('/user_profile')
def user_profile():
    if 'username' in session:
        return render_template('user_profile.html', recipes=recipe_manager.get_user_recipes(session['username']))
    return redirect(url_for('login'))

@app.route('/view_recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    recipe = recipe_manager.get_recipe_by_id(recipe_id)
    return render_template('view_recipe.html', recipe=recipe)

@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'username' in session:
        user_manager.delete_account(session['username'])
        session.pop('username', None)
        return redirect(url_for('login'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8550, debug=False)

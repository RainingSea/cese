from flask import Flask, render_template, request, redirect, url_for
from user_manager import UserManager
from culture_manager import CultureManager

app = Flask(__name__)

user_manager = UserManager()
culture_manager = CultureManager()

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

@app.route('/dashboard', methods=['GET'])
def dashboard():
    culture_facts = culture_manager.get_culture_facts()
    return render_template('dashboard.html', culture_facts=culture_facts)

@app.route('/culture/<culture_name>', methods=['GET'])
def culture_details(culture_name):
    details = culture_manager.get_culture_details(culture_name)
    return render_template('culture_details.html', details=details)

@app.route('/bookmarks', methods=['GET'])
def bookmarks():
    username = request.args.get('username')
    bookmarked_cultures = culture_manager.get_bookmarks(username)
    return render_template('bookmarks.html', bookmarks=bookmarked_cultures)

if __name__ == '__main__':
    app.run(port=8312, debug=False)

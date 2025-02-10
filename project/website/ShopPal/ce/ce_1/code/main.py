from flask import Flask, render_template, request, redirect, session
from user import User
from collection import Collection

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        user.save()
        return redirect('/')
    return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        user_collections = Collection(session['username']).load()
        return render_template('dashboard.html', collections=user_collections)
    return redirect('/')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        # Implement search logic here
        return render_template('search_results.html', query=query)
    return redirect('/')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']
    users = User.load_all()
    for user in users:
        if user.username == username and user.password == password:
            session['username'] = username
            return redirect('/dashboard')
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8693, debug=False)

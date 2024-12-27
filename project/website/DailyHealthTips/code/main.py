from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from tip import Tip
from feedback import Feedback

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = User.load_all()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect(url_for('archive'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        new_user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/archive')
def archive():
    tips = Tip.load_all()
    return render_template('archive.html', tips=tips)

@app.route('/tip/<int:tip_index>')
def tip(tip_index):
    tips = Tip.load_all()
    if 0 <= tip_index < len(tips):
        return render_template('tip.html', tip=tips[tip_index])
    return redirect(url_for('archive'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        tips = Tip.load_all()
        search_results = [tip for tip in tips if query.lower() in tip.content.lower()]
        return render_template('archive.html', tips=search_results)
    return redirect(url_for('archive'))

@app.route('/feedback', methods=['GET', 'POST'])
def submit_feedback():
    if request.method == 'POST':
        username = session.get('username', 'Guest')
        message = request.form['message']
        feedback = Feedback(username, message)
        feedback.save()
        return redirect(url_for('archive'))
    return render_template('feedback.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
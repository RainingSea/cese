from flask import Flask, render_template, request, redirect, url_for, session
from data_handler import DataHandler

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
data_handler = DataHandler()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if data_handler.authenticate_user(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match')
        
        if data_handler.register_user(username, password):
            return redirect(url_for('login'))
        return render_template('register.html', error='Username already exists')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    notes = data_handler.get_notes(session['username'])
    return render_template('dashboard.html', username=session['username'], notes=notes)

@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        data_handler.add_note(session['username'], title, content)
        return redirect(url_for('dashboard'))
    return render_template('add_note.html')

@app.route('/view_note/<note_id>', methods=['GET', 'POST'])
def view_note(note_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    notes = data_handler.get_notes(session['username'])
    note = next((n for n in notes if n['id'] == note_id), None)
    if not note:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        if request.form.get('_method') == 'PUT':
            title = request.form['title']
            content = request.form['content']
            data_handler.update_note(session['username'], note_id, title, content)
            return redirect(url_for('view_note', note_id=note_id))
        elif request.form.get('_method') == 'DELETE':
            data_handler.delete_note(session['username'], note_id)
            return redirect(url_for('dashboard'))
    
    edit_mode = request.args.get('edit') == 'true'
    return render_template('view_note.html', note=note, edit_mode=edit_mode)

@app.route('/search')
def search():
    if 'username' not in session:
        return redirect(url_for('login'))
    query = request.args.get('query', '')
    results = data_handler.search_notes(session['username'], query)
    return render_template('search.html', query=query, results=results)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8095, debug=False)

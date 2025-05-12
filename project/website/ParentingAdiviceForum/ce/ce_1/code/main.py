from flask import Flask, render_template, request, redirect, session
from user_manager import UserManager
from thread_manager import ThreadManager
from contact_manager import ContactManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager('users.txt')
thread_manager = ThreadManager('threads.txt')
contact_manager = ContactManager('contacts.txt')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def handle_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username
            return redirect('/home')
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect('/')
    return render_template('register.html')

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect('/')
    return render_template('home.html')

@app.route('/forum')
def forum():
    if 'username' not in session:
        return redirect('/')
    threads = thread_manager.get_threads()
    return render_template('forum.html', threads=threads)

@app.route('/view_thread/<int:thread_id>', methods=['GET', 'POST'])
def view_thread(thread_id):
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        comment = request.form['comment']
        thread_manager.add_comment(thread_id, comment)
        return redirect(f'/view_thread/{thread_id}')
    thread = thread_manager.get_thread(thread_id)
    return render_template('view_thread.html', thread=thread)

@app.route('/post_advice', methods=['GET', 'POST'])
def post_advice():
    if 'username' not in session:
        return redirect('/')
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        thread_manager.create_thread(title, content)
        return redirect('/forum')
    return render_template('post_advice.html')

@app.route('/my_account')
def my_account():
    if 'username' not in session:
        return redirect('/')
    return render_template('my_account.html')

@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        contact_manager.submit_contact(name, email, message)
        return redirect('/home')
    return render_template('contact_us.html')

if __name__ == '__main__':
    app.run(port=8493, debug=False)

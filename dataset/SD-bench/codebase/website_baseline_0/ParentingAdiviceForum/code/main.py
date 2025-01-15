from flask import Flask, render_template, request, redirect, url_for, session
from file_manager import FileManager
from user import User
from thread import Thread
from comment import Comment
from advice import Advice

app = Flask(__name__)
app.secret_key = 'your_secret_key'
file_manager = FileManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = file_manager.load_users()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect(url_for('home'))
        return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        file_manager.save_user(user)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/forum')
def forum():
    threads = file_manager.load_threads()
    return render_template('forum.html', threads=threads)

@app.route('/create_thread', methods=['GET', 'POST'])
def create_thread():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        thread = Thread(title, content)
        file_manager.save_thread(thread)
        return redirect(url_for('forum'))
    return render_template('create_thread.html')

@app.route('/view_thread/<int:thread_id>', methods=['GET', 'POST'])
def view_thread(thread_id):
    if request.method == 'POST':
        comment_content = request.form['comment']
        comment = Comment(comment_content)
        file_manager.save_comment(thread_id, comment)
        return redirect(url_for('view_thread', thread_id=thread_id))
    
    threads = file_manager.load_threads()
    if 0 <= thread_id < len(threads):
        thread = threads[thread_id]
        comments = file_manager.load_comments(thread_id)
        return render_template('view_thread.html', thread=thread, comments=comments)
    return "Thread not found", 404

@app.route('/post_advice', methods=['GET', 'POST'])
def post_advice():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        advice = Advice(title, content)
        file_manager.save_advice(advice)
        return redirect(url_for('home'))
    return render_template('post_advice.html')

@app.route('/my_account')
def my_account():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('my_account.html')

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

if __name__ == '__main__':
    app.run(port=8546, debug=False)

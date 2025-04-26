from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from user_manager import UserManager
from thread_manager import ThreadManager
from comment_manager import CommentManager
from advice_manager import AdviceManager

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

user_manager = UserManager()
thread_manager = ThreadManager()
comment_manager = CommentManager()
advice_manager = AdviceManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            session['username'] = username  # Store username in session
            return redirect('/home')
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
    advice_posts = advice_manager.get_advice()
    return render_template('home.html', advice_posts=advice_posts)

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        thread_manager.create_thread(title, content)
        return redirect('/forum')
    threads = thread_manager.get_threads()
    return render_template('forum.html', threads=threads)

@app.route('/view_thread/<int:thread_id>', methods=['GET', 'POST'])
def view_thread(thread_id):
    thread = thread_manager.get_thread(thread_id)
    if not thread:
        return "Thread not found", 404  # Improved error handling
    comments = comment_manager.get_comments(thread_id)
    if request.method == 'POST':
        comment = request.form['comment']
        comment_manager.add_comment(thread_id, comment)
        return redirect(f'/view_thread/{thread_id}')
    return render_template('view_thread.html', thread=thread, comments=comments)

@app.route('/post_advice', methods=['GET', 'POST'])
def post_advice():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        advice_manager.post_advice(title, content)
        return redirect('/home')
    return render_template('post_advice.html')

@app.route('/my_account')
def my_account():
    return render_template('my_account.html')

@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # Handle contact form submission
        return redirect('/home')
    return render_template('contact_us.html')

if __name__ == '__main__':
    app.run(port=8217, debug=False)

from flask import Flask, render_template, request, redirect, url_for, session
from user_manager import UserManager
from thread_manager import ThreadManager
from comment_manager import CommentManager
from advice_manager import AdviceManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager()
thread_manager = ThreadManager()
comment_manager = CommentManager()
advice_manager = AdviceManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_manager.register(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/forum')
def forum():
    threads = thread_manager.get_threads()
    return render_template('forum.html', threads=threads)

@app.route('/view_thread/<int:thread_id>')
def view_thread(thread_id):
    thread = thread_manager.get_thread(thread_id)
    comments = comment_manager.get_comments(thread_id)
    return render_template('view_thread.html', thread=thread, comments=comments)

@app.route('/post_advice', methods=['GET', 'POST'])
def post_advice():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        advice_manager.post_advice(title, content)
        return redirect(url_for('home'))
    return render_template('post_advice.html')

@app.route('/my_account')
def my_account():
    return render_template('my_account.html')

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

if __name__ == '__main__':
    app.run(port=8388, debug=False)

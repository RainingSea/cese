from flask import Flask, render_template, request, redirect, url_for
from user_manager import UserManager
from thread_manager import ThreadManager
from comment_manager import CommentManager
from advice_manager import AdviceManager
from contact_manager import ContactManager

app = Flask(__name__)

user_manager = UserManager()
thread_manager = ThreadManager()
comment_manager = CommentManager()
advice_manager = AdviceManager()
contact_manager = ContactManager()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.register(username, password):
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/forum')
def forum():
    threads = thread_manager.get_threads()
    return render_template('forum.html', threads=threads)

@app.route('/thread/<int:thread_id>', methods=['GET', 'POST'])
def view_thread(thread_id):
    if request.method == 'POST':
        comment = request.form['comment']
        comment_manager.add_comment(thread_id, comment)
    thread_details = thread_manager.get_thread_details(thread_id)
    return render_template('view_thread.html', thread=thread_details)

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

@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        contact_manager.submit_inquiry(name, email, message)
        return redirect(url_for('home'))
    return render_template('contact_us.html')

if __name__ == '__main__':
    app.run(port=8214, debug=False)

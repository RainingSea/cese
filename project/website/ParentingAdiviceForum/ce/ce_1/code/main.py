from flask import Flask, request, render_template, redirect, session
from user_manager import UserManager
from thread_manager import ThreadManager
from comment_manager import CommentManager
from contact_inquiry_manager import ContactInquiryManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key
user_manager = UserManager()
thread_manager = ThreadManager()
comment_manager = CommentManager()
contact_inquiry_manager = ContactInquiryManager()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if user_manager.register(username, password):
        return redirect('/')
    return "Registration failed", 400

@app.route('/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']
    if user_manager.login(username, password):
        session['username'] = username
        return redirect('/home')
    return "Login failed", 400

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/forum')
def forum():
    threads = thread_manager.get_threads()
    return render_template('forum.html', threads=threads)

@app.route('/post_advice', methods=['POST'])
def post_advice():
    title = request.form['title']
    content = request.form['content']
    thread_manager.create_thread(title, content)
    return redirect('/forum')

@app.route('/view_thread/<int:thread_id>')
def view_thread(thread_id):
    thread_details = thread_manager.get_thread_details(thread_id)
    comments = comment_manager.get_comments(thread_id)
    return render_template('view_thread.html', thread=thread_details, comments=comments)

@app.route('/add_comment/<int:thread_id>', methods=['POST'])
def add_comment(thread_id):
    comment = request.form['comment']
    comment_manager.add_comment(thread_id, comment)
    return redirect(f'/view_thread/{thread_id}')

@app.route('/contact_us', methods=['POST'])
def contact_us():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    contact_inquiry_manager.submit_inquiry(name, email, message)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8215, debug=False)

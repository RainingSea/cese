from flask import Flask, render_template, request, redirect, session
from user_manager import UserManager
from forum import Forum
from contact_manager import ContactManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

user_manager = UserManager()
forum = Forum()
contact_manager = ContactManager()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login_user(username, password):
            session['username'] = username
            return redirect('/forum')
        return 'Invalid credentials'
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_manager.register_user(username, password)
        return redirect('/login')
    return render_template('register.html')

@app.route('/forum')
def forum_page():
    threads = forum.get_threads()
    return render_template('forum.html', threads=threads)

@app.route('/post_advice', methods=['GET', 'POST'])
def post_advice():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        forum.add_thread(Thread(title, content))
        return redirect('/forum')
    return render_template('post_advice.html')

@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        contact_manager.add_inquiry(ContactInquiry(name, email, message))
        return redirect('/')
    return render_template('contact_us.html')

@app.route('/my_account')
def my_account():
    return render_template('my_account.html')

if __name__ == '__main__':
    app.run(port=8323, debug=False)

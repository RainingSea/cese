from flask import Flask, render_template, request, redirect, session
from user import User, UserManager
from forum import Forum, Thread, Comment, ContactInquiry

app = Flask(__name__)
app.secret_key = 'supersecretkey'

user_manager = UserManager()
forum = Forum()

# Load existing data from files
def load_data():
    with open('users.txt', 'r') as users_file:
        for line in users_file:
            username, password = line.strip().split('|')
            user_manager.add_user(User(username, password))
    
    with open('threads.txt', 'r') as threads_file:
        for line in threads_file:
            title, content = line.strip().split('|')
            forum.add_thread(Thread(title, content))

    with open('comments.txt', 'r') as comments_file:
        for line in comments_file:
            title, content = line.strip().split('|')
            thread = forum.get_thread(title)
            if thread:
                thread.add_comment(Comment(content))

load_data()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = user_manager.get_user(username)
        if user and user.password == password:
            session['username'] = username
            return redirect('/home')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        user_manager.add_user(user)
        with open('users.txt', 'a') as users_file:
            users_file.write(f"{username}|{password}\n")
        return redirect('/')
    return render_template('register.html')

@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/forum', methods=['GET', 'POST'])
def forum_page():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        thread = Thread(title, content)
        forum.add_thread(thread)
        with open('threads.txt', 'a') as threads_file:
            threads_file.write(f"{title}|{content}\n")
        return redirect('/forum')
    threads = forum.list_threads()
    return render_template('forum.html', threads=threads)

@app.route('/forum/<title>', methods=['GET', 'POST'])
def view_thread(title):
    thread = forum.get_thread(title)
    if request.method == 'POST':
        comment_content = request.form['comment']
        comment = Comment(comment_content)
        thread.add_comment(comment)
        with open('comments.txt', 'a') as comments_file:
            comments_file.write(f"{title}|{comment_content}\n")
        return redirect(f'/forum/{title}')
    return render_template('view_thread.html', thread=thread)

@app.route('/post_advice', methods=['GET', 'POST'])
def post_advice():
    if request.method == 'POST':
        advice_content = request.form['advice']
        # Logic to save advice can be implemented here
        return redirect('/home')
    return render_template('post_advice.html')

@app.route('/my_account', methods=['GET'])
def my_account():
    return render_template('my_account.html')

@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        inquiry = ContactInquiry(name, email, message)
        with open('contact_inquiries.txt', 'a') as inquiries_file:
            inquiries_file.write(f"{name}|{email}|{message}\n")
        return redirect('/home')
    return render_template('contact_us.html')

if __name__ == '__main__':
    app.run(port=8973, debug=False)

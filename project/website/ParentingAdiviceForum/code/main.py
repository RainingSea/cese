from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Load data from text files
def load_users():
    users = []
    with open('users.txt', 'r') as file:
        for line in file:
            username, password, entries = line.strip().split('|')
            users.append({'username': username, 'password': password, 'entries': entries.split(',')})
    return users

def load_threads():
    threads = []
    with open('threads.txt', 'r') as file:
        for line in file:
            title, content, author = line.strip().split('|')
            threads.append({'title': title, 'content': content, 'author': author})
    return threads

def load_comments():
    comments = []
    with open('comments.txt', 'r') as file:
        for line in file:
            thread_id, content, author = line.strip().split('|')
            comments.append({'thread_id': int(thread_id), 'content': content, 'author': author})
    return comments

# Save user data
def save_users(users):
    with open('users.txt', 'w') as file:
        for user in users:
            file.write(f"{user['username']}|{user['password']}|{','.join(user['entries'])}\n")

# Routes
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        for user in users:
            if user['username'] == username and user['password'] == password:
                session['username'] = username
                return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}|\n")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = session.get('username', 'Anonymous')
        with open('threads.txt', 'a') as file:
            file.write(f"{title}|{content}|{author}\n")
        return redirect(url_for('forum'))
    
    threads = load_threads()
    return render_template('forum.html', threads=threads)

@app.route('/view_thread/<int:thread_id>', methods=['GET', 'POST'])
def view_thread(thread_id):
    threads = load_threads()
    comments = load_comments()
    thread = threads[thread_id]
    thread_comments = [comment for comment in comments if comment['thread_id'] == thread_id]
    
    if request.method == 'POST':
        comment_content = request.form['comment']
        author = session.get('username', 'Anonymous')
        with open('comments.txt', 'a') as file:
            file.write(f"{thread_id}|{comment_content}|{author}\n")
        return redirect(url_for('view_thread', thread_id=thread_id))

    return render_template('view_thread.html', thread=thread, comments=thread_comments)

@app.route('/post_advice', methods=['GET', 'POST'])
def post_advice():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        with open('advice.txt', 'a') as file:
            file.write(f"{title}|{content}\n")
        return redirect(url_for('home'))
    return render_template('post_advice.html')

@app.route('/my_account', methods=['GET', 'POST'])
def my_account():
    users = load_users()
    current_user = session.get('username')
    user_data = next((user for user in users if user['username'] == current_user), None)

    if request.method == 'POST':
        if 'delete' in request.form:
            users.remove(user_data)
            save_users(users)
            session.pop('username', None)
            return redirect(url_for('login'))
        else:
            new_password = request.form['password']
            user_data['password'] = new_password
            save_users(users)
            return redirect(url_for('home'))

    return render_template('my_account.html', user=user_data)

@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        with open('contact_inquiries.txt', 'a') as file:
            file.write(f"{name}|{email}|{message}\n")
        return redirect(url_for('home'))
    return render_template('contact_us.html')

if __name__ == '__main__':
    app.run(port=8172, debug=True)

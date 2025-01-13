from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load users from users.txt
def load_users():
    users = {}
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as f:
            for line in f:
                username, password = line.strip().split('|')
                users[username] = password
    return users

# Load threads from threads.txt
def load_threads():
    threads = []
    if os.path.exists('threads.txt'):
        with open('threads.txt', 'r') as f:
            for line in f:
                title, content, comments = line.strip().split('|')
                comments = comments.split(';') if comments else []
                threads.append(Thread(title, content, comments))
    return threads

# Load advice from advice.txt
def load_advice():
    advice_list = []
    if os.path.exists('advice.txt'):
        with open('advice.txt', 'r') as f:
            for line in f:
                title, content = line.strip().split('|')
                advice_list.append(Advice(title, content))
    return advice_list

# Load contact inquiries from contact_inquiries.txt
def load_contact_inquiries():
    inquiries = []
    if os.path.exists('contact_inquiries.txt'):
        with open('contact_inquiries.txt', 'r') as f:
            for line in f:
                name, email, message = line.strip().split('|')
                inquiries.append(ContactInquiry(name, email, message))
    return inquiries

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with open('users.txt', 'a') as f:
            f.write(f"{username}|{password}\n")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/forum')
def forum():
    threads = load_threads()
    return render_template('forum.html', threads=threads)

@app.route('/view_thread/<int:thread_id>')
def view_thread(thread_id):
    threads = load_threads()
    thread = threads[thread_id]
    return render_template('view_thread.html', thread=thread)

@app.route('/post_advice', methods=['GET', 'POST'])
def post_advice():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        advice = Advice(title, content)
        advice.save()
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
        inquiry = ContactInquiry(name, email, message)
        inquiry.save()
        return redirect(url_for('home'))
    return render_template('contact_us.html')

if __name__ == '__main__':
    app.run(port=8475, debug=False)

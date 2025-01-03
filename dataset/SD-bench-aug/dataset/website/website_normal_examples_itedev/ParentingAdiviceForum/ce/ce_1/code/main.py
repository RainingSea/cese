from flask import Flask, render_template, request, redirect, url_for
from user import User
from thread import Thread
from comment import Comment
from advice import Advice
from contact_inquiry import ContactInquiry

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/forum')
def forum():
    threads = load_threads()
    return render_template('forum.html', threads=threads)

@app.route('/post_advice', methods=['GET', 'POST'])
def post_advice():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        advice = Advice(title, content)
        advice.save()
        return redirect(url_for('forum'))
    return render_template('post_advice.html')

@app.route('/view_thread/<int:thread_id>', methods=['GET', 'POST'])
def view_thread(thread_id):
    thread = load_thread(thread_id)
    comments = load_comments(thread_id)
    if request.method == 'POST':
        comment_content = request.form['comment']
        comment = Comment(thread_id, comment_content)
        comment.save()
        return redirect(url_for('view_thread', thread_id=thread_id))
    return render_template('view_thread.html', thread=thread, comments=comments)

@app.route('/my_account', methods=['GET', 'POST'])
def my_account():
    users = load_users()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        action = request.form['action']
        
        if action == 'update':
            user = User(username, password)
            user.save()
            return redirect(url_for('my_account'))
        elif action == 'delete':
            user = User(username, password)
            user.delete()
            return redirect(url_for('home'))
    
    return render_template('my_account.html', users=users)

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

def load_threads():
    threads = []
    with open('threads.txt', 'r') as file:
        for line in file:
            title, content = line.strip().split('|')
            threads.append(Thread(title, content))
    return threads

def load_thread(thread_id):
    with open('threads.txt', 'r') as file:
        lines = file.readlines()
        title, content = lines[thread_id].strip().split('|')
        return Thread(title, content)

def load_comments(thread_id):
    comments = []
    with open('comments.txt', 'r') as file:
        for line in file:
            if line.startswith(str(thread_id)):
                _, content = line.strip().split('|')
                comments.append(Comment(thread_id, content))
    return comments

def load_users():
    users = []
    with open('users.txt', 'r') as file:
        for line in file:
            username, password = line.strip().split('|')
            users.append(User(username, password))
    return users

if __name__ == '__main__':
    app.run(debug=True)
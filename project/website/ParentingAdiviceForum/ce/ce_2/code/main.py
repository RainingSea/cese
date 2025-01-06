from flask import Flask, render_template, request, redirect, url_for
from user import User
from thread import Thread
from advice import Advice
from contact_inquiry import ContactInquiry

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        user.save()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        thread = Thread(title, content)
        thread.save()
        return redirect(url_for('forum'))
    return render_template('forum.html')

@app.route('/thread/<int:thread_id>', methods=['GET', 'POST'])
def view_thread(thread_id):
    if request.method == 'POST':
        comment_content = request.form['comment']
        thread = Thread.load(thread_id)
        thread.add_comment(comment_content)
        thread.save()
        return redirect(url_for('view_thread', thread_id=thread_id))
    thread = Thread.load(thread_id)
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
    app.run(port=8184, debug=False)

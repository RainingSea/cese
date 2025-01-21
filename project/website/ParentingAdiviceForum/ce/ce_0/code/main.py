from flask import Flask, render_template, request, redirect, url_for, session
from data_storage import DataStorage
from models import User, Thread, Comment, Advice, ContactInquiry

app = Flask(__name__)
app.secret_key = 'your_secret_key'
data_storage = DataStorage()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        data_storage.save_user(user)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/forum')
def forum():
    threads = data_storage.load_threads()
    return render_template('forum.html', threads=threads)

@app.route('/view_thread/<title>')
def view_thread(title):
    thread = next((t for t in data_storage.load_threads() if t.title == title), None)
    comments = data_storage.load_comments(title)
    return render_template('view_thread.html', thread=thread, comments=comments)

@app.route('/post_advice', methods=['GET', 'POST'])
def post_advice():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        advice = Advice(title, content)
        data_storage.save_advice(advice)
        return redirect(url_for('forum'))
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
        data_storage.save_contact_inquiry(inquiry)
        return redirect(url_for('home'))
    return render_template('contact_us.html')

if __name__ == '__main__':
    app.run(port=8968, debug=False)

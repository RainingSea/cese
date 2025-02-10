from flask import Flask, render_template, request, redirect, url_for, session
from file_manager import FileManager
from user import User
from thread import Thread
from contact_inquiry import ContactInquiry

app = Flask(__name__)
app.secret_key = 'supersecretkey'
file_manager = FileManager()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = file_manager.load_users()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect(url_for('forum'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username, password)
        file_manager.save_user(new_user)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/forum')
def forum():
    threads = file_manager.load_threads()
    return render_template('forum.html', threads=threads)

@app.route('/thread/<int:thread_id>', methods=['GET', 'POST'])
def view_thread(thread_id):
    threads = file_manager.load_threads()
    thread = threads[thread_id]
    if request.method == 'POST':
        comment = request.form['comment']
        thread.add_comment(comment)
        file_manager.save_thread(thread)
        return redirect(url_for('view_thread', thread_id=thread_id))
    return render_template('view_thread.html', thread=thread)

@app.route('/post_advice', methods=['GET', 'POST'])
def post_advice():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_thread = Thread(title, content)
        file_manager.save_thread(new_thread)
        return redirect(url_for('forum'))
    return render_template('post_advice.html')

@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        inquiry = ContactInquiry(name, email, message)
        file_manager.save_contact_inquiry(inquiry)
        return redirect(url_for('home'))
    return render_template('contact_us.html')

if __name__ == '__main__':
    app.run(port=8565, debug=False)

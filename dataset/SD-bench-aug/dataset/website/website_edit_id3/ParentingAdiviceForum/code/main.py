from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from thread import Thread
from comment import Comment
from advice import Advice

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

def init_routes():
    @app.route('/')
    def login():
        return render_template('login.html')

    @app.route('/login', methods=['POST'])
    def do_login():
        username = request.form['username']
        password = request.form['password']
        users = User.load_all()
        for user in users:
            if user.username == username and user.password == password:
                session['username'] = username
                return redirect(url_for('home'))
        return redirect(url_for('login'))  # Redirect back to login on failure

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            new_user = User(username, password)
            new_user.save()
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
            new_thread = Thread(title, content)
            new_thread.save()
            return redirect(url_for('forum'))
        
        threads = Thread.load_all()
        return render_template('forum.html', threads=threads)

    @app.route('/view_thread/<int:thread_id>', methods=['GET', 'POST'])
    def view_thread(thread_id):
        if request.method == 'POST':
            content = request.form['content']
            new_comment = Comment(thread_id, content)
            new_comment.save()
            return redirect(url_for('view_thread', thread_id=thread_id))

        thread = Thread.load_all()[thread_id]
        comments = Comment.load_all(thread_id)
        return render_template('view_thread.html', thread=thread, comments=comments)

    @app.route('/post_advice', methods=['GET', 'POST'])
    def post_advice():
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            new_advice = Advice(title, content)
            new_advice.save()
            return redirect(url_for('home'))
        return render_template('post_advice.html')

    @app.route('/my_account', methods=['GET', 'POST'])
    def my_account():
        if request.method == 'POST':
            # Logic to update user profile or delete account
            # For simplicity, we will just redirect to home for now
            return redirect(url_for('home'))
        return render_template('my_account.html')

    @app.route('/contact_us', methods=['GET', 'POST'])
    def contact_us():
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            message = request.form['message']
            # Here you would typically send the message to an admin or save it
            # For now, we will just redirect to home
            return redirect(url_for('home'))
        return render_template('contact_us.html')

if __name__ == '__main__':
    init_routes()
    app.run(port=8138, debug=True)

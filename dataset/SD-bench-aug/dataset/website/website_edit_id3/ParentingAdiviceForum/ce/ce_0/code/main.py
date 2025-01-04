from flask import Flask, render_template, request, redirect, url_for, session
from user import User
from thread import Thread
from comment import Comment
from advice import Advice

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

def init_routes():
    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User(username, password)
            if user.login():
                session['username'] = username
                return redirect(url_for('forum'))
            return "Invalid credentials"
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

    @app.route('/forum', methods=['GET', 'POST'])
    def forum():
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            thread = Thread(title, content)
            thread.save()
            return redirect(url_for('forum'))
        
        threads = Thread.load_all()
        return render_template('forum.html', threads=threads)

    @app.route('/view_thread/<int:thread_id>', methods=['GET', 'POST'])
    def view_thread(thread_id):
        thread = Thread.load(thread_id)
        comments = Comment.load_all(thread_id)
        if request.method == 'POST':
            comment_content = request.form['comment']
            comment = Comment(thread_id, comment_content)
            comment.save()
            return redirect(url_for('view_thread', thread_id=thread_id))
        return render_template('view_thread.html', thread=thread, comments=comments)

    @app.route('/post_advice', methods=['GET', 'POST'])
    def post_advice():
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            advice = Advice(title, content)
            advice.save()
            return redirect(url_for('home'))
        return render_template('post_advice.html')

    @app.route('/my_account', methods=['GET', 'POST'])
    def my_account():
        if request.method == 'POST':
            # Logic to update user profile can be added here
            return "Profile updated!"
        return render_template('my_account.html')

    @app.route('/contact_us', methods=['GET', 'POST'])
    def contact_us():
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            message = request.form['message']
            # Here you can implement logic to save the inquiry or send an email
            return "Thank you for your inquiry!"
        return render_template('contact_us.html')

if __name__ == '__main__':
    init_routes()
    app.run(port=8137, debug=True)

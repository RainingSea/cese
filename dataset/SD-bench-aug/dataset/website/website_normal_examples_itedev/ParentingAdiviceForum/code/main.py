from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Load data from text files
def load_data(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, 'r') as file:
        return [line.strip().split('|') for line in file.readlines()]

# Save user data to text file
def save_user_data(users):
    with open('users.txt', 'w') as file:
        for user in users:
            file.write(f"{user[0]}|{user[1]}\n")

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Forum route
@app.route('/forum')
def forum():
    threads = load_data('threads.txt')
    return render_template('forum.html', threads=threads)

# View Thread route
@app.route('/view_thread/<int:thread_id>', methods=['GET', 'POST'])
def view_thread(thread_id):
    threads = load_data('threads.txt')
    comments = load_data('comments.txt')
    if thread_id <= len(threads):
        thread = threads[thread_id - 1]
        thread_comments = [comment for comment in comments if int(comment[0]) == thread_id]
        
        if request.method == 'POST':
            comment_content = request.form['comment']
            with open('comments.txt', 'a') as file:
                file.write(f"{thread_id}|{comment_content}\n")
            return redirect(url_for('view_thread', thread_id=thread_id))
        
        return render_template('view_thread.html', thread=thread, comments=thread_comments)
    return redirect(url_for('forum'))

# Post Advice route
@app.route('/post_advice', methods=['GET', 'POST'])
def post_advice():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        with open('advice.txt', 'a') as file:
            file.write(f"{title}|{content}\n")
        return redirect(url_for('home'))
    return render_template('post_advice.html')

# My Account route
@app.route('/my_account', methods=['GET', 'POST'])
def my_account():
    users = load_data('users.txt')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for user in users:
            if user[0] == username:
                user[1] = password  # Update password
                save_user_data(users)
                return redirect(url_for('home'))
    return render_template('my_account.html')

# Contact Us route
@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        with open('contact_inquiries.txt', 'a') as file:
            file.write(f"{name}|{email}|{message}\n")
        return render_template('contact_us.html', confirmation=True)
    return render_template('contact_us.html')

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Load data from text files
def load_data(filename):
    with open(filename, 'r') as file:
        return file.readlines()

# Save data to text files
def save_data(filename, data):
    with open(filename, 'a') as file:
        file.write(f"{data}\n")

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Forum route
@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        save_data('threads.txt', f"{title}|{content}")
        return redirect(url_for('forum'))
    
    threads = load_data('threads.txt')
    return render_template('forum.html', threads=threads)

# View Thread route
@app.route('/thread/<int:thread_id>', methods=['GET', 'POST'])
def view_thread(thread_id):
    threads = load_data('threads.txt')
    comments = load_data('comments.txt')
    thread = threads[thread_id].strip().split('|')
    
    if request.method == 'POST':
        comment_content = request.form['comment']
        save_data('comments.txt', f"{thread_id}|{comment_content}")
        return redirect(url_for('view_thread', thread_id=thread_id))
    
    thread_comments = [comment.strip() for comment in comments if comment.startswith(str(thread_id))]
    return render_template('view_thread.html', thread=thread, comments=thread_comments)

# Post Advice route
@app.route('/post_advice', methods=['GET', 'POST'])
def post_advice():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        save_data('advice.txt', f"{title}|{content}")
        return redirect(url_for('home'))
    return render_template('post_advice.html')

# My Account route
@app.route('/my_account', methods=['GET', 'POST'])
def my_account():
    users = load_data('users.txt')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        action = request.form['action']
        
        if action == 'update':
            # Update user information (for simplicity, we just overwrite the file)
            save_data('users.txt', f"{username}|{password}")
        elif action == 'delete':
            # Delete user account (for simplicity, we just clear the file)
            open('users.txt', 'w').close()
        
        return redirect(url_for('home'))
    
    return render_template('my_account.html', users=users)

# Contact Us route
@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        save_data('contact_inquiries.txt', f"{name}|{email}|{message}")
        return redirect(url_for('home'))
    return render_template('contact_us.html')

if __name__ == '__main__':
    app.run(debug=True)
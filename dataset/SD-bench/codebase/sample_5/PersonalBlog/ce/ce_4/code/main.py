from flask import Flask, render_template, request, redirect, session
from user import User
from blog_post import BlogPost

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a real secret key

# Load users and posts from files
def load_users():
    users = {}
    with open('users.txt', 'r') as file:
        for line in file:
            username, password, email = line.strip().split(':')
            users[username] = User(username, password, email)
    return users

def load_posts():
    posts = []
    with open('posts.txt', 'r') as file:
        for line in file:
            username, post_id, title, content = line.strip().split(':')
            posts.append(BlogPost(username, int(post_id), title, content))
    return posts

users = load_users()
posts = load_posts()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user = User(username, password, email)
        if user.register(username, password, email):
            with open('users.txt', 'a') as file:
                file.write(f"{username}:{password}:{email}\n")
            return redirect('/')
    return render_template('registration.html')

@app.route('/main_blog')
def main_blog():
    return render_template('main_blog.html', posts=posts)

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        post_id = len(posts) + 1
        username = session.get('username')
        blog_post = BlogPost(username, post_id, title, content)
        if blog_post.create_post(username, title, content):
            posts.append(blog_post)
            with open('posts.txt', 'a') as file:
                file.write(f"{username}:{post_id}:{title}:{content}\n")
            return redirect('/main_blog')
    return render_template('new_post.html')

@app.route('/view_post/<int:post_id>')
def view_post(post_id):
    post = next((p for p in posts if p.post_id == post_id), None)
    return render_template('view_post.html', post=post)

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = next((p for p in posts if p.post_id == post_id), None)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        # Update the posts.txt file
        with open('posts.txt', 'w') as file:
            for p in posts:
                file.write(f"{p.username}:{p.post_id}:{p.title}:{p.content}\n")
        return redirect('/view_post/{}'.format(post_id))
    return render_template('edit_post.html', post=post)

@app.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    global posts
    posts = [p for p in posts if p.post_id != post_id]
    with open('posts.txt', 'w') as file:
        for p in posts:
            file.write(f"{p.username}:{p.post_id}:{p.title}:{p.content}\n")
    return redirect('/main_blog')

if __name__ == '__main__':
    app.run(port=8481, debug=False)

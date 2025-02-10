from flask import Flask, request, redirect, url_for, session
from auth import Auth
from views import View
from models import BlogPost

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this in production

@app.route('/')
def login():
    return View.render_login()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if Auth.register(username, password, email):
            return redirect(url_for('login'))
    return View.render_registration()

@app.route('/main', methods=['GET'])
def main():
    posts = BlogPost.load_posts()
    return View.render_main(posts)

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        post = BlogPost(title, content, author)
        post.save()
        return redirect(url_for('main'))
    return View.render_new_post()

@app.route('/view_post/<string:title>', methods=['GET'])
def view_post(title):
    posts = BlogPost.load_posts()
    post = next((p for p in posts if p['title'] == title), None)
    if post:
        return View.render_view_post(BlogPost(post['title'], post['content'], post['author']))
    return redirect(url_for('main'))

@app.route('/edit_post/<string:title>', methods=['GET', 'POST'])
def edit_post(title):
    posts = BlogPost.load_posts()
    post = next((p for p in posts if p['title'] == title), None)
    if request.method == 'POST':
        new_title = request.form['title']
        new_content = request.form['content']
        post_obj = BlogPost(post['title'], post['content'], post['author'])
        post_obj.update(new_title, new_content)
        return redirect(url_for('main'))
    if post:
        return View.render_edit_post(BlogPost(post['title'], post['content'], post['author']))
    return redirect(url_for('main'))

if __name__ == '__main__':
    app.run(port=8568, debug=False)

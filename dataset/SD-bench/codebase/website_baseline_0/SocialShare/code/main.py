from flask import Flask, render_template, request, redirect, url_for, session, flash
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username, password, bio=''):
        self.username = username
        self.password = password
        self.bio = bio
        self.following = []

    def follow(self, user):
        if user not in self.following:
            self.following.append(user)

    def unfollow(self, user):
        if user in self.following:
            self.following.remove(user)

    def update_bio(self, new_bio):
        self.bio = new_bio

class Article:
    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        self.author = author
        self.likes = 0
        self.comments = []

    def like(self):
        self.likes += 1

    def comment(self, content, user):
        comment = Comment(content, user, self)
        self.comments.append(comment)
        return comment

class Comment:
    def __init__(self, content, author, article):
        self.content = content
        self.author = author
        self.article = article

class SocialShare:
    def __init__(self):
        self.users = self.load_users()
        self.articles = self.load_articles()

    def load_users(self):
        users = []
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password, bio = line.strip().split('|')
                    users.append(User(username, password, bio))
        except FileNotFoundError:
            pass
        return users

    def load_articles(self):
        articles = []
        try:
            with open('articles.txt', 'r') as file:
                for line in file:
                    title, content, author = line.strip().split('|')
                    articles.append(Article(title, content, author))
        except FileNotFoundError:
            pass
        return articles

    def register(self, username, password):
        if any(user.username == username for user in self.users):
            return None  # Username already exists
        new_user = User(username, password)
        self.users.append(new_user)
        self.save_users()
        return new_user

    def login(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                return user
        return None

    def share_article(self, title, content, author):
        new_article = Article(title, content, author.username)
        self.articles.append(new_article)
        self.save_articles()
        return new_article

    def get_feed(self):
        return self.articles

    def save_users(self):
        with open('users.txt', 'w') as file:
            for user in self.users:
                file.write(f"{user.username}|{user.password}|{user.bio}\n")

    def save_articles(self):
        with open('articles.txt', 'w') as file:
            for article in self.articles:
                file.write(f"{article.title}|{article.content}|{article.author}\n")

social_share = SocialShare()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = social_share.login(username, password)
        if user:
            session['username'] = user.username
            return redirect(url_for('profile'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = social_share.register(username, password)
        if user:
            return redirect(url_for('login'))
        else:
            flash('Username already exists. Please choose a different one.', 'error')
    return render_template('register.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    username = session.get('username')
    user = next((u for u in social_share.users if u.username == username), None)
    if request.method == 'POST':
        new_bio = request.form['bio']
        if user:
            user.update_bio(new_bio)
            social_share.save_users()  # Save updated user info
    return render_template('profile.html', username=username, following=user.following)

@app.route('/feed', methods=['GET', 'POST'])
def feed():
    articles = social_share.get_feed()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = next((u for u in social_share.users if u.username == session.get('username')), None)
        if author:
            social_share.share_article(title, content, author)
            return redirect(url_for('feed'))
    return render_template('feed.html', articles=articles)

@app.route('/like/<article_title>', methods=['POST'])
def like_article(article_title):
    article = next((a for a in social_share.articles if a.title == article_title), None)
    if article:
        article.like()
        social_share.save_articles()
    return redirect(url_for('feed'))

@app.route('/comment/<article_title>', methods=['POST'])
def comment_article(article_title):
    content = request.form['content']
    article = next((a for a in social_share.articles if a.title == article_title), None)
    user = next((u for u in social_share.users if u.username == session.get('username')), None)
    if article and user:
        article.comment(content, user)
        social_share.save_articles()
    return redirect(url_for('feed'))

@app.route('/follow/<username>', methods=['POST'])
def follow_user(username):
    current_user = next((u for u in social_share.users if u.username == session.get('username')), None)
    user_to_follow = next((u for u in social_share.users if u.username == username), None)
    if current_user and user_to_follow:
        current_user.follow(user_to_follow)
        social_share.save_users()
    return redirect(url_for('profile'))

@app.route('/unfollow/<username>', methods=['POST'])
def unfollow_user(username):
    current_user = next((u for u in social_share.users if u.username == session.get('username')), None)
    user_to_unfollow = next((u for u in social_share.users if u.username == username), None)
    if current_user and user_to_unfollow:
        current_user.unfollow(user_to_unfollow)
        social_share.save_users()
    return redirect(url_for('profile'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=8554, debug=False)

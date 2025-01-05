from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}\n")

    def delete(self):
        pass  # Not implemented

class Thread:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content
        self.comments = []

    def save(self):
        with open('threads.txt', 'a') as f:
            f.write(f"{self.title}|{self.content}\n")

    def add_comment(self, comment: str):
        self.comments.append(comment)
        with open('comments.txt', 'a') as f:
            f.write(f"{self.title}|{comment}\n")

class Comment:
    def __init__(self, content: str):
        self.content = content

class ContactInquiry:
    def __init__(self, name: str, email: str, message: str):
        self.name = name
        self.email = email
        self.message = message

    def save(self):
        with open('contact_inquiries.txt', 'a') as f:
            f.write(f"{self.name}|{self.email}|{self.message}\n")

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with open('users.txt', 'r') as f:
            users = f.readlines()
            for user in users:
                user_data = user.strip().split('|')
                if user_data[0] == username and user_data[1] == password:
                    session['username'] = username
                    return redirect(url_for('home'))
        return "Invalid credentials", 401
    return render_template('login.html')

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
    return render_template('forum.html')

@app.route('/view_thread/<title>', methods=['GET', 'POST'])
def view_thread(title):
    if request.method == 'POST':
        comment_content = request.form['comment']
        thread = Thread(title, "")
        thread.add_comment(comment_content)
        return redirect(url_for('view_thread', title=title))
    return render_template('view_thread.html', title=title)

@app.route('/post_advice', methods=['GET', 'POST'])
def post_advice():
    if request.method == 'POST':
        advice_content = request.form['advice']
        # Logic to save advice
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
    app.run(port=8105, debug=False)

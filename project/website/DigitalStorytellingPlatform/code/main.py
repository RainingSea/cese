from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

class UserManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.load_users()

    def load_users(self):
        """Load users from the specified file."""
        self.users = {}
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    username, password, email = line.strip().split('|')
                    self.users[username] = (password, email)

    def register(self, username: str, password: str, email: str) -> bool:
        """Register a new user if the username does not already exist."""
        if username in self.users:
            return False
        self.users[username] = (password, email)
        with open(self.filename, 'a') as file:
            file.write(f"{username}|{password}|{email}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        """Check if the username and password match."""
        return username in self.users and self.users[username][0] == password

class StoryManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.load_stories()

    def load_stories(self):
        """Load stories from the specified file."""
        self.stories = []
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    title, content = line.strip().split('|', 1)
                    self.stories.append((title, content))

    def create_story(self, title: str, content: str) -> bool:
        """Create a new story and save it to the file."""
        self.stories.append((title, content))
        with open(self.filename, 'a') as file:
            file.write(f"{title}|{content}\n")
        return True

    def edit_story(self, title: str, content: str) -> bool:
        """Edit an existing story."""
        for index, (t, c) in enumerate(self.stories):
            if t == title:
                self.stories[index] = (title, content)
                self.save_stories()
                return True
        return False

    def save_stories(self):
        """Save all stories back to the file."""
        with open(self.filename, 'w') as file:
            for title, content in self.stories:
                file.write(f"{title}|{content}\n")

    def get_all_stories(self) -> list:
        """Return all stories."""
        return self.stories

user_manager = UserManager('users.txt')
story_manager = StoryManager('stories.txt')

@app.route('/', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if user_manager.login(username, password):
            flash('Login successful!')
            return redirect(url_for('story_list'))  # Redirect to story list after login
        else:
            flash('Login failed. Please check your credentials.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if user_manager.register(username, password, email):
            flash('Registration successful!')
            return redirect(url_for('login'))
        else:
            flash('Username already exists. Please choose another.')
    return render_template('register.html')

@app.route('/story_creation', methods=['GET', 'POST'])
def story_creation():
    """Handle story creation."""
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        story_manager.create_story(title, content)
        flash('Story saved successfully!')
        return redirect(url_for('story_list'))  # Redirect to story list after saving
    return render_template('story_creation.html')

@app.route('/story_list', methods=['GET'])
def story_list():
    """Display all stories."""
    stories = story_manager.get_all_stories()
    return render_template('story_list.html', stories=stories)

@app.route('/edit_story/<string:title>', methods=['GET', 'POST'])
def edit_story(title):
    """Handle story editing."""
    if request.method == 'POST':
        content = request.form['content']
        if story_manager.edit_story(title, content):
            flash('Story updated successfully!')
            return redirect(url_for('story_list'))
        else:
            flash('Error updating story.')
    else:
        # Load existing content for editing
        for t, c in story_manager.get_all_stories():
            if t == title:
                return render_template('edit_story.html', title=t, content=c)
    return redirect(url_for('story_list'))

if __name__ == '__main__':
    app.run(port=8326, debug=False)

import os

class Main:
    def __init__(self):
        self.user_manager = UserManager('users.txt')
        self.post_manager = PostManager('posts.txt')

    def main(self):
        # Simulate routing logic for demonstration
        return self.user_manager.login("admin", "admin123")  # Example login

class UserManager:
    def __init__(self, user_file: str):
        self.user_file = user_file
        self.load_users()

    def load_users(self):
        self.users = {}
        if os.path.exists(self.user_file):
            with open(self.user_file, 'r') as file:
                for line in file:
                    username, password, email = line.strip().split(',')
                    self.users[username] = (password, email)

    def register(self, username: str, password: str, email: str) -> bool:
        if username in self.users:
            return False
        with open(self.user_file, 'a') as file:
            file.write(f"{username},{password},{email}\n")
        self.users[username] = (password, email)
        return True

    def login(self, username: str, password: str) -> bool:
        if username in self.users and self.users[username][0] == password:
            return True
        return False

class PostManager:
    def __init__(self, post_file: str):
        self.post_file = post_file
        self.load_posts()

    def load_posts(self):
        self.posts = []
        if os.path.exists(self.post_file):
            with open(self.post_file, 'r') as file:
                for line in file:
                    username, title, content = line.strip().split(',', 2)
                    self.posts.append((username, title, content))

    def create_post(self, username: str, title: str, content: str) -> bool:
        with open(self.post_file, 'a') as file:
            file.write(f"{username},{title},{content}\n")
        self.posts.append((username, title, content))
        return True

    def edit_post(self, title: str, content: str) -> bool:
        for index, (username, post_title, _) in enumerate(self.posts):
            if post_title == title:
                self.posts[index] = (username, title, content)
                self.save_posts()
                return True
        return False

    def delete_post(self, title: str) -> bool:
        for index, (username, post_title, _) in enumerate(self.posts):
            if post_title == title:
                del self.posts[index]
                self.save_posts()
                return True
        return False

    def get_posts(self, username: str):
        return [post for post in self.posts if post[0] == username]

    def get_post(self, title: str):
        for post in self.posts:
            if post[1] == title:
                return post
        return None

    def save_posts(self):
        with open(self.post_file, 'w') as file:
            for username, title, content in self.posts:
                file.write(f"{username},{title},{content}\n")

if __name__ == "__main__":
    app = Main()
    app.main()
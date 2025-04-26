import os

class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def register(self, username: str, password: str, email: str) -> bool:
        if not self._is_username_taken(username):
            with open('users.txt', 'a') as f:
                f.write(f"{username}|{password}|{email}\n")
            return True
        return False

    def login(self, username: str, password: str) -> bool:
        with open('users.txt', 'r') as f:
            for line in f:
                user_data = line.strip().split('|')
                if user_data[0] == username and user_data[1] == password:
                    return True
        return False

    def _is_username_taken(self, username: str) -> bool:
        with open('users.txt', 'r') as f:
            for line in f:
                user_data = line.strip().split('|')
                if user_data[0] == username:
                    return True
        return False


class BlogPost:
    def __init__(self):
        self.posts = self._load_posts()

    def _load_posts(self):
        posts = []
        if os.path.exists('posts.txt'):
            with open('posts.txt', 'r') as f:
                for line in f:
                    post_data = line.strip().split('|')
                    posts.append({
                        'post_id': int(post_data[0]),
                        'title': post_data[1],
                        'content': post_data[2],
                        'author': post_data[3]
                    })
        return posts

    def create_post(self, title: str, content: str, author: str) -> bool:
        post_id = len(self.posts) + 1
        with open('posts.txt', 'a') as f:
            f.write(f"{post_id}|{title}|{content}|{author}\n")
        self.posts.append({'post_id': post_id, 'title': title, 'content': content, 'author': author})
        return True

    def edit_post(self, post_id: int, title: str, content: str) -> bool:
        for post in self.posts:
            if post['post_id'] == post_id:
                post['title'] = title
                post['content'] = content
                self._save_posts()
                return True
        return False

    def delete_post(self, post_id: int) -> bool:
        self.posts = [post for post in self.posts if post['post_id'] != post_id]
        self._save_posts()
        return True

    def view_post(self, post_id: int) -> str:
        for post in self.posts:
            if post['post_id'] == post_id:
                return post['content']
        return ""

    def _save_posts(self):
        with open('posts.txt', 'w') as f:
            for post in self.posts:
                f.write(f"{post['post_id']}|{post['title']}|{post['content']}|{post['author']}\n")


class Main:
    @staticmethod
    def main() -> str:
        return "Welcome to Personal Blog Application"


if __name__ == "__main__":
    app = Main()
    print(app.main())
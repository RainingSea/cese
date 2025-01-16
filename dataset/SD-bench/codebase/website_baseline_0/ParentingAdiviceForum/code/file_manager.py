from user import User
from thread import Thread
from comment import Comment
from advice import Advice

class FileManager:
    def save_user(self, user: User) -> None:
        user.save()

    def load_users(self) -> list:
        users = []
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        except FileNotFoundError:
            pass
        return users

    def save_thread(self, thread: Thread) -> None:
        thread.save()

    def load_threads(self) -> list:
        threads = []
        try:
            with open('threads.txt', 'r') as f:
                for line in f:
                    title, content = line.strip().split('|')
                    threads.append(Thread(title, content))
        except FileNotFoundError:
            pass
        return threads

    def save_comment(self, thread_id: int, comment: Comment) -> None:
        with open('comments.txt', 'a') as f:
            f.write(f"{thread_id}|{comment.content}\n")

    def load_comments(self, thread_id: int) -> list:
        comments = []
        try:
            with open('comments.txt', 'r') as f:
                for line in f:
                    tid, content = line.strip().split('|')
                    if int(tid) == thread_id:
                        comments.append(Comment(content))
        except FileNotFoundError:
            pass
        return comments

    def save_advice(self, advice: Advice) -> None:
        advice.save()

    def load_advice(self) -> list:
        advice_list = []
        try:
            with open('advice.txt', 'r') as f:
                for line in f:
                    title, content = line.strip().split('|')
                    advice_list.append(Advice(title, content))
        except FileNotFoundError:
            pass
        return advice_list
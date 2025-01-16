import os
from typing import List, Dict

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def to_string(self) -> str:
        return f"{self.username}|{self.password}"

class Album:
    def __init__(self, title: str, owner: str, images: List[str], is_private: bool):
        self.title = title
        self.owner = owner
        self.images = images
        self.is_private = is_private

    def to_string(self) -> str:
        images_str = ",".join(self.images)
        return f"{self.title}|{self.owner}|{images_str}|{self.is_private}"

class Comment:
    def __init__(self, album_id: str, user: str, content: str):
        self.album_id = album_id
        self.user = user
        self.content = content

    def to_string(self) -> str:
        return f"{self.album_id}|{self.user}|{self.content}"

class Notification:
    def __init__(self, user: str, message: str):
        self.user = user
        self.message = message

    def to_string(self) -> str:
        return f"{self.user}|{self.message}"

class DataManager:
    def save_user(self, user: User):
        with open('users.txt', 'a') as f:
            f.write(user.to_string() + '\n')

    def load_users(self) -> List[User]:
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        return users

    def save_album(self, album: Album):
        with open('albums.txt', 'a') as f:
            f.write(album.to_string() + '\n')

    def load_albums(self) -> List[Album]:
        albums = []
        if os.path.exists('albums.txt'):
            with open('albums.txt', 'r') as f:
                for line in f:
                    title, owner, images_str, is_private = line.strip().split('|')
                    images = images_str.split(',') if images_str else []
                    albums.append(Album(title, owner, images, is_private == 'True'))
        return albums

    def save_comment(self, comment: Comment):
        with open('comments.txt', 'a') as f:
            f.write(comment.to_string() + '\n')

    def load_comments(self) -> List[Comment]:
        comments = []
        if os.path.exists('comments.txt'):
            with open('comments.txt', 'r') as f:
                for line in f:
                    album_id, user, content = line.strip().split('|')
                    comments.append(Comment(album_id, user, content))
        return comments

    def share_album(self, album_id: str, shared_with: List[str]):
        with open('shared_albums.txt', 'a') as f:
            f.write(f"{album_id}|{','.join(shared_with)}\n")

    def load_shared_albums(self) -> List[tuple]:
        shared_albums = []
        if os.path.exists('shared_albums.txt'):
            with open('shared_albums.txt', 'r') as f:
                for line in f:
                    album_id, shared_with_str = line.strip().split('|')
                    shared_with = shared_with_str.split(',')
                    shared_albums.append((album_id, shared_with))
        return shared_albums

    def follow_user(self, follower: str, followee: str):
        with open('follows.txt', 'a') as f:
            f.write(f"{follower}|{followee}\n")

    def load_followers(self, username: str) -> List[str]:
        followers = []
        if os.path.exists('follows.txt'):
            with open('follows.txt', 'r') as f:
                for line in f:
                    follower, followee = line.strip().split('|')
                    if followee == username:
                        followers.append(follower)
        return followers

    def save_notification(self, notification: Notification):
        with open('notifications.txt', 'a') as f:
            f.write(notification.to_string() + '\n')

    def load_notifications(self, username: str) -> List[Notification]:
        notifications = []
        if os.path.exists('notifications.txt'):
            with open('notifications.txt', 'r') as f:
                for line in f:
                    user, message = line.strip().split('|')
                    if user == username:
                        notifications.append(Notification(user, message))
        return notifications
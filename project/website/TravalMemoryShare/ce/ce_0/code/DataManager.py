import os
from User import User
from Album import Album
from Comment import Comment

class DataManager:
    def load_users(self):
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        return users

    def load_albums(self):
        albums = []
        if os.path.exists('albums.txt'):
            with open('albums.txt', 'r') as file:
                for line in file:
                    title, user, images, is_public = line.strip().split('|')
                    albums.append(Album(title, user, images.split(','), is_public == 'True'))
        return albums

    def load_comments(self):
        comments = []
        if os.path.exists('comments.txt'):
            with open('comments.txt', 'r') as file:
                for line in file:
                    album_id, user, content = line.strip().split('|')
                    comments.append(Comment(album_id, user, content))
        return comments

    def save_user(self, user: User):
        with open('users.txt', 'a') as file:
            file.write(f"{user.username}|{user.password}\n")

    def save_album(self, album: Album):
        with open('albums.txt', 'a') as file:
            file.write(f"{album.title}|{album.user}|{','.join(album.images)}|{album.is_public}\n")

    def save_comment(self, comment: Comment):
        with open('comments.txt', 'a') as file:
            file.write(f"{comment.album_id}|{comment.user}|{comment.content}\n")
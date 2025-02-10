import json
from models import User, Tip, Resource, ForumPost

class DataManager:
    def load_users(self) -> list:
        try:
            with open('users.txt', 'r') as file:
                return [User(*line.strip().split('|')) for line in file.readlines()]
        except FileNotFoundError:
            return []

    def save_users(self, users: list) -> None:
        with open('users.txt', 'w') as file:
            for user in users:
                file.write(f"{user.username}|{user.password}\n")

    def load_tips(self) -> list:
        try:
            with open('tips.txt', 'r') as file:
                return [Tip(*line.strip().split('|')) for line in file.readlines()]
        except FileNotFoundError:
            return []

    def save_tips(self, tips: list) -> None:
        with open('tips.txt', 'w') as file:
            for tip in tips:
                file.write(f"{tip.title}|{tip.content}\n")

    def load_resources(self) -> list:
        try:
            with open('resources.txt', 'r') as file:
                return [Resource(*line.strip().split('|')) for line in file.readlines()]
        except FileNotFoundError:
            return []

    def save_resources(self, resources: list) -> None:
        with open('resources.txt', 'w') as file:
            for resource in resources:
                file.write(f"{resource.title}|{resource.link}\n")

    def load_forum_posts(self) -> list:
        try:
            with open('forum.txt', 'r') as file:
                return [ForumPost(*line.strip().split('|')) for line in file.readlines()]
        except FileNotFoundError:
            return []

    def save_forum_posts(self, posts: list) -> None:
        with open('forum.txt', 'w') as file:
            for post in posts:
                file.write(f"{post.username}|{post.content}\n")
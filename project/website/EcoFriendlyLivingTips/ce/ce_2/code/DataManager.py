from User import User
from Tip import Tip
from Resource import Resource
from ForumPost import ForumPost

class DataManager:
    def load_users(self) -> list[User]:
        users = []
        with open('users.txt', 'r') as file:
            for line in file:
                username, password, email = line.strip().split('|')
                users.append(User(username, password, email))
        return users

    def save_user(self, user: User):
        with open('users.txt', 'a') as file:
            file.write(user.to_string() + '\n')

    def load_tips(self) -> list[Tip]:
        tips = []
        with open('tips.txt', 'r') as file:
            for line in file:
                title, content, author = line.strip().split('|')
                tips.append(Tip(title, content, author))
        return tips

    def save_tip(self, tip: Tip):
        with open('tips.txt', 'a') as file:
            file.write(tip.to_string() + '\n')

    def load_resources(self) -> list[Resource]:
        resources = []
        with open('resources.txt', 'r') as file:
            for line in file:
                title, url = line.strip().split('|')
                resources.append(Resource(title, url))
        return resources

    def save_resource(self, resource: Resource):
        with open('resources.txt', 'a') as file:
            file.write(resource.to_string() + '\n')

    def load_forum_posts(self) -> list[ForumPost]:
        posts = []
        with open('forum.txt', 'r') as file:
            for line in file:
                title, content, author = line.strip().split('|')
                posts.append(ForumPost(title, content, author))
        return posts

    def save_forum_post(self, post: ForumPost):
        with open('forum.txt', 'a') as file:
            file.write(post.to_string() + '\n')
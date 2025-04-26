import os

class Main:
    def main(self):
        self.load_data()
        self.show_login_page()

    def load_data(self):
        self.users = self.load_users()
        self.tips = self.load_tips()
        self.resources = self.load_resources()
        self.forum_posts = self.load_forum_posts()

    def load_users(self):
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        return users

    def load_tips(self):
        tips = []
        if os.path.exists('tips.txt'):
            with open('tips.txt', 'r') as file:
                for line in file:
                    tips.append(Tip(line.strip()))
        return tips

    def load_resources(self):
        resources = []
        if os.path.exists('resources.txt'):
            with open('resources.txt', 'r') as file:
                for line in file:
                    resources.append(Resource(line.strip()))
        return resources

    def load_forum_posts(self):
        forum_posts = []
        if os.path.exists('forum.txt'):
            with open('forum.txt', 'r') as file:
                for line in file:
                    forum_posts.append(ForumPost(line.strip()))
        return forum_posts

    def show_login_page(self):
        # Logic to display login page goes here
        pass

    def login(self):
        # Logic for user login goes here
        pass

    def register(self):
        # Logic for user registration goes here
        pass

    def submitTip(self):
        # Logic for submitting a tip goes here
        pass

    def addResource(self):
        # Logic for adding a resource goes here
        pass

    def viewForum(self):
        # Logic for viewing forum posts goes here
        pass

    def updateProfile(self):
        # Logic for updating user profile goes here
        pass

    def contactSupport(self):
        # Logic for contacting support goes here
        pass


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def createAccount(self):
        # Logic to create an account goes here
        return True

    def validateLogin(self, username, password):
        return self.username == username and self.password == password

    def updateProfile(self):
        # Logic to update user profile goes here
        return True


class Tip:
    def __init__(self, content):
        self.content = content

    def submitTip(self):
        # Logic to submit a tip goes here
        return True

    def getAllTips(self):
        return [tip.content for tip in Main().load_tips()]


class Resource:
    def __init__(self, url):
        self.url = url

    def addResource(self):
        # Logic to add a resource goes here
        return True

    def getAllResources(self):
        return [resource.url for resource in Main().load_resources()]


class ForumPost:
    def __init__(self, content):
        self.content = content

    def addPost(self):
        # Logic to add a forum post goes here
        return True

    def getAllPosts(self):
        return [post.content for post in Main().load_forum_posts()]
from user import User
from tip import Tip
from resource import Resource
from forum_post import ForumPost

class EcoFriendlyLivingTips:
    """Handles the eco-friendly living tips application logic."""
    def __init__(self):
        self.users = []
        self.tips = []
        self.resources = []
        self.forum_posts = []

    def register_user(self, username: str, password: str, email: str):
        """Registers a new user."""
        user = User(username, password, email)
        user.save()

    def login_user(self, username: str, password: str) -> bool:
        """Logs in a user."""
        user = User.load(username)
        if user and user.password == password:
            return True
        return False

    def submit_tip(self, title: str, content: str):
        """Submits a new tip."""
        tip = Tip(title, content)
        tip.save()

    def submit_resource(self, title: str, url: str):
        """Submits a new resource."""
        resource = Resource(title, url)
        resource.save()

    def submit_forum_post(self, username: str, content: str):
        """Submits a new forum post."""
        forum_post = ForumPost(username, content)
        forum_post.save()

    def load_data(self):
        """Loads all data from files."""
        self.users = User.load_all()
        self.tips = Tip.load_all()
        self.resources = Resource.load_all()
        self.forum_posts = ForumPost.load_all()
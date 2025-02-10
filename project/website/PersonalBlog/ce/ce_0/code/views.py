from flask import render_template
from models import BlogPost

class View:
    """Handles rendering of HTML pages."""
    @staticmethod
    def render_login() -> str:
        """Render the login page."""
        return render_template('login.html')

    @staticmethod
    def render_registration() -> str:
        """Render the registration page."""
        return render_template('register.html')

    @staticmethod
    def render_main(posts: list) -> str:
        """Render the main blog page."""
        return render_template('main.html', posts=posts)

    @staticmethod
    def render_new_post() -> str:
        """Render the new post page."""
        return render_template('new_post.html')

    @staticmethod
    def render_view_post(post: BlogPost) -> str:
        """Render a single blog post."""
        return render_template('view_post.html', post=post)

    @staticmethod
    def render_edit_post(post: BlogPost) -> str:
        """Render the edit post page."""
        return render_template('edit_post.html', post=post)
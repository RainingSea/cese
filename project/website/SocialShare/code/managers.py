import os
from datetime import datetime

class UserManager:
    def user_exists(self, username):
        if not os.path.exists('users.txt'):
            return False
        with open('users.txt', 'r') as f:
            for line in f:
                if line.strip() and line.split('|')[0] == username:
                    return True
        return False

    def register(self, username, password):
        if self.user_exists(username):
            return False
        with open('users.txt', 'a') as f:
            f.write(f"{username}|{password}\n")
        return True

    def login(self, username, password):
        if not os.path.exists('users.txt'):
            return False
        with open('users.txt', 'r') as f:
            for line in f:
                if line.strip() and line.split('|')[0] == username and line.split('|')[1].strip() == password:
                    return True
        return False

class ProfileManager:
    def create_profile(self, username, bio):
        with open('profiles.txt', 'a') as f:
            f.write(f"{username}|{bio}|{datetime.now().isoformat()}\n")
        return True

    def get_profile(self, username):
        if not os.path.exists('profiles.txt'):
            return None
        
        latest_profile = None
        with open('profiles.txt', 'r') as f:
            for line in f:
                if line.strip() and line.split('|')[0] == username:
                    parts = line.strip().split('|')
                    latest_profile = {'username': parts[0], 'bio': parts[1], 'timestamp': parts[2]}
        return latest_profile

    def update_profile(self, username, bio):
        if not os.path.exists('profiles.txt'):
            return False
        
        lines = []
        updated = False
        with open('profiles.txt', 'r') as f:
            for line in f:
                if line.strip() and line.split('|')[0] == username:
                    lines.append(f"{username}|{bio}|{datetime.now().isoformat()}\n")
                    updated = True
                else:
                    lines.append(line)
        
        if not updated:
            lines.append(f"{username}|{bio}|{datetime.now().isoformat()}\n")
        
        with open('profiles.txt', 'w') as f:
            f.writelines(lines)
        return True

class ContentManager:
    def upload_content(self, username, title, content):
        with open('content.txt', 'a') as f:
            f.write(f"{username}|{title}|{content}|{datetime.now().isoformat()}\n")
        return True

    def get_feed(self):
        if not os.path.exists('content.txt'):
            return []
        
        with open('content.txt', 'r') as f:
            lines = f.readlines()
        
        feed = []
        for i, line in enumerate(lines):
            if line.strip():
                parts = line.strip().split('|')
                feed.append({
                    'id': str(i+1),
                    'username': parts[0],
                    'title': parts[1],
                    'content': parts[2],
                    'timestamp': parts[3]
                })
        
        return sorted(feed, key=lambda x: x['timestamp'], reverse=True)

    def get_content_by_user(self, username):
        if not os.path.exists('content.txt'):
            return []
        
        user_content = []
        with open('content.txt', 'r') as f:
            for i, line in enumerate(f):
                if line.strip() and line.split('|')[0] == username:
                    parts = line.strip().split('|')
                    user_content.append({
                        'id': str(i+1),
                        'title': parts[1],
                        'content': parts[2],
                        'timestamp': parts[3]
                    })
        
        return sorted(user_content, key=lambda x: x['timestamp'], reverse=True)

    def get_feed_for_users(self, usernames):
        if not os.path.exists('content.txt'):
            return []
        
        feed = []
        with open('content.txt', 'r') as f:
            for i, line in enumerate(f):
                if line.strip() and line.split('|')[0] in usernames:
                    parts = line.strip().split('|')
                    feed.append({
                        'id': str(i+1),
                        'username': parts[0],
                        'title': parts[1],
                        'content': parts[2],
                        'timestamp': parts[3]
                    })
        
        return sorted(feed, key=lambda x: x['timestamp'], reverse=True)

class InteractionManager:
    def like_content(self, username, content_id):
        with open('interactions.txt', 'a') as f:
            f.write(f"{username}|{content_id}|like||{datetime.now().isoformat()}\n")
        return True

    def comment(self, username, content_id, text):
        with open('interactions.txt', 'a') as f:
            f.write(f"{username}|{content_id}|comment|{text}|{datetime.now().isoformat()}\n")
        return True

    def get_interactions(self, content_id):
        if not os.path.exists('interactions.txt'):
            return []
        
        interactions = []
        with open('interactions.txt', 'r') as f:
            for line in f:
                if line.strip() and line.split('|')[1] == content_id:
                    parts = line.strip().split('|')
                    interactions.append({
                        'username': parts[0],
                        'content_id': parts[1],
                        'type': parts[2],
                        'text': parts[3],
                        'timestamp': parts[4]
                    })
        
        return sorted(interactions, key=lambda x: x['timestamp'])

    def follow_user(self, follower, target):
        with open('followers.txt', 'a') as f:
            f.write(f"{follower}|{target}|{datetime.now().isoformat()}\n")
        return True

    def unfollow_user(self, follower, target):
        if not os.path.exists('followers.txt'):
            return False
        
        lines = []
        removed = False
        with open('followers.txt', 'r') as f:
            for line in f:
                if line.strip() and not (line.split('|')[0] == follower and line.split('|')[1] == target):
                    lines.append(line)
                else:
                    removed = True
        
        with open('followers.txt', 'w') as f:
            f.writelines(lines)
        return removed

    def check_following(self, follower, target):
        if not os.path.exists('followers.txt'):
            return False
        
        with open('followers.txt', 'r') as f:
            for line in f:
                if line.strip() and line.split('|')[0] == follower and line.split('|')[1] == target:
                    return True
        return False

    def get_following(self, username):
        if not os.path.exists('followers.txt'):
            return []
        
        following = []
        with open('followers.txt', 'r') as f:
            for line in f:
                if line.strip() and line.split('|')[0] == username:
                    following.append(line.split('|')[1])
        return following
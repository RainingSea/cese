import logging
from datetime import datetime

class UserManager:
    def __init__(self, users_file):
        self.users_file = users_file
        self.logger = logging.getLogger(__name__)

    def register(self, username, password):
        try:
            if self.user_exists(username):
                self.logger.warning(f'Username {username} already exists')
                return False
            with open(self.users_file, 'a') as f:
                f.write(f"{username}|{password}\n")
            return True
        except Exception as e:
            self.logger.error(f'Error registering user: {e}')
            return False

    def validate_user(self, username, password):
        try:
            with open(self.users_file, 'r') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if parts[0] == username and parts[1] == password:
                        return True
            return False
        except Exception as e:
            self.logger.error(f'Error validating user: {e}')
            return False

    def user_exists(self, username):
        try:
            with open(self.users_file, 'r') as f:
                for line in f:
                    if line.startswith(username + '|'):
                        return True
            return False
        except Exception as e:
            self.logger.error(f'Error checking user existence: {e}')
            return False

class ProfileManager:
    def __init__(self, profiles_file):
        self.profiles_file = profiles_file
        self.logger = logging.getLogger(__name__)

    def get_profile(self, username):
        try:
            with open(self.profiles_file, 'r') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if parts[0] == username:
                        return {'username': parts[0], 'interests': parts[1], 'expertise': parts[2]}
            return {'username': username, 'interests': '', 'expertise': ''}
        except Exception as e:
            self.logger.error(f'Error getting profile: {e}')
            return {'username': username, 'interests': '', 'expertise': ''}

    def update_profile(self, username, interests, expertise):
        try:
            lines = []
            updated = False
            try:
                with open(self.profiles_file, 'r') as f:
                    for line in f:
                        parts = line.strip().split('|')
                        if parts[0] == username:
                            lines.append(f"{username}|{interests}|{expertise}\n")
                            updated = True
                        else:
                            lines.append(line)
            except FileNotFoundError:
                pass
            
            if not updated:
                lines.append(f"{username}|{interests}|{expertise}\n")
            
            with open(self.profiles_file, 'w') as f:
                f.writelines(lines)
            return True
        except Exception as e:
            self.logger.error(f'Error updating profile: {e}')
            return False

class GroupManager:
    def __init__(self, groups_file):
        self.groups_file = groups_file
        self.logger = logging.getLogger(__name__)

    def list_groups(self):
        try:
            groups = []
            with open(self.groups_file, 'r') as f:
                for line in f:
                    parts = line.strip().split('|')
                    groups.append({'name': parts[0], 'members': parts[1].split(',') if len(parts) > 1 else []})
            return groups
        except Exception as e:
            self.logger.error(f'Error listing groups: {e}')
            return []

    def join_group(self, username, groupname):
        try:
            lines = []
            updated = False
            with open(self.groups_file, 'r') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if parts[0] == groupname:
                        members = parts[1].split(',') if len(parts) > 1 else []
                        if username not in members:
                            members.append(username)
                        lines.append(f"{groupname}|{','.join(members)}\n")
                        updated = True
                    else:
                        lines.append(line)
            
            if not updated:
                lines.append(f"{groupname}|{username}\n")
            
            with open(self.groups_file, 'w') as f:
                f.writelines(lines)
            return True
        except Exception as e:
            self.logger.error(f'Error joining group: {e}')
            return False

    def get_user_groups(self, username):
        try:
            user_groups = []
            with open(self.groups_file, 'r') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) > 1 and username in parts[1].split(','):
                        user_groups.append({'name': parts[0], 'members': parts[1].split(',')})
            return user_groups
        except Exception as e:
            self.logger.error(f'Error getting user groups: {e}')
            return []

class ResourceManager:
    def __init__(self, resources_file):
        self.resources_file = resources_file
        self.logger = logging.getLogger(__name__)

    def add_resource(self, title, content, author, group):
        try:
            with open(self.resources_file, 'a') as f:
                f.write(f"{title}|{content}|{author}|{group}\n")
            return True
        except Exception as e:
            self.logger.error(f'Error adding resource: {e}')
            return False

    def get_resources(self, group):
        try:
            resources = []
            with open(self.resources_file, 'r') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if group is None or parts[3] == group:
                        resources.append({
                            'title': parts[0],
                            'content': parts[1],
                            'author': parts[2],
                            'group': parts[3]
                        })
            return resources
        except Exception as e:
            self.logger.error(f'Error getting resources: {e}')
            return []

    def get_latest_resources(self, count):
        try:
            resources = []
            with open(self.resources_file, 'r') as f:
                lines = f.readlines()
                for line in lines[-count:]:
                    parts = line.strip().split('|')
                    resources.append({
                        'title': parts[0],
                        'content': parts[1],
                        'author': parts[2],
                        'group': parts[3]
                    })
            return resources
        except Exception as e:
            self.logger.error(f'Error getting latest resources: {e}')
            return []

class MessageManager:
    def __init__(self, messages_file):
        self.messages_file = messages_file
        self.logger = logging.getLogger(__name__)

    def send_message(self, sender, receiver, content):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.messages_file, 'a') as f:
                f.write(f"{sender}|{receiver}|{content}|{timestamp}\n")
            return True
        except Exception as e:
            self.logger.error(f'Error sending message: {e}')
            return False

    def get_messages(self, user):
        try:
            messages = []
            with open(self.messages_file, 'r') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if parts[0] == user or parts[1] == user:
                        messages.append({
                            'sender': parts[0],
                            'receiver': parts[1],
                            'content': parts[2],
                            'timestamp': parts[3],
                            'is_read': parts[0] != user
                        })
            return messages
        except Exception as e:
            self.logger.error(f'Error getting messages: {e}')
            return []

    def post_group_message(self, group_name, sender, message):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.messages_file, 'a') as f:
                f.write(f"GROUP|{group_name}|{sender}|{message}|{timestamp}\n")
            return True
        except Exception as e:
            self.logger.error(f'Error posting group message: {e}')
            return False

    def get_group_messages(self, group_name):
        try:
            messages = []
            with open(self.messages_file, 'r') as f:
                for line in f:
                    parts = line.strip().split('|')
                    if parts[0] == "GROUP" and parts[1] == group_name:
                        messages.append({
                            'group': parts[1],
                            'sender': parts[2],
                            'content': parts[3],
                            'timestamp': parts[4]
                        })
            return messages
        except Exception as e:
            self.logger.error(f'Error getting group messages: {e}')
            return []
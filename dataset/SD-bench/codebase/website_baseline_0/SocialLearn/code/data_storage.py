import os
from user import User
from profile import Profile
from study_group import StudyGroup
from resource import Resource
from message import Message
import logging

class DataStorage:
    def __init__(self):
        self.user_file = 'users.txt'
        self.profile_file = 'profiles.txt'
        self.group_file = 'groups.txt'
        self.resource_file = 'resources.txt'
        self.message_file = 'messages.txt'
        logging.basicConfig(level=logging.INFO)

    def save_user(self, user: User) -> None:
        with open(self.user_file, 'a') as f:
            f.write(f"{user.username}|{user.password}\n")
        logging.info(f"User {user.username} saved.")

    def load_users(self) -> list:
        users = []
        if os.path.exists(self.user_file):
            with open(self.user_file, 'r') as f:
                for line in f:
                    username, password = line.strip().split('|')
                    users.append(User(username, password))
        logging.info(f"Loaded {len(users)} users.")
        return users

    def save_profile(self, profile: Profile) -> None:
        with open(self.profile_file, 'a') as f:
            interests = ','.join(profile.interests)
            f.write(f"{profile.username}|{interests}\n")
        logging.info(f"Profile for {profile.username} saved.")

    def load_profiles(self) -> list:
        profiles = []
        if os.path.exists(self.profile_file):
            with open(self.profile_file, 'r') as f:
                for line in f:
                    username, interests = line.strip().split('|')
                    interests_list = interests.split(',')
                    profiles.append(Profile(username, interests_list))
        logging.info(f"Loaded {len(profiles)} profiles.")
        return profiles

    def save_group(self, group: StudyGroup) -> None:
        with open(self.group_file, 'a') as f:
            members = ','.join(group.members)
            f.write(f"{group.group_name}|{members}\n")
        logging.info(f"Group {group.group_name} saved.")

    def load_groups(self) -> list:
        groups = []
        if os.path.exists(self.group_file):
            with open(self.group_file, 'r') as f:
                for line in f:
                    group_name, members = line.strip().split('|')
                    members_list = members.split(',')
                    groups.append(StudyGroup(group_name, members_list))
        logging.info(f"Loaded {len(groups)} groups.")
        return groups

    def save_resource(self, resource: Resource) -> None:
        with open(self.resource_file, 'a') as f:
            f.write(f"{resource.title}|{resource.link}\n")
        logging.info(f"Resource {resource.title} saved.")

    def load_resources(self) -> list:
        resources = []
        if os.path.exists(self.resource_file):
            with open(self.resource_file, 'r') as f:
                for line in f:
                    title, link = line.strip().split('|')
                    resources.append(Resource(title, link))
        logging.info(f"Loaded {len(resources)} resources.")
        return resources

    def save_message(self, message: Message) -> None:
        with open(self.message_file, 'a') as f:
            f.write(f"{message.sender}|{message.receiver}|{message.content}\n")
        logging.info(f"Message from {message.sender} to {message.receiver} saved.")

    def load_messages(self) -> list:
        messages = []
        if os.path.exists(self.message_file):
            with open(self.message_file, 'r') as f:
                for line in f:
                    sender, receiver, content = line.strip().split('|')
                    messages.append(Message(sender, receiver, content))
        logging.info(f"Loaded {len(messages)} messages.")
        return messages
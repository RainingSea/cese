import os
import time

class InteractionController:
    def __init__(self):
        self.interactions_file = "interactions.txt"
        self.messages_file = "messages.txt"
        if not os.path.exists(self.interactions_file):
            open(self.interactions_file, 'w').close()
        if not os.path.exists(self.messages_file):
            open(self.messages_file, 'w').close()

    def like_content(self, username, content_id):
        interaction_id = f"{int(time.time())}_{hash(username + content_id)}"
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(self.interactions_file, 'a') as f:
            f.write(f"{interaction_id}|like|{content_id}|{username}||{timestamp}\n")
        return True

    def comment(self, username, content_id, comment):
        interaction_id = f"{int(time.time())}_{hash(username + content_id + comment)}"
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(self.interactions_file, 'a') as f:
            f.write(f"{interaction_id}|comment|{content_id}|{username}|{comment}|{timestamp}\n")
        return True

    def follow(self, username, target_user):
        interaction_id = f"{int(time.time())}_{hash(username + target_user)}"
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(self.interactions_file, 'a') as f:
            f.write(f"{interaction_id}|follow||{username}|{target_user}|{timestamp}\n")
        return True

    def send_message(self, sender, receiver, message_content):
        message_id = f"{int(time.time())}_{hash(sender + receiver)}"
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(self.messages_file, 'a') as f:
            f.write(f"{message_id}|{sender}|{receiver}|{message_content}|{timestamp}\n")
        return True
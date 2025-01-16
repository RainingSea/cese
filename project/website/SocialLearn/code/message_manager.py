import json
from message import Message

class MessageManager:
    def __init__(self):
        self.messages_file = 'messages.json'
        self.messages = self.load_messages()

    def load_messages(self):
        try:
            with open(self.messages_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_messages(self):
        with open(self.messages_file, 'w') as file:
            json.dump(self.messages, file)

    def send_message(self, sender, receiver, content):
        message = Message(sender, receiver, content)
        self.messages.append(message.__dict__)
        self.save_messages()
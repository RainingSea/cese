class MessageManager:
    def __init__(self, filename):
        self.filename = filename
        self.messages = self.load_messages()

    def load_messages(self):
        messages = []
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    sender, receiver, content = line.strip().split('|')
                    messages.append({'sender': sender, 'receiver': receiver, 'content': content})
        except FileNotFoundError:
            pass
        return messages

    def send_message(self, sender: str, receiver: str, content: str) -> bool:
        self.messages.append({'sender': sender, 'receiver': receiver, 'content': content})
        self.save_messages()
        return True

    def get_messages(self, username: str):
        return [msg for msg in self.messages if msg['receiver'] == username or msg['sender'] == username]

    def save_messages(self):
        with open(self.filename, 'w') as file:
            for message in self.messages:
                file.write(f"{message['sender']}|{message['receiver']}|{message['content']}\n")
class MessageManager:
    def __init__(self):
        self.messages = self.load_messages()

    def load_messages(self):
        messages = []
        with open('messages.txt', 'r') as f:
            for line in f:
                messages.append(line.strip())
        return messages

    def send_message(self, from_user: str, to_user: str, message: str) -> bool:
        self.messages.append(f"{from_user}|{to_user}|{message}")
        self.save_messages()
        return True

    def get_messages(self, username: str):
        return [msg for msg in self.messages if msg.split('|')[1] == username]

    def save_messages(self):
        with open('messages.txt', 'w') as f:
            for message in self.messages:
                f.write(f"{message}\n")
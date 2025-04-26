class MessageManager:
    def __init__(self):
        self.messages = self.load_messages()

    def load_messages(self):
        messages = []
        with open('messages.txt', 'r') as file:
            for line in file:
                from_user, to_user, content = line.strip().split('|')
                messages.append({'from': from_user, 'to': to_user, 'content': content})
        return messages

    def send_message(self, from_user: str, to_user: str, content: str) -> bool:
        self.messages.append({'from': from_user, 'to': to_user, 'content': content})
        self.save_messages()
        return True

    def get_messages(self, username: str) -> list:
        return [msg for msg in self.messages if msg['to'] == username]

    def save_messages(self):
        with open('messages.txt', 'w') as file:
            for message in self.messages:
                file.write(f"{message['from']}|{message['to']}|{message['content']}\n")
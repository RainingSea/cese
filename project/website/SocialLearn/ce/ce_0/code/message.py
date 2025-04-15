class Message:
    def __init__(self, sender: str, receiver: str, content: str):
        self.sender = sender
        self.receiver = receiver
        self.content = content

    def send_message(self):
        """Save the message to the messages.txt file."""
        with open('messages.txt', 'a') as file:
            file.write(f"{self.sender}|{self.receiver}|{self.content}\n")

    @staticmethod
    def load_messages() -> list:
        """Load messages from the messages.txt file."""
        messages = []
        try:
            with open('messages.txt', 'r') as file:
                for line in file:
                    sender, receiver, content = line.strip().split('|')
                    messages.append({'sender': sender, 'receiver': receiver, 'content': content})
        except FileNotFoundError:
            return []
        return messages
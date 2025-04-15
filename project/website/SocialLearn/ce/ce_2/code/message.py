class Message:
    """Message class to handle messaging between users."""
    def __init__(self, sender: str, recipient: str, content: str):
        self.sender = sender
        self.recipient = recipient
        self.content = content

    def send_message(self) -> bool:
        """Send a message by saving it to the messages.txt file."""
        try:
            with open('messages.txt', 'a') as file:
                file.write(f"{self.sender}|{self.recipient}|{self.content}\n")
            return True
        except Exception as e:
            print(f"Error sending message: {e}")
            return False

    def get_messages(self) -> list:
        """Retrieve all messages from the messages.txt file."""
        messages = []
        try:
            with open('messages.txt', 'r') as file:
                for line in file:
                    sender, recipient, content = line.strip().split('|')
                    messages.append({'sender': sender, 'recipient': recipient, 'content': content})
        except Exception as e:
            print(f"Error loading messages: {e}")
        return messages
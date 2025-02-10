class Message:
    def __init__(self, sender: str, receiver: str, content: str):
        self.sender = sender
        self.receiver = receiver
        self.content = content

    def save(self):
        with open('messages.txt', 'a') as file:
            file.write(f"{self.sender}|{self.receiver}|{self.content}\n")
import os

class Message:
    def __init__(self, sender: str, recipient: str, content: str):
        self.sender = sender
        self.recipient = recipient
        self.content = content

    def save(self):
        with open('messages.txt', 'a') as file:
            file.write(f"{self.sender}|{self.recipient}|{self.content}\n")
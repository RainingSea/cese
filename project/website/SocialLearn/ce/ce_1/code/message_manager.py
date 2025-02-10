class MessageManager:
    def __init__(self):
        self.messages = []

    def send_message(self, from_user: str, to_user: str, message: str) -> None:
        self.messages.append(f"{from_user}|{to_user}|{message}")
        self.save_messages()

    def load_messages(self) -> list:
        try:
            with open('messages.txt', 'r') as file:
                self.messages = [line.strip() for line in file]
        except FileNotFoundError:
            self.messages = []

    def save_messages(self) -> None:
        with open('messages.txt', 'w') as file:
            for message in self.messages:
                file.write(f"{message}\n")
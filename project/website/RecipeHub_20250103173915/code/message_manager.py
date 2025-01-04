class MessageManager:
    def __init__(self, messages_file: str):
        self.messages_file = messages_file

    def log_message(self, message: str):
        with open(self.messages_file, 'a') as f:
            f.write(f"{message}\n")
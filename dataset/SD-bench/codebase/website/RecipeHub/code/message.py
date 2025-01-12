class Message:
    def __init__(self):
        self.content = ""

    def success_message(self) -> str:
        return "Operation completed successfully."

    def error_message(self) -> str:
        return "An error occurred. Please try again."
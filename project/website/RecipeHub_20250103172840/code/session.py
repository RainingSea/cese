class Session:
    def __init__(self):
        self.session_data = {}

    def create_session(self, username: str) -> bool:
        self.session_data[username] = True
        return True

    def destroy_session(self, username: str) -> bool:
        if username in self.session_data:
            del self.session_data[username]
            return True
        return False
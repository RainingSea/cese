class SessionManager:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.load_sessions()

    def load_sessions(self):
        self.sessions = {}
        with open(self.filepath, 'r') as file:
            for line in file:
                username = line.strip()
                self.sessions[username] = True

    def create_session(self, username: str) -> bool:
        if username in self.sessions:
            return False
        self.sessions[username] = True
        with open(self.filepath, 'a') as file:
            file.write(f"{username}\n")
        return True

    def destroy_session(self, username: str) -> bool:
        if username not in self.sessions:
            return False
        del self.sessions[username]
        self.save_sessions()
        return True

    def save_sessions(self):
        with open(self.filepath, 'w') as file:
            for username in self.sessions.keys():
                file.write(f"{username}\n")
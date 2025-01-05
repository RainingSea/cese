class Session:
    def __init__(self, username: str):
        self.username = username

    def save(self):
        with open('sessions.txt', 'a') as file:
            file.write(f"{self.username}\n")

    @staticmethod
    def load():
        sessions = []
        with open('sessions.txt', 'r') as file:
            for line in file:
                sessions.append(line.strip())
        return sessions
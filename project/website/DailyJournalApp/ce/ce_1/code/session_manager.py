class Session:
    def __init__(self, username: str):
        self.username = username

    def save(self):
        with open('sessions.txt', 'a') as file:
            file.write(f'{self.username}\n')

    @staticmethod
    def load() -> str:
        with open('sessions.txt', 'r') as file:
            return file.readline().strip()
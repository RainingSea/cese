import os

class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def is_authenticated(self) -> bool:
        return True  # For simplicity, we assume the user is authenticated if they exist in the file

class JournalEntry:
    def __init__(self, title: str, content: str, date: str):
        self.title = title
        self.content = content
        self.date = date

    def save(self) -> None:
        with open('journal_entries.txt', 'a') as file:
            file.write(f"{self.title}|{self.content}|{self.date}\n")

    @staticmethod
    def load_entries() -> list:
        if not os.path.exists('journal_entries.txt'):
            return []
        with open('journal_entries.txt', 'r') as file:
            entries = [line.strip().split('|') for line in file.readlines()]
            return [JournalEntry(title, content, date) for title, content, date in entries]

class Main:
    def main(self) -> str:
        return "Welcome to the Daily Journal App"

    def login(self, username: str, password: str) -> bool:
        if not os.path.exists('users.txt'):
            return False
        with open('users.txt', 'r') as file:
            for line in file:
                user, pwd = line.strip().split('|')
                if user == username and pwd == password:
                    return True
        return False

    def register(self, username: str, password: str) -> bool:
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    user, _ = line.strip().split('|')
                    if user == username:
                        return False  # User already exists
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def create_entry(self, title: str, content: str) -> None:
        from datetime import datetime
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = JournalEntry(title, content, date)
        entry.save()

    def view_entries(self) -> list:
        return JournalEntry.load_entries()

    def logout(self) -> None:
        pass  # In a real application, this would clear the session

if __name__ == "__main__":
    app = Main()
    print(app.main())
import os
from datetime import datetime
from user_manager import UserManager
from note_manager import NoteManager

class Main:
    def __init__(self):
        self.user_manager = UserManager('users.txt')
        self.note_manager = NoteManager()

    def main(self):
        # Load existing users and notes
        self.user_manager.load_users()
        self.note_manager.load_notes()
        # Start the application (placeholder for actual UI logic)
        print("Welcome to the Note Taking App!")

if __name__ == "__main__":
    app = Main()
    app.main()
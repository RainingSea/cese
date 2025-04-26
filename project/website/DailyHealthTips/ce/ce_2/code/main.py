import os
import json

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.tip_manager = TipManager()
        self.feedback_manager = FeedbackManager()

    def main(self):
        # Load data from files
        self.user_manager.load_users()
        self.tip_manager.load_tips()
        self.feedback_manager.load_feedbacks()
        # Start the application (this would be where you'd set up your web server)
        print("DailyHealthTips application started.")

class UserManager:
    def __init__(self):
        self.users = []

    def load_users(self):
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                self.users = [line.strip().split('|') for line in file.readlines()]

    def login(self, username: str, password: str) -> bool:
        for user in self.users:
            if user[0] == username and user[1] == password:
                return True
        return False

    def register(self, username: str, password: str) -> bool:
        if any(user[0] == username for user in self.users):
            return False
        self.users.append([username, password])
        with open('users.txt', 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

class TipManager:
    def __init__(self):
        self.tips = []

    def load_tips(self):
        if os.path.exists('tips.txt'):
            with open('tips.txt', 'r') as file:
                self.tips = [line.strip() for line in file.readlines()]

    def get_current_tip(self) -> str:
        return self.tips[0] if self.tips else "No tips available."

    def get_previous_tip(self) -> str:
        return self.tips[-1] if len(self.tips) > 1 else "No previous tip available."

    def get_next_tip(self) -> str:
        return self.tips[1] if len(self.tips) > 1 else "No next tip available."

    def search_tips(self, query: str) -> list:
        return [tip for tip in self.tips if query.lower() in tip.lower()]

class FeedbackManager:
    def __init__(self):
        self.feedbacks = []

    def load_feedbacks(self):
        if os.path.exists('feedback.txt'):
            with open('feedback.txt', 'r') as file:
                self.feedbacks = [line.strip() for line in file.readlines()]

    def submit_feedback(self, feedback: str) -> None:
        self.feedbacks.append(feedback)
        with open('feedback.txt', 'a') as file:
            file.write(f"{feedback}\n")

if __name__ == "__main__":
    app = Main()
    app.main()
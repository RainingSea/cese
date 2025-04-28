import os

class Main:
    def __init__(self):
        self.user_manager = UserManager('users.txt')
        self.test_result_manager = TestResultManager('test_results.txt')
        self.reminder_manager = ReminderManager('reminders.txt')

    def main(self):
        while True:
            print("Welcome to the Medical Test Tracker")
            print("1. Register")
            print("2. Login")
            choice = input("Choose an option: ")
            if choice == '1':
                username = input("Enter username: ")
                password = input("Enter password: ")
                if self.user_manager.register(username, password):
                    print("Registration successful!")
                else:
                    print("Registration failed. Username may already exist.")
            elif choice == '2':
                username = input("Enter username: ")
                password = input("Enter password: ")
                if self.user_manager.login(username, password):
                    print("Login successful!")
                    self.dashboard(username)
                else:
                    print("Login failed. Invalid credentials.")
            else:
                print("Invalid option. Please try again.")

    def dashboard(self, username):
        while True:
            print(f"Welcome {username} to your dashboard!")
            print("1. Add Test Result")
            print("2. View Test Results")
            print("3. Set Reminder")
            print("4. View Reminders")
            print("5. Logout")
            choice = input("Choose an option: ")
            if choice == '1':
                result = input("Enter test result: ")
                if self.test_result_manager.add_result(username, result):
                    print("Test result added successfully!")
                else:
                    print("Failed to add test result.")
            elif choice == '2':
                results = self.test_result_manager.get_results(username)
                print("Your Test Results:")
                for res in results:
                    print(res)
            elif choice == '3':
                reminder = input("Enter reminder: ")
                if self.reminder_manager.set_reminder(username, reminder):
                    print("Reminder set successfully!")
                else:
                    print("Failed to set reminder.")
            elif choice == '4':
                reminders = self.reminder_manager.get_reminders(username)
                print("Your Reminders:")
                for rem in reminders:
                    print(rem)
            elif choice == '5':
                print("Logging out...")
                break
            else:
                print("Invalid option. Please try again.")

class UserManager:
    def __init__(self, filename):
        self.filename = filename
        self.load_users()

    def load_users(self):
        self.users = {}
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    username, password = line.strip().split('|')
                    self.users[username] = password

    def register(self, username: str, password: str) -> bool:
        if username in self.users:
            return False
        self.users[username] = password
        with open(self.filename, 'a') as file:
            file.write(f"{username}|{password}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

class TestResultManager:
    def __init__(self, filename):
        self.filename = filename
        self.load_results()

    def load_results(self):
        self.results = {}
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    username, result = line.strip().split('|')
                    if username not in self.results:
                        self.results[username] = []
                    self.results[username].append(result)

    def add_result(self, username: str, result: str) -> bool:
        if username not in self.results:
            self.results[username] = []
        self.results[username].append(result)
        with open(self.filename, 'a') as file:
            file.write(f"{username}|{result}\n")
        return True

    def get_results(self, username: str) -> list:
        return self.results.get(username, [])

class ReminderManager:
    def __init__(self, filename):
        self.filename = filename
        self.load_reminders()

    def load_reminders(self):
        self.reminders = {}
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    username, reminder = line.strip().split('|')
                    if username not in self.reminders:
                        self.reminders[username] = []
                    self.reminders[username].append(reminder)

    def set_reminder(self, username: str, reminder: str) -> bool:
        if username not in self.reminders:
            self.reminders[username] = []
        self.reminders[username].append(reminder)
        with open(self.filename, 'a') as file:
            file.write(f"{username}|{reminder}\n")
        return True

    def get_reminders(self, username: str) -> list:
        return self.reminders.get(username, [])

if __name__ == "__main__":
    app = Main()
    app.main()
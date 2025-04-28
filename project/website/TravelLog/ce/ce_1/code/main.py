from UserManager import UserManager
from EntryManager import EntryManager

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.entry_manager = EntryManager()

    def main(self):
        self.user_manager.load_users()
        self.entry_manager.load_entries()
        print("Welcome to Travel_Log!")
        # Here you would add the logic for user interaction, like showing login/register options.

if __name__ == "__main__":
    app = Main()
    app.main()
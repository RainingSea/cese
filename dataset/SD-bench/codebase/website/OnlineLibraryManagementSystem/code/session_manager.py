from user_manager import UserManager

class SessionManager:
    def __init__(self):
        self.current_user = None
        self.user_manager = UserManager()
        self.user_manager.load_users()

    def login(self, username: str, password: str) -> bool:
        user = self.user_manager.find_user(username)
        if user and user.password == password and user.active:
            self.current_user = user
            return True
        return False

    def logout(self) -> None:
        self.current_user = None

    def get_current_user(self):
        return self.current_user
from flask import session

class SessionManager:
    def is_logged_in(self) -> bool:
        return 'username' in session

    def get_current_user(self) -> str:
        return session.get('username', '')
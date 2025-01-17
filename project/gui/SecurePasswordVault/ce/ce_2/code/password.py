class Password:
    def __init__(self, service: str, username: str, encrypted_password: str) -> None:
        self.service = service
        self.username = username
        self.encrypted_password = encrypted_password
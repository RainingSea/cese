class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email
        self.applied_jobs = []

    def to_dict(self) -> dict:
        return {
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'applied_jobs': self.applied_jobs
        }
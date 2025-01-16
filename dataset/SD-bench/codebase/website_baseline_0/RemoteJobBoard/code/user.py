class User:
    def __init__(self, username='', password='', email=''):
        self.username = username
        self.password = password
        self.email = email
        self.applied_jobs = []

    def save(self):
        with open('users.txt', 'a') as f:
            f.write(f"{self.username}|{self.password}|{self.email}|{','.join(self.applied_jobs)}\n")

    @staticmethod
    def load_users():
        users = []
        try:
            with open('users.txt', 'r') as f:
                for line in f:
                    username, password, email, applied_jobs = line.strip().split('|')
                    user = User(username, password, email)
                    user.applied_jobs = applied_jobs.split(',') if applied_jobs else []
                    users.append(user)
        except FileNotFoundError:
            pass
        return users
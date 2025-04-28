class UserManager:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        users = []
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password, email = line.strip().split(',')
                    users.append({'username': username, 'password': password, 'email': email})
        except FileNotFoundError:
            pass
        return users

    def register(self, username: str, password: str, email: str) -> bool:
        if any(user['username'] == username for user in self.users):
            return False
        self.users.append({'username': username, 'password': password, 'email': email})
        with open('users.txt', 'a') as file:
            file.write(f"{username},{password},{email}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        return any(user['username'] == username and user['password'] == password for user in self.users)

    def get_user_profile(self, username: str) -> dict:
        for user in self.users:
            if user['username'] == username:
                return user
        return {}

class JobManager:
    def __init__(self):
        self.jobs = self.load_jobs()

    def load_jobs(self):
        jobs = []
        try:
            with open('jobs.txt', 'r') as file:
                for line in file:
                    job_title, company_name, job_description, username = line.strip().split(',')
                    jobs.append({'job_title': job_title, 'company_name': company_name, 'job_description': job_description, 'username': username})
        except FileNotFoundError:
            pass
        return jobs

    def post_job(self, job_title: str, company_name: str, job_description: str, username: str) -> bool:
        self.jobs.append({'job_title': job_title, 'company_name': company_name, 'job_description': job_description, 'username': username})
        with open('jobs.txt', 'a') as file:
            file.write(f"{job_title},{company_name},{job_description},{username}\n")
        return True

    def get_all_jobs(self) -> list:
        return self.jobs

    def apply_for_job(self, username: str, job_title: str) -> bool:
        with open('applied_jobs.txt', 'a') as file:
            file.write(f"{username},{job_title}\n")
        return True

class Main:
    def __init__(self):
        self.user_manager = UserManager()
        self.job_manager = JobManager()

    def main(self):
        # This would be the entry point for the web application
        pass

if __name__ == "__main__":
    app = Main()
    app.main()
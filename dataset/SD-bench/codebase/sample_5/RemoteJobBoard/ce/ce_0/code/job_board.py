from user import User
from job import Job

class JobBoard:
    def __init__(self, users_file: str, jobs_file: str, applied_jobs_file: str):
        self.users_file = users_file
        self.jobs_file = jobs_file
        self.applied_jobs_file = applied_jobs_file
        self.load_users()
        self.load_jobs()

    def load_users(self):
        self.users = {}
        try:
            with open(self.users_file, 'r') as file:
                for line in file:
                    username, password, email = line.strip().split('|')
                    self.users[username] = User(username, password, email)
        except FileNotFoundError:
            pass

    def load_jobs(self):
        self.jobs = []
        try:
            with open(self.jobs_file, 'r') as file:
                for line in file:
                    title, company, description = line.strip().split('|')
                    self.jobs.append(Job(title, company, description))
        except FileNotFoundError:
            pass

    def register_user(self, username: str, password: str, email: str) -> bool:
        if username in self.users:
            return False
        new_user = User(username, password, email)
        self.users[username] = new_user
        with open(self.users_file, 'a') as file:
            file.write(f"{username}|{password}|{email}\n")
        return True

    def login_user(self, username: str, password: str) -> bool:
        user = self.users.get(username)
        return user is not None and user.password == password

    def post_job(self, job: Job) -> None:
        self.jobs.append(job)
        with open(self.jobs_file, 'a') as file:
            file.write(f"{job.title}|{job.company}|{job.description}\n")

    def get_featured_jobs(self) -> list:
        return self.jobs[:5]  # Return the first 5 jobs as featured

    def browse_jobs(self) -> list:
        return self.jobs

    def apply_for_job(self, username: str, job_title: str) -> None:
        user = self.users.get(username)
        if user:
            user.applied_jobs.append(job_title)
            with open(self.applied_jobs_file, 'a') as file:
                file.write(f"{username}|{job_title}\n")

    def get_user_profile(self, username: str) -> User:
        return self.users.get(username)
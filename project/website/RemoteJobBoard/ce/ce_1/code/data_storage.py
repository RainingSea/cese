import json

class DataStorage:
    def save_user(self, user):
        users = self.load_users()
        users[user.username] = {'password': user.password, 'email': user.email}
        with open('users.txt', 'w') as f:
            json.dump(users, f)
        return True

    def load_users(self):
        try:
            with open('users.txt', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_job(self, job):
        jobs = self.load_jobs()
        jobs.append({'title': job.title, 'company': job.company, 'description': job.description})
        with open('jobs.txt', 'w') as f:
            json.dump(jobs, f)
        return True

    def load_jobs(self):
        try:
            with open('jobs.txt', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_applied_job(self, username: str, job_title: str) -> bool:
        applied_jobs = self.load_applied_jobs(username)
        applied_jobs.append(job_title)
        with open('applied_jobs.txt', 'w') as f:
            json.dump({username: applied_jobs}, f)
        return True

    def load_applied_jobs(self, username: str):
        try:
            with open('applied_jobs.txt', 'r') as f:
                applied_jobs = json.load(f)
                return applied_jobs.get(username, [])
        except FileNotFoundError:
            return []
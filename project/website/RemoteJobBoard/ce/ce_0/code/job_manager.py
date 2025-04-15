class JobManager:
    def __init__(self):
        self.jobs = []

    def load_jobs(self) -> None:
        try:
            with open('jobs.txt', 'r') as file:
                for line in file:
                    title, company, description = line.strip().split('|')
                    self.jobs.append({'title': title, 'company': company, 'description': description})
        except FileNotFoundError:
            pass

    def save_jobs(self) -> None:
        with open('jobs.txt', 'w') as file:
            for job in self.jobs:
                file.write(f"{job['title']}|{job['company']}|{job['description']}\n")

    def post_job(self, title: str, company: str, description: str) -> bool:
        self.jobs.append({'title': title, 'company': company, 'description': description})
        self.save_jobs()
        return True

    def get_jobs(self) -> list:
        return self.jobs

    def apply_for_job(self, username: str, job_id: int) -> bool:
        if job_id < len(self.jobs):
            application_manager.record_application(username, job_id)
            return True
        return False
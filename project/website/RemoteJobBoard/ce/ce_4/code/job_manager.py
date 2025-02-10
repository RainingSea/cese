from models import Job

class JobManager:
    def __init__(self, jobs_file: str):
        self.jobs_file = jobs_file
        self.jobs = self.load_jobs()

    def load_jobs(self) -> list:
        jobs = []
        try:
            with open(self.jobs_file, 'r') as file:
                for line in file:
                    title, company, description = line.strip().split('|')
                    jobs.append(Job(title, company, description))
        except FileNotFoundError:
            pass
        return jobs

    def post_job(self, title: str, company: str, description: str) -> bool:
        new_job = Job(title, company, description)
        self.jobs.append(new_job)
        with open(self.jobs_file, 'a') as file:
            file.write(new_job.to_string() + '\n')
        return True

    def get_all_jobs(self) -> list:
        return self.jobs

    def apply_for_job(self, username: str, job_title: str) -> bool:
        for job in self.jobs:
            if job.title == job_title:
                job.applied_jobs.append(username)
                return True
        return False
from job import Job
from user import User

class JobBoard:
    def browse_jobs(self):
        return Job.load_jobs()

    def post_job(self, job: Job):
        job.save()

    def apply_for_job(self, job_id: int, user: User):
        with open('applied_jobs.txt', 'a') as file:
            file.write(f"{user.username}|{job_id}\n")
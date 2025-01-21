from data_storage import DataStorage
from uuid import uuid4

class Job:
    def __init__(self, job_id: str, title: str, company: str, description: str):
        self.job_id = job_id
        self.title = title
        self.company = company
        self.description = description

    def save(self) -> None:
        """Saves the job to the data storage."""
        DataStorage.write_job(self.job_id, self.title, self.company, self.description)

    @staticmethod
    def load_all() -> list:
        """Loads all jobs from the data storage."""
        jobs = DataStorage.read_jobs()
        return [Job(job[0], job[1], job[2], job[3]) for job in jobs]

    @staticmethod
    def load_by_id(job_id: str) -> 'Job':
        """Loads a job by its ID."""
        jobs = DataStorage.read_jobs()
        for job in jobs:
            if job[0] == job_id:
                return Job(job[0], job[1], job[2], job[3])
        return None

class JobBoard:
    @staticmethod
    def browse_jobs() -> list:
        """Browses all available jobs."""
        return Job.load_all()

    @staticmethod
    def post_job(title: str, company: str, description: str) -> None:
        """Posts a new job to the job board."""
        job_id = str(uuid4())
        new_job = Job(job_id, title, company, description)
        new_job.save()
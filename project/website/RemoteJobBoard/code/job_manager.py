class JobManager:
    def __init__(self, jobs_file: str):
        self.jobs_file = jobs_file
        self.load_jobs()

    def load_jobs(self):
        self.jobs = []
        with open(self.jobs_file, 'r') as file:
            for line in file:
                job_id, title, description = line.strip().split('|')
                self.jobs.append({'id': int(job_id), 'title': title, 'description': description})

    def post_job(self, job_details: dict) -> bool:
        job_id = len(self.jobs) + 1
        self.jobs.append({'id': job_id, **job_details})
        with open(self.jobs_file, 'a') as file:
            file.write(f"{job_id}|{job_details['title']}|{job_details['description']}\n")
        return True

    def get_all_jobs(self) -> list:
        return self.jobs

    def apply_for_job(self, username: str, job_id: int) -> bool:
        return True
class JobManager:
    def __init__(self, job_file: str):
        self.job_file = job_file
        self.load_jobs()

    def load_jobs(self):
        self.jobs = []
        try:
            with open(self.job_file, 'r') as file:
                for line in file:
                    job_id, job_title, company_name, job_description = line.strip().split('|')
                    self.jobs.append({'id': int(job_id), 'title': job_title, 'company': company_name, 'description': job_description})
        except FileNotFoundError:
            open(self.job_file, 'w').close()  # Create file if it doesn't exist

    def post_job(self, job_title: str, company_name: str, job_description: str) -> bool:
        job_id = len(self.jobs) + 1
        self.jobs.append({'id': job_id, 'title': job_title, 'company': company_name, 'description': job_description})
        with open(self.job_file, 'a') as file:
            file.write(f"{job_id}|{job_title}|{company_name}|{job_description}\n")
        return True

    def get_all_jobs(self) -> list:
        return self.jobs

    def apply_for_job(self, username: str, job_id: int) -> bool:
        # Here we would normally save the application, but for simplicity, we will just return True
        return True
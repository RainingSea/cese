class JobManager:
    def __init__(self, jobs_file: str):
        self.jobs_file = jobs_file
        self.load_jobs()

    def load_jobs(self):
        self.jobs = []
        try:
            with open(self.jobs_file, 'r') as file:
                for line in file:
                    job_id, title, company, description = line.strip().split('|')
                    self.jobs.append({
                        'id': int(job_id),
                        'title': title,
                        'company': company,
                        'description': description
                    })
        except FileNotFoundError:
            pass

    def post_job(self, title: str, company: str, description: str) -> bool:
        job_id = len(self.jobs) + 1
        self.jobs.append({'id': job_id, 'title': title, 'company': company, 'description': description})
        with open(self.jobs_file, 'a') as file:
            file.write(f"{job_id}|{title}|{company}|{description}\n")
        return True

    def get_jobs(self) -> list:
        return self.jobs

    def apply_for_job(self, username: str, job_id: int) -> bool:
        # Placeholder for application logic
        return True
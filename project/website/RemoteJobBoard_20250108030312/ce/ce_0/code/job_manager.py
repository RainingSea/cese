class JobManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.load_jobs()

    def load_jobs(self):
        self.jobs = []
        with open(self.file_path, 'r') as file:
            for line in file:
                job_title, company_name, job_description = line.strip().split('|')
                self.jobs.append({"job_title": job_title, "company_name": company_name, "job_description": job_description})

    def post_job(self, job_title: str, company_name: str, job_description: str) -> bool:
        with open(self.file_path, 'a') as file:
            file.write(f"{job_title}|{company_name}|{job_description}\n")
        self.jobs.append({"job_title": job_title, "company_name": company_name, "job_description": job_description})
        return True

    def get_all_jobs(self) -> list:
        return self.jobs
class JobManager:
    def __init__(self):
        self.jobs = []

    def load_jobs(self):
        try:
            with open('jobs.txt', 'r') as file:
                for line in file:
                    title, company, description = line.strip().split('|')
                    self.jobs.append({"title": title, "company": company, "description": description})
        except FileNotFoundError:
            with open('jobs.txt', 'w') as file:
                pass  # Create the file if it doesn't exist

    def add_job(self, title: str, company: str, description: str) -> None:
        job = {"title": title, "company": company, "description": description}
        self.jobs.append(job)
        with open('jobs.txt', 'a') as file:
            file.write(f"{title}|{company}|{description}\n")

    def get_jobs(self) -> list:
        return self.jobs

    def apply_for_job(self, username: str, job_id: int) -> bool:
        if job_id < len(self.jobs):
            # Job application logic can be implemented here
            return True
        return False
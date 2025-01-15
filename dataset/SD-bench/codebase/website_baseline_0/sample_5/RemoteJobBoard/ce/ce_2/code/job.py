class Job:
    def __init__(self):
        self.jobs_file = 'jobs.txt'
        self.load_jobs()

    def load_jobs(self) -> list:
        jobs = []
        with open(self.jobs_file, 'r') as file:
            for line in file:
                title, company, description = line.strip().split('|')
                jobs.append({'title': title, 'company': company, 'description': description})
        return jobs

    def save(self, title: str, company: str, description: str) -> None:
        with open(self.jobs_file, 'a') as file:
            file.write(f"{title}|{company}|{description}\n")
class Job:
    def __init__(self, title: str = '', company: str = '', description: str = ''):
        self.title = title
        self.company = company
        self.description = description

    def save(self, title: str, company: str, description: str) -> None:
        with open('jobs.txt', 'a') as file:
            file.write(f"{title}|{company}|{description}\n")

    def load_all(self) -> list:
        jobs = []
        with open('jobs.txt', 'r') as file:
            for line in file:
                job_data = line.strip().split('|')
                jobs.append(Job(job_data[0], job_data[1], job_data[2]))
        return jobs
class Job:
    def __init__(self, title: str, company: str, description: str):
        self.title = title
        self.company = company
        self.description = description

    def save(self) -> None:
        with open('jobs.txt', 'a') as f:
            f.write(f"{self.title}|{self.company}|{self.description}\n")

    @staticmethod
    def load_all() -> list:
        jobs = []
        with open('jobs.txt', 'r') as f:
            for line in f:
                title, company, description = line.strip().split('|')
                jobs.append(Job(title, company, description))
        return jobs
class Job:
    def __init__(self, title: str, company: str, description: str):
        self.title = title
        self.company = company
        self.description = description

    def save(self):
        with open('jobs.txt', 'a') as file:
            file.write(f"{self.title}|{self.company}|{self.description}\n")

    @staticmethod
    def load_jobs() -> list:
        jobs = []
        try:
            with open('jobs.txt', 'r') as file:
                for line in file:
                    title, company, description = line.strip().split('|')
                    jobs.append(Job(title, company, description))
        except Exception as e:
            print(f"Error loading jobs: {e}")
        return jobs
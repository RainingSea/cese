class Job:
    def __init__(self, title='', company='', description=''):
        self.title = title
        self.company = company
        self.description = description

    def save(self):
        with open('jobs.txt', 'a') as f:
            f.write(f"{self.title}|{self.company}|{self.description}\n")

    @staticmethod
    def load_jobs():
        jobs = []
        try:
            with open('jobs.txt', 'r') as f:
                for line in f:
                    title, company, description = line.strip().split('|')
                    jobs.append(Job(title, company, description))
        except FileNotFoundError:
            pass
        return jobs
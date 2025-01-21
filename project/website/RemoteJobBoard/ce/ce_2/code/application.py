class Application:
    def __init__(self, username: str, job_title: str):
        self.username = username
        self.job_title = job_title

    def save(self):
        with open('applied_jobs.txt', 'a') as file:
            file.write(f"{self.username}|{self.job_title}\n")

    @staticmethod
    def load_applications():
        applications = []
        with open('applied_jobs.txt', 'r') as file:
            for line in file:
                username, job_title = line.strip().split('|')
                applications.append(Application(username, job_title))
        return applications
class ApplicationManager:
    def __init__(self):
        self.applications = []

    def load_applications(self) -> None:
        try:
            with open('applications.txt', 'r') as file:
                for line in file:
                    username, job_id = line.strip().split('|')
                    self.applications.append({'username': username, 'job_id': int(job_id)})
        except FileNotFoundError:
            pass

    def save_applications(self) -> None:
        with open('applications.txt', 'w') as file:
            for application in self.applications:
                file.write(f"{application['username']}|{application['job_id']}\n")

    def record_application(self, username: str, job_id: int) -> None:
        self.applications.append({'username': username, 'job_id': job_id})
        self.save_applications()
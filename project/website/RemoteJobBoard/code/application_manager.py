class ApplicationManager:
    def __init__(self, applications_file: str):
        self.applications_file = applications_file

    def record_application(self, username: str, job_id: int) -> bool:
        with open(self.applications_file, 'a') as file:
            file.write(f"{username}|{job_id}\n")
        return True
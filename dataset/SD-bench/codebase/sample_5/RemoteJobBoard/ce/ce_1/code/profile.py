class Profile:
    def __init__(self, user):
        self.user = user
        self.applied_jobs = []

    def view_profile(self) -> dict:
        return {
            'username': self.user.username,
            'applied_jobs': self.applied_jobs
        }

    def edit_profile(self, new_username: str, new_password: str):
        self.user.username = new_username
        self.user.password = new_password
        # Save changes back to the user file if needed

    def apply_job(self, job):
        self.applied_jobs.append(job.title)
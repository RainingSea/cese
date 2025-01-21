import os

class DataStorage:
    @staticmethod
    def read_users() -> list:
        """Reads users from the users.txt file."""
        users = []
        if os.path.exists('users.txt'):
            with open('users.txt', 'r') as file:
                for line in file:
                    username, password, email = line.strip().split('|')
                    users.append((username, password, email))
        return users

    @staticmethod
    def write_user(username: str, password: str, email: str) -> None:
        """Writes a new user to the users.txt file."""
        if username and password and email:
            with open('users.txt', 'a') as file:
                file.write(f"{username}|{password}|{email}\n")

    @staticmethod
    def read_jobs() -> list:
        """Reads jobs from the jobs.txt file."""
        jobs = []
        if os.path.exists('jobs.txt'):
            with open('jobs.txt', 'r') as file:
                for line in file:
                    job_id, title, company, description = line.strip().split('|')
                    jobs.append((job_id, title, company, description))
        return jobs

    @staticmethod
    def write_job(job_id: str, title: str, company: str, description: str) -> None:
        """Writes a new job to the jobs.txt file."""
        if job_id and title and company and description:
            with open('jobs.txt', 'a') as file:
                file.write(f"{job_id}|{title}|{company}|{description}\n")

    @staticmethod
    def write_application(user_id: str, job_id: str) -> None:
        """Writes a job application to the applications.txt file."""
        if user_id and job_id:
            with open('applications.txt', 'a') as file:
                file.write(f"{user_id}|{job_id}\n")

    @staticmethod
    def read_applications() -> list:
        """Reads job applications from the applications.txt file."""
        applications = []
        if os.path.exists('applications.txt'):
            with open('applications.txt', 'r') as file:
                for line in file:
                    user_id, job_id = line.strip().split('|')
                    applications.append((user_id, job_id))
        return applications

    @staticmethod
    def update_user(username: str, new_password: str, new_email: str) -> None:
        """Updates the user's information in the users.txt file."""
        users = DataStorage.read_users()
        with open('users.txt', 'w') as file:
            for user in users:
                if user[0] == username:
                    file.write(f"{username}|{new_password}|{new_email}\n")
                else:
                    file.write(f"{user[0]}|{user[1]}|{user[2]}\n")
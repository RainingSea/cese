from user import User

class Profile:
    @staticmethod
    def view_profile(username):
        users = User.load_users()
        for user in users:
            if user.username == username:
                return {
                    'username': user.username,
                    'email': user.email,
                    'applied_jobs': user.applied_jobs
                }
        return {}

    @staticmethod
    def edit_profile(username, email):
        users = User.load_users()
        for user in users:
            if user.username == username:
                user.email = email
                # Save updated user data back to file
                with open('users.txt', 'w') as f:
                    for u in users:
                        f.write(f"{u.username}|{u.password}|{u.email}|{','.join(u.applied_jobs)}\n")
                break

    @staticmethod
    def apply_job(username, job_title):
        users = User.load_users()
        for user in users:
            if user.username == username:
                user.applied_jobs.append(job_title)
                # Save updated user data back to file
                with open('users.txt', 'w') as f:
                    for u in users:
                        f.write(f"{u.username}|{u.password}|{u.email}|{','.join(u.applied_jobs)}\n")
                break
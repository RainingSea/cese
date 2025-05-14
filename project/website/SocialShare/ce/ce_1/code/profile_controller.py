import os

class ProfileController:
    def __init__(self):
        self.profiles_file = "profiles.txt"
        if not os.path.exists(self.profiles_file):
            open(self.profiles_file, 'w').close()

    def get_profile(self, username):
        with open(self.profiles_file, 'r') as f:
            for line in f:
                profile_username, bio, personal_info = line.strip().split('|')
                if profile_username == username:
                    return {
                        'username': profile_username,
                        'bio': bio,
                        'personal_info': personal_info
                    }
        return {
            'username': username,
            'bio': '',
            'personal_info': ''
        }

    def update_profile(self, username, bio, personal_info):
        profiles = []
        found = False
        
        if os.path.exists(self.profiles_file):
            with open(self.profiles_file, 'r') as f:
                for line in f:
                    profile_username, _, _ = line.strip().split('|')
                    if profile_username == username:
                        profiles.append(f"{username}|{bio}|{personal_info}\n")
                        found = True
                    else:
                        profiles.append(line)
        
        if not found:
            profiles.append(f"{username}|{bio}|{personal_info}\n")
        
        with open(self.profiles_file, 'w') as f:
            f.writelines(profiles)
        return True
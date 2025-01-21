import json

class UserProfileManager:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.profiles = self.load_profiles()

    def load_profiles(self) -> list:
        try:
            with open(self.file_path, 'r') as file:
                return [json.loads(line) for line in file.readlines()]
        except FileNotFoundError:
            return []

    def create_profile(self, user_data: dict) -> None:
        self.profiles.append(user_data)
        self._save_profiles()

    def update_profile(self, user_data: dict) -> None:
        for index, profile in enumerate(self.profiles):
            if profile['username'] == user_data['username']:
                self.profiles[index] = user_data
                break
        self._save_profiles()

    def get_profiles(self) -> list:
        return self.profiles

    def _save_profiles(self) -> None:
        with open(self.file_path, 'w') as file:
            for profile in self.profiles:
                file.write(json.dumps(profile) + '\n')
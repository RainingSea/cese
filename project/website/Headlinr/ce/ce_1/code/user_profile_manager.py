import json

class UserProfileManager:
    def __init__(self):
        self.user_profiles = self.load_profiles()

    def load_profiles(self) -> dict:
        """
        Loads user profiles from a text file.

        Returns:
            dict: Dictionary of user profiles.
        """
        profiles = {}
        try:
            with open('users.txt', 'r') as file:
                for line in file:
                    user_id, preferences = line.strip().split('|')
                    profiles[user_id] = json.loads(preferences)
        except FileNotFoundError:
            pass
        return profiles

    def save_profiles(self) -> None:
        """
        Saves user profiles to a text file.
        """
        with open('users.txt', 'w') as file:
            for user_id, preferences in self.user_profiles.items():
                file.write(f"{user_id}|{json.dumps(preferences)}\n")

    def update_profile(self, user_id: str, preferences: dict) -> None:
        """
        Updates a user profile with new preferences.

        Args:
            user_id (str): The ID of the user to update.
            preferences (dict): The new preferences for the user.
        """
        self.user_profiles[user_id] = preferences
        self.save_profiles()
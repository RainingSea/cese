class Preferences:
    def __init__(self, budget: float, activities: list, climate: str):
        self.budget = budget
        self.activities = activities
        self.climate = climate

    def save(self, username: str) -> None:
        with open('preferences.txt', 'a') as file:
            activities_str = ','.join(self.activities)
            file.write(f"{username}|{self.budget}|{activities_str}|{self.climate}\n")

    @staticmethod
    def load(username: str) -> 'Preferences':
        with open('preferences.txt', 'r') as file:
            for line in file:
                pref_data = line.strip().split('|')
                if pref_data[0] == username:
                    activities = pref_data[2].split(',')
                    return Preferences(float(pref_data[1]), activities, pref_data[3])
        return None
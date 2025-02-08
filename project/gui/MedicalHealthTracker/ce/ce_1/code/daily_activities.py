class DailyActivities:
    def __init__(self):
        self.file_path = 'daily_activities.txt'

    def add_activity(self, activity: str):
        with open(self.file_path, 'a') as file:
            file.write(activity + '\n')

    def load_activities(self):
        with open(self.file_path, 'r') as file:
            return file.read().splitlines()
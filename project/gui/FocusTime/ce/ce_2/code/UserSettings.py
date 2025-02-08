import os

class UserSettings:
    def __init__(self, settings_file: str):
        self.settings_file = settings_file
        self.default_work_duration = 25  # default work duration in minutes
        self.default_break_duration = 5   # default break duration in minutes

    def load_settings(self) -> dict:
        settings = {}
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as file:
                for line in file:
                    key, value = line.strip().split('|')
                    settings[key] = int(value)
        else:
            settings['work_duration'] = self.default_work_duration
            settings['break_duration'] = self.default_break_duration
        return settings

    def save_settings(self, work_duration: int, break_duration: int):
        with open(self.settings_file, 'w') as file:
            file.write(f'work_duration|{work_duration}\n')
            file.write(f'break_duration|{break_duration}\n')
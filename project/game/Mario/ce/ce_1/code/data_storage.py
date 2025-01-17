import os

SCORES_FILE = 'scores.txt'
SETTINGS_FILE = 'settings.txt'

def save_score(score):
    with open(SCORES_FILE, 'a') as file:
        file.write(f"{score}\n")

def load_scores():
    if not os.path.exists(SCORES_FILE):
        return []
    with open(SCORES_FILE, 'r') as file:
        return [int(line.strip()) for line in file.readlines()]

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as file:
        for key, value in settings.items():
            file.write(f"{key}|{value}\n")

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {}
    settings = {}
    with open(SETTINGS_FILE, 'r') as file:
        for line in file:
            key, value = line.strip().split('|')
            settings[key] = value
    return settings
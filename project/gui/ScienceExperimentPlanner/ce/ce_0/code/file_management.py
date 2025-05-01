import os

def save_to_file(experiment_data: dict, filename: str) -> None:
    with open(filename, 'w') as file:
        for key, value in experiment_data.items():
            file.write(f'{key}|{value}\n')

def load_from_file(filename: str) -> dict:
    experiment_data = {}
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            for line in file:
                key, value = line.strip().split('|')
                experiment_data[key] = value
    return experiment_data
import os

def load_data(filename: str):
    if not os.path.exists(filename):
        return None
    with open(filename, 'r') as file:
        return file.read().strip()

def save_data(filename: str, data: str) -> None:
    with open(filename, 'w') as file:
        file.write(data)
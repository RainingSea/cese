def save_progress(user: str):
    with open('progress.txt', 'a') as f:
        f.write(f"{user}|some_progress_data\n")  # Example of saving progress

def load_progress(user: str):
    with open('progress.txt', 'r') as f:
        for line in f:
            if line.startswith(user):
                return line.strip().split('|')[1]  # Return the progress data
    return None
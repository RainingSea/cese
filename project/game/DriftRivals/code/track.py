import json

class Track:
    def __init__(self):
        self.track_data = {}

    def load_track(self, file_path: str) -> None:
        try:
            with open(file_path, 'r') as f:
                self.track_data = json.load(f)
        except FileNotFoundError:
            print(f"File {file_path} not found. Initializing empty track data.")
            self.track_data = {}
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {file_path}. Initializing empty track data.")
            self.track_data = {}

    def render_track(self) -> None:
        if 'tracks' in self.track_data:
            for track in self.track_data['tracks']:
                print(f"Track Name: {track['name']}, Points: {track['points']}")
        else:
            print("No tracks available to render.")
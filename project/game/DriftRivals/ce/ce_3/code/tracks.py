class Track:
    def __init__(self):
        self.name = ""
        self.corners = []

    def load_track(self, data: str):
        parts = data.split('|')
        self.name = parts[0]
        self.corners = eval(parts[1])  # Convert string representation of list to actual list
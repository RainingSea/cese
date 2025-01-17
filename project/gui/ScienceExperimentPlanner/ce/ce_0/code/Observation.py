import datetime

class Observation:
    def __init__(self, experiment_id: int, note: str, timestamp: str = None):
        self.experiment_id = experiment_id
        self.note = note
        self.timestamp = timestamp if timestamp else datetime.datetime.now().isoformat()
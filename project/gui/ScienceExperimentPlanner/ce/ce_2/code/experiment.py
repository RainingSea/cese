class Experiment:
    def __init__(self, objective: str, materials: str, procedure: str):
        self.objective = objective
        self.materials = materials
        self.procedure = procedure
        self.status = "In Progress"

    def update_status(self, status: str):
        self.status = status

    def to_string(self) -> str:
        return f"{self.objective}|{self.materials}|{self.procedure}|{self.status}"
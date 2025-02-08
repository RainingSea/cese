class Experiment:
    def __init__(self, id: int, objectives: str, materials: str, procedure: str):
        self.id = id
        self.objectives = objectives
        self.materials = materials
        self.procedure = procedure
        self.status = "Not Started"

    def update_status(self, status: str):
        self.status = status
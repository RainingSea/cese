class Experiment:
    def __init__(self, title: str, objectives: str, materials: str, procedures: str) -> None:
        self.title = title
        self.objectives = objectives
        self.materials = materials
        self.procedures = procedures
        self.observations = ""
        self.progress = ""

    def record_observation(self, observation: str) -> None:
        self.observations += observation + "\n"

    def update_progress(self, progress: str) -> None:
        self.progress = progress

    def to_string(self) -> str:
        return f"Title: {self.title}\nObjectives: {self.objectives}\nMaterials: {self.materials}\nProcedures: {self.procedures}\nObservations: {self.observations}\nProgress: {self.progress}\n"
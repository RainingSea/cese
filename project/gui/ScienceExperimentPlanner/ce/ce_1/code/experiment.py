class Experiment:
    def __init__(self, title: str, objectives: str, materials: str, procedures: str, expected_results: str) -> None:
        self.title = title
        self.objectives = objectives
        self.materials = materials
        self.procedures = procedures
        self.expected_results = expected_results
        self.progress = ""
        self.observations = []

    def add_observation(self, observation: str) -> None:
        self.observations.append(observation)

    def update_progress(self, progress: str) -> None:
        self.progress = progress

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "objectives": self.objectives,
            "materials": self.materials,
            "procedures": self.procedures,
            "expected_results": self.expected_results,
            "progress": self.progress,
            "observations": self.observations
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Experiment':
        experiment = cls(
            title=data["title"],
            objectives=data["objectives"],
            materials=data["materials"],
            procedures=data["procedures"],
            expected_results=data["expected_results"]
        )
        experiment.progress = data.get("progress", "")
        experiment.observations = data.get("observations", [])
        return experiment
class Experiment:
    def __init__(self, title: str, objectives: str, materials: str, procedures: str):
        self.title = title
        self.objectives = objectives
        self.materials = materials
        self.procedures = procedures
        self.status = "Not Started"

    def record_observation(self, observation: str) -> None:
        with open(f'observations/{self.title}_observations.txt', 'a') as obs_file:
            obs_file.write(observation + '\n')

    def get_details(self) -> str:
        return f'Title: {self.title}\nObjectives: {self.objectives}\nMaterials: {self.materials}\nProcedures: {self.procedures}\nStatus: {self.status}'
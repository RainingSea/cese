class ExerciseRoutines:
    def __init__(self):
        self.file_path = 'exercise_routines.txt'

    def add_routine(self, routine: str):
        with open(self.file_path, 'a') as file:
            file.write(routine + '\n')

    def load_routines(self):
        with open(self.file_path, 'r') as file:
            return file.read().splitlines()
class MedicalInfo:
    def __init__(self, diagnoses: list, medications: list, treatments: list):
        self.diagnoses = diagnoses
        self.medications = medications
        self.treatments = treatments

    def add_diagnosis(self, diagnosis: str):
        self.diagnoses.append(diagnosis)

    def add_medication(self, medication: str):
        self.medications.append(medication)

    def add_treatment(self, treatment: str):
        self.treatments.append(treatment)

    def save(self, username: str):
        with open('medical_info.txt', 'a') as file:
            file.write(f"{username}|{','.join(self.diagnoses)}|{','.join(self.medications)}|{','.join(self.treatments)}\n")

    @staticmethod
    def load(username: str):
        medical_info = MedicalInfo([], [], [])
        try:
            with open('medical_info.txt', 'r') as file:
                for line in file:
                    user, diagnoses, medications, treatments = line.strip().split('|')
                    if user == username:
                        medical_info.diagnoses = diagnoses.split(',')
                        medical_info.medications = medications.split(',')
                        medical_info.treatments = treatments.split(',')
                        break
        except FileNotFoundError:
            pass
        return medical_info
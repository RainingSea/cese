class MedicalInfo:
    def __init__(self, username: str):
        self.username = username
        self.diagnoses = []
        self.medications = []
        self.treatments = []

    def add_diagnosis(self, diagnosis: str):
        self.diagnoses.append(diagnosis)

    def add_medication(self, medication: str):
        self.medications.append(medication)

    def add_treatment(self, treatment: str):
        self.treatments.append(treatment)

    def save(self):
        with open('medical_info.txt', 'a') as file:
            file.write(f"{self.username}|{','.join(self.diagnoses)}|{','.join(self.medications)}|{','.join(self.treatments)}\n")

    @staticmethod
    def load(username: str):
        with open('medical_info.txt', 'r') as file:
            for line in file:
                info_data = line.strip().split('|')
                if info_data[0] == username:
                    medical_info = MedicalInfo(info_data[0])
                    medical_info.diagnoses = info_data[1].split(',') if info_data[1] else []
                    medical_info.medications = info_data[2].split(',') if info_data[2] else []
                    medical_info.treatments = info_data[3].split(',') if info_data[3] else []
                    return medical_info
        return None
class MedicalInfo:
    def __init__(self):
        self.diagnoses = []
        self.medications = []
        self.treatments = []

    def add_diagnosis(self, diagnosis: str) -> None:
        self.diagnoses.append(diagnosis)

    def add_medication(self, medication: str) -> None:
        self.medications.append(medication)

    def add_treatment(self, treatment: str) -> None:
        self.treatments.append(treatment)

    def save(self) -> None:
        with open('medical_info.txt', 'w') as f:
            for diagnosis in self.diagnoses:
                f.write(f"Diagnosis: {diagnosis}\n")
            for medication in self.medications:
                f.write(f"Medication: {medication}\n")
            for treatment in self.treatments:
                f.write(f"Treatment: {treatment}\n")

    @staticmethod
    def load() -> 'MedicalInfo':
        info = MedicalInfo()
        try:
            with open('medical_info.txt', 'r') as f:
                for line in f:
                    if line.startswith("Diagnosis:"):
                        info.add_diagnosis(line.split(": ")[1].strip())
                    elif line.startswith("Medication:"):
                        info.add_medication(line.split(": ")[1].strip())
                    elif line.startswith("Treatment:"):
                        info.add_treatment(line.split(": ")[1].strip())
        except FileNotFoundError:
            pass
        return info
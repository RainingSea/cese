class MedicalInfo:
    def __init__(self):
        self.diagnoses = []
        self.medications = []
        self.treatments = []

    def add_diagnosis(self, diagnosis: str) -> None:
        self.diagnoses.append(diagnosis)
        self.save()

    def add_medication(self, medication: str) -> None:
        self.medications.append(medication)
        self.save()

    def add_treatment(self, treatment: str) -> None:
        self.treatments.append(treatment)
        self.save()

    def save(self) -> None:
        with open('medical_info.txt', 'w') as f:
            for diagnosis in self.diagnoses:
                f.write(f"Diagnosis: {diagnosis}\n")
            for medication in self.medications:
                f.write(f"Medication: {medication}\n")
            for treatment in self.treatments:
                f.write(f"Treatment: {treatment}\n")

    def load(self) -> None:
        try:
            with open('medical_info.txt', 'r') as f:
                for line in f:
                    if line.startswith("Diagnosis:"):
                        self.diagnoses.append(line.strip().split(": ")[1])
                    elif line.startswith("Medication:"):
                        self.medications.append(line.strip().split(": ")[1])
                    elif line.startswith("Treatment:"):
                        self.treatments.append(line.strip().split(": ")[1])
        except FileNotFoundError:
            pass
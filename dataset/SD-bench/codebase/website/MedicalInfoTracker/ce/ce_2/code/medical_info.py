class MedicalInfo:
    def __init__(self):
        self.user_data = self.load_medical_info()

    def load_medical_info(self):
        info = {}
        try:
            with open('medical_info.txt', 'r') as file:
                for line in file:
                    username, diagnoses, medications, treatments = line.strip().split('|')
                    info[username] = {
                        'diagnoses': diagnoses.split(','),
                        'medications': medications.split(','),
                        'treatments': treatments.split(',')
                    }
        except FileNotFoundError:
            pass
        return info

    def add_diagnosis(self, username: str, diagnosis: str) -> None:
        if username not in self.user_data:
            self.user_data[username] = {'diagnoses': [], 'medications': [], 'treatments': []}
        self.user_data[username]['diagnoses'].append(diagnosis)
        self.save_medical_info()

    def add_medication(self, username: str, medication: str) -> None:
        if username not in self.user_data:
            self.user_data[username] = {'diagnoses': [], 'medications': [], 'treatments': []}
        self.user_data[username]['medications'].append(medication)
        self.save_medical_info()

    def add_treatment(self, username: str, treatment: str) -> None:
        if username not in self.user_data:
            self.user_data[username] = {'diagnoses': [], 'medications': [], 'treatments': []}
        self.user_data[username]['treatments'].append(treatment)
        self.save_medical_info()

    def view_info(self, username: str) -> dict:
        return self.user_data.get(username, {'diagnoses': [], 'medications': [], 'treatments': []})

    def save_medical_info(self):
        with open('medical_info.txt', 'w') as file:
            for username, data in self.user_data.items():
                file.write(f"{username}|{','.join(data['diagnoses'])}|{','.join(data['medications'])}|{','.join(data['treatments'])}\n")
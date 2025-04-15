from user import User
from medical_info import MedicalInfo
from appointment import Appointment

class DataHandler:
    def save_user(self, user: User) -> None:
        user.save()

    def load_users(self) -> list:
        return User.load_users()

    def save_medical_info(self, info: MedicalInfo) -> None:
        with open('medical_info.txt', 'a') as file:
            for diagnosis in info.diagnoses:
                file.write(f"diagnosis|{diagnosis}\n")
            for medication in info.medications:
                file.write(f"medication|{medication}\n")
            for treatment in info.treatments:
                file.write(f"treatment|{treatment}\n")

    def load_medical_info(self) -> MedicalInfo:
        info = MedicalInfo()
        try:
            with open('medical_info.txt', 'r') as file:
                for line in file:
                    entry_type, value = line.strip().split('|')
                    if entry_type == 'diagnosis':
                        info.add_diagnosis(value)
                    elif entry_type == 'medication':
                        info.add_medication(value)
                    elif entry_type == 'treatment':
                        info.add_treatment(value)
        except FileNotFoundError:
            pass
        return info

    def save_appointment(self, appointment: Appointment) -> None:
        appointment.save()

    def load_appointments(self) -> list:
        return Appointment.load_appointments()
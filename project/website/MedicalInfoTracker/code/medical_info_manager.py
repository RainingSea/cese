class MedicalInfoManager:
    def __init__(self, medical_info_file: str):
        self.medical_info_file = medical_info_file
        self.load_medical_info()

    def load_medical_info(self):
        self.medical_info = {}

        with open(self.medical_info_file, 'r') as file:
            for line in file:
                user_id, info = line.strip().split('|')
                if user_id not in self.medical_info:
                    self.medical_info[user_id] = []
                self.medical_info[user_id].append(info)

    def add_medical_info(self, user_id: str, info: str):
        with open(self.medical_info_file, 'a') as file:
            file.write(f"{user_id}|{info}\n")
        if user_id not in self.medical_info:
            self.medical_info[user_id] = []
        self.medical_info[user_id].append(info)

    def edit_medical_info(self, user_id: str, info_id: int, new_info: str):
        if user_id in self.medical_info and 0 <= info_id < len(self.medical_info[user_id]):
            self.medical_info[user_id][info_id] = new_info
            self.save_medical_info()

    def delete_medical_info(self, user_id: str, info_id: int):
        if user_id in self.medical_info and 0 <= info_id < len(self.medical_info[user_id]):
            del self.medical_info[user_id][info_id]
            self.save_medical_info()

    def save_medical_info(self):
        with open(self.medical_info_file, 'w') as file:
            for user_id, infos in self.medical_info.items():
                for info in infos:
                    file.write(f"{user_id}|{info}\n")

    def get_medical_info(self, user_id: str):
        return self.medical_info.get(user_id, [])
import json
import os

class DataStorage:
    @staticmethod
    def load_vault(vault_name: str):
        file_path = f"vaults/{vault_name}.json"
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return json.load(file)
        return []

    @staticmethod
    def save_vault(vault_name: str, data: list) -> None:
        file_path = f"vaults/{vault_name}.json"
        with open(file_path, 'w') as file:
            json.dump(data, file)

    @staticmethod
    def load_user_data() -> dict:
        if os.path.exists("user_data.json"):
            with open("user_data.json", 'r') as file:
                return json.load(file)
        return {}

    @staticmethod
    def save_user_data(data: dict) -> None:
        with open("user_data.json", 'w') as file:
            json.dump(data, file)
class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "password": self.password,
            "email": self.email
        }

class Project:
    def __init__(self, name: str, description: str, freelancer: str):
        self.name = name
        self.description = description
        self.freelancer = freelancer

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "freelancer": self.freelancer
        }

class Freelancer:
    def __init__(self, name: str, details: str):
        self.name = name
        self.details = details

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "details": self.details
        }
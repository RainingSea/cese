import json
from user import User
from vehicle import Vehicle
from maintenance import Maintenance

class DataManager:
    """Handles data storage and retrieval for users, vehicles, and maintenance records."""
    
    def save_user(self, user: User) -> None:
        """Saves a user to the JSON file."""
        users = self.load_users()
        users.append(user.__dict__)
        with open('users.json', 'w') as f:
            json.dump(users, f)

    def load_users(self) -> list:
        """Loads users from the JSON file."""
        try:
            with open('users.json', 'r') as f:
                users_data = json.load(f)
                return [User(**user) for user in users_data]
        except FileNotFoundError:
            return []

    def save_vehicle(self, vehicle: Vehicle) -> None:
        """Saves a vehicle to the JSON file."""
        vehicles = self.load_vehicles()
        vehicles.append(vehicle.__dict__)
        with open('vehicles.json', 'w') as f:
            json.dump(vehicles, f)

    def load_vehicles(self) -> list:
        """Loads vehicles from the JSON file."""
        try:
            with open('vehicles.json', 'r') as f:
                vehicles_data = json.load(f)
                return [Vehicle(**vehicle) for vehicle in vehicles_data]
        except FileNotFoundError:
            return []

    def save_maintenance(self, maintenance: Maintenance) -> None:
        """Saves maintenance records to the JSON file."""
        maintenance_records = self.load_maintenance(maintenance.vehicle_id)
        maintenance_records.append(maintenance.__dict__)
        with open('maintenance.json', 'w') as f:
            json.dump(maintenance_records, f)

    def load_maintenance(self, vehicle_id: int) -> list:
        """Loads maintenance records for a specific vehicle from the JSON file."""
        try:
            with open('maintenance.json', 'r') as f:
                maintenance_data = json.load(f)
                return [Maintenance(**record) for record in maintenance_data if record['vehicle_id'] == vehicle_id]
        except FileNotFoundError:
            return []
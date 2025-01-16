from equipment import Equipment

class Dashboard:
    def add_equipment(self, equipment: Equipment):
        equipment.save()

    def update_equipment(self, equipment: Equipment):
        # Update logic can be added here if needed
        pass

    def search_equipment(self, query: str) -> list:
        equipment_list = Equipment.load_equipment()
        return [eq for eq in equipment_list if query.lower() in eq.name.lower()]

    def filter_equipment(self, criteria: dict) -> list:
        equipment_list = Equipment.load_equipment()
        filtered_list = equipment_list
        for key, value in criteria.items():
            filtered_list = [eq for eq in filtered_list if getattr(eq, key) == value]
        return filtered_list
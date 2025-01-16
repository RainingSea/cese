class Alert:
    def __init__(self, equipment_name: str, alert_type: str):
        self.equipment_name = equipment_name
        self.alert_type = alert_type

    def save(self):
        with open('alerts.txt', 'a') as file:
            file.write(f"{self.equipment_name}|{self.alert_type}\n")

    @staticmethod
    def load_alerts() -> list:
        alerts = []
        try:
            with open('alerts.txt', 'r') as file:
                for line in file:
                    equipment_name, alert_type = line.strip().split('|')
                    alerts.append(Alert(equipment_name, alert_type))
        except FileNotFoundError:
            pass
        return alerts
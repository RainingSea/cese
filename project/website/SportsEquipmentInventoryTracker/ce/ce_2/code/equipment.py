class EquipmentManager:
    def __init__(self, equipment_file='equipment.txt'):
        self.equipment_file = equipment_file

    def add_item(self, name, type, quantity, condition, location):
        with open(self.equipment_file, 'r') as f:
            lines = f.readlines()
            last_id = int(lines[-1].split('|')[0]) if lines else 0
        new_id = last_id + 1
        with open(self.equipment_file, 'a') as f:
            f.write(f"{new_id}|{name}|{type}|{quantity}|{condition}|{location}|No alerts\n")
        return True

    def update_item(self, id, field, value):
        with open(self.equipment_file, 'r') as f:
            lines = f.readlines()
        
        updated = False
        with open(self.equipment_file, 'w') as f:
            for line in lines:
                parts = line.strip().split('|')
                if parts[0] == str(id):
                    if field == 'name':
                        parts[1] = value
                    elif field == 'type':
                        parts[2] = value
                    elif field == 'quantity':
                        parts[3] = value
                    elif field == 'condition':
                        parts[4] = value
                    elif field == 'location':
                        parts[5] = value
                    elif field == 'alert':
                        parts[6] = value
                    updated = True
                    line = '|'.join(parts) + '\n'
                f.write(line)
        return updated

    def search(self, query, filter_type=None):
        results = []
        with open(self.equipment_file, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if (not filter_type or parts[2] == filter_type) and query.lower() in line.lower():
                    results.append({
                        'id': parts[0],
                        'name': parts[1],
                        'type': parts[2],
                        'quantity': parts[3],
                        'condition': parts[4],
                        'location': parts[5],
                        'alert': parts[6]
                    })
        return results

    def set_alert(self, id, alert_msg):
        return self.update_item(id, 'alert', alert_msg)

    def get_all(self):
        return self.search('')
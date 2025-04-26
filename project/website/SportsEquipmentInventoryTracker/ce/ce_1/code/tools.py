import os

def load_users():
    users = {}
    if os.path.exists('users.txt'):
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users[username] = password
    return users

def load_equipment():
    equipment = {}
    if os.path.exists('equipment.txt'):
        with open('equipment.txt', 'r') as file:
            for line in file:
                name, type, quantity, condition, availability, location = line.strip().split(',')
                equipment[name] = {
                    'type': type,
                    'quantity': int(quantity),
                    'condition': condition,
                    'availability': availability.lower() == 'true',
                    'location': location
                }
    return equipment

def save_users(users):
    with open('users.txt', 'w') as file:
        for username, password in users.items():
            file.write(f"{username}|{password}\n")

def save_equipment(equipment):
    with open('equipment.txt', 'w') as file:
        for name, details in equipment.items():
            file.write(f"{name},{details['type']},{details['quantity']},{details['condition']},{details['availability']},{details['location']}\n")
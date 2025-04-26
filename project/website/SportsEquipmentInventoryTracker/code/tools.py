def load_users():
    users = []
    try:
        with open('users.txt', 'r') as file:
            for line in file:
                username, password = line.strip().split('|')
                users.append((username, password))
    except FileNotFoundError:
        pass
    return users

def save_users(users):
    with open('users.txt', 'w') as file:
        for username, password in users:
            file.write(f"{username}|{password}\n")

def load_equipment():
    equipment = []
    try:
        with open('equipment.txt', 'r') as file:
            for line in file:
                name, type_, quantity, condition, location = line.strip().split('|')
                equipment.append((name, type_, int(quantity), condition, location))
    except FileNotFoundError:
        pass
    return equipment

def save_equipment(equipment):
    with open('equipment.txt', 'w') as file:
        for name, type_, quantity, condition, location in equipment:
            file.write(f"{name}|{type_}|{quantity}|{condition}|{location}\n")
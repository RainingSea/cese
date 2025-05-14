class TripManager:
    def __init__(self, file_path='trips.txt'):
        self.file_path = file_path
        self._initialize_file()

    def _initialize_file(self):
        try:
            with open(self.file_path, 'r'):
                pass
        except FileNotFoundError:
            with open(self.file_path, 'w'):
                pass

    def save_trip(self, username, start, destination, date, option):
        if not all([username, start, destination, date, option]):
            return False, "All trip details must be provided"
            
        with open(self.file_path, 'a') as file:
            file.write(f"{username}|{start}|{destination}|{date}|{option}\n")
        return True, "Trip saved successfully"

    def get_saved_trips(self, username):
        trips = []
        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    parts = line.strip().split('|')
                    if parts[0] == username:
                        trips.append({
                            'start': parts[1],
                            'destination': parts[2],
                            'date': parts[3],
                            'option': parts[4]
                        })
        except FileNotFoundError:
            return [], "No trips database found"
        return trips, "Trips retrieved successfully"

    def get_options(self, start, destination):
        if not start or not destination:
            return None, "Start and destination must be provided"
            
        options = {
            'public_transport': {
                'cost': 5.50,
                'time': '45 min',
                'description': 'Bus and subway combination'
            },
            'ride_sharing': {
                'cost': 15.00,
                'time': '25 min',
                'description': 'Direct ride with shared vehicle'
            },
            'walking': {
                'cost': 0.00,
                'time': '90 min',
                'description': 'Walking route'
            }
        }
        
        comparison = self.compare_options(options)
        return comparison, "Options retrieved successfully"

    def compare_options(self, options):
        cheapest = min(options.items(), key=lambda x: x[1]['cost'])
        fastest = min(options.items(), key=lambda x: int(x[1]['time'].split()[0]))
        
        return {
            'cheapest': cheapest[0],
            'fastest': fastest[0],
            'all_options': options
        }
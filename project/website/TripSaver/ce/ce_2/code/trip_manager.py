import json

class TripManager:
    def __init__(self, trips_file, transport_data):
        self.trips_file = trips_file
        self.transport_data = transport_data

    def save_trip(self, user, origin, destination, date):
        try:
            with open(self.trips_file, 'a') as f:
                trip_data = {
                    'user': user,
                    'origin': origin,
                    'destination': destination,
                    'date': date,
                    'options': self.get_transport_options(origin, destination)
                }
                f.write(json.dumps(trip_data) + '\n')
            return True
        except:
            return False

    def get_transport_options(self, origin, destination):
        options = []
        with open(self.transport_data, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if parts[0] == origin and parts[1] == destination:
                    options.append({
                        'type': parts[2],
                        'cost': parts[3],
                        'duration': parts[4]
                    })
        return options

    def compare_options(self, options):
        if not options:
            return {}
        
        comparison = {
            'cheapest': min(options, key=lambda x: float(x['cost'])),
            'fastest': min(options, key=lambda x: x['duration']),
            'all_options': options
        }
        return comparison
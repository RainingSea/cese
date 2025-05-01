import pygame
import random

class Vehicle:
    def __init__(self, name, handling, acceleration, top_speed):
        self.name = name
        self.handling = handling
        self.acceleration = acceleration
        self.top_speed = top_speed
        self.position = 0
        self.speed = 0

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.speed += self.acceleration
        if keys[pygame.K_DOWN]:
            self.speed -= self.acceleration
        if keys[pygame.K_LEFT]:
            self.turn(-self.handling)
        if keys[pygame.K_RIGHT]:
            self.turn(self.handling)
        self.speed = max(0, min(self.speed, self.top_speed))
        self.position += self.speed

    def turn(self, angle):
        # Simplified turning logic for demonstration
        self.position += angle  # Adjust position based on turning angle

    def check_collision(self, obstacles):
        for obstacle in obstacles:
            if self.position >= obstacle['position'] and self.position <= obstacle['position'] + obstacle['width']:
                self.speed = 0  # Stop the vehicle on collision
                print(f"Collision with {obstacle['name']}!")

class Track:
    def __init__(self, name):
        self.name = name
        self.obstacles = []
        self.lap_count = 0

    def load_track(self):
        with open('tracks.txt', 'r') as file:
            for line in file:
                obstacle = line.strip()
                if obstacle:
                    self.obstacles.append({'name': obstacle, 'position': random.randint(100, 700), 'width': 50})

    def check_lap_completion(self, vehicle_position):
        if vehicle_position >= 800:  # Assuming 800 is the finish line
            self.lap_count += 1
            return True
        return False

class Game:
    def __init__(self):
        self.vehicles = []
        self.tracks = []
        self.current_vehicle = None
        self.current_track = None
        self.load_vehicles()
        self.load_tracks()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Racing Game")
        self.laps_completed = 0

    def load_vehicles(self):
        with open('vehicles.txt', 'r') as file:
            for line in file:
                name, handling, acceleration, top_speed = line.strip().split('|')
                vehicle = Vehicle(name, float(handling), float(acceleration), float(top_speed))
                self.vehicles.append(vehicle)

    def load_tracks(self):
        with open('tracks.txt', 'r') as file:
            for line in file:
                track_name = line.strip()
                if track_name:
                    track = Track(track_name)
                    track.load_track()
                    self.tracks.append(track)

    def start_race(self):
        self.current_vehicle = self.select_vehicle()
        self.current_track = self.tracks[0]  # Select the first track for simplicity

    def select_vehicle(self):
        print("Select a vehicle:")
        for index, vehicle in enumerate(self.vehicles):
            print(f"{index + 1}: {vehicle.name} (Acceleration: {vehicle.acceleration})")
        choice = int(input("Enter the number of your choice: ")) - 1
        return self.vehicles[choice] if 0 <= choice < len(self.vehicles) else random.choice(self.vehicles)

    def update(self):
        if self.current_vehicle:
            self.current_vehicle.move()
            for track in self.tracks:
                self.current_vehicle.check_collision(track.obstacles)
                if track.check_lap_completion(self.current_vehicle.position):
                    self.laps_completed += 1
                    print(f"Lap completed! Total laps: {self.laps_completed}")

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def render(self):
        self.screen.fill((0, 0, 0))  # Clear the screen with black
        if self.current_vehicle:
            # Draw the vehicle as a rectangle for simplicity
            pygame.draw.rect(self.screen, (255, 0, 0), (self.current_vehicle.position, 300, 50, 30))
            for track in self.tracks:
                for obstacle in track.obstacles:
                    pygame.draw.rect(self.screen, (0, 255, 0), (obstacle['position'], 300, obstacle['width'], 30))
        pygame.display.flip()  # Update the display

    def save_results(self):
        with open('scores.txt', 'a') as file:
            file.write(f"{self.current_vehicle.name}|{self.laps_completed}\n")
from target import Target

class TargetManager:
    def __init__(self):
        self.targets = [Target() for _ in range(5)]
        self.target_speed = 3  # Default speed

    def set_target_speed(self, speed: int) -> None:
        self.target_speed = speed

    def spawn_target(self) -> None:
        target = Target()
        self.targets.append(target)

    def move_targets(self) -> None:
        for target in self.targets:
            target.move(self.target_speed)

    def reset_targets(self) -> None:
        self.targets = [Target() for _ in range(5)]
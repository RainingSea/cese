class Snake:
    def __init__(self):
        self.positions = [(5, 5), (5, 4), (5, 3)]  # Initial positions of the snake

    def move(self, direction: str) -> None:
        head_x, head_y = self.positions[0]
        if direction == 'UP':
            new_head = (head_x, head_y - 1)
        elif direction == 'DOWN':
            new_head = (head_x, head_y + 1)
        elif direction == 'LEFT':
            new_head = (head_x - 1, head_y)
        elif direction == 'RIGHT':
            new_head = (head_x + 1, head_y)
        else:
            return  # Invalid direction
        
        self.positions.insert(0, new_head)
        self.positions.pop()  # Remove the tail segment

    def grow(self) -> None:
        self.positions.append(self.positions[-1])  # Duplicate the last segment to grow

    def check_self_collision(self) -> bool:
        return len(self.positions) != len(set(self.positions))  # Check for duplicates
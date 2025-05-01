class Snake:
    def __init__(self):
        self.body = [(100, 100), (90, 100), (80, 100)]
        self.direction = (1, 0)  # Start moving to the right

    def move(self):
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0] * 10, head_y + self.direction[1] * 10)
        self.body.insert(0, new_head)  # Insert new head position to body
        self.body.pop()  # Remove last segment of the snake

    def grow(self):
        tail = self.body[-1]
        self.body.append(tail)

    def check_self_collision(self):
        return self.body[0] in self.body[1:]

    def get_head_position(self):
        return self.body[0]
class Agent:
    """Define a vacuum agent"""
    def __init__(self, home, direction):
        """Init the starting location and direction"""
        self.location = home
        self.direction = direction

    def suck_dirt(self, room):
        room.floor.dirt[self.location.x][self.location.y] = 0

    def move_forward(self):
        self.location = self.location.add(self.direction)

    def turn_right(self):
        self.direction.rotate_right()

    def turn_left(self):
        self.direction.rotate_left()

    def turn_off(self):
        pass

    def dirt_sensor(self, room):
        return room.floor.dirt[self.location.x][self.location.y]


    def wall_sensor(self, room):
        next_location = self.location.add(self.direction)
        if (next_location.x > room.wall.width) or (next_location.x < 0) or (next_location.y < 0) or (next_location.y > room.wall.height)
            return 1
        return 0

    def home_sensor(self, room):
        if self.location.equal(room.home):
            return 1
        return 0




class Agent:
    """Define a vacuum agent"""

    def __init__(self, home, direction):
        """Init the starting location and direction"""
        self.location = home
        self.direction = direction
        self.actions_count = 0
        self.suck_count = 0

    def suck_dirt(self, room):
        room.floor.dirt[self.location.x][self.location.y] = 0

    def move_forward(self):
        self.location = self.location.add(self.direction)

    def turn_right(self):
        self.direction.rotate_right()

    def turn_left(self):
        self.direction.rotate_left()

    def turn_off(self):
        #TODO: turn off the agent
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


class SimpleReflexAgent(Agent):
    """A simple memoryless deterministic reflex agent."""

    def run(room):
        while True:
            self.actions_count += 1
            if self.dirt_sensor(room):
                self.suck_dirt(room)
                self.suck_count += 1
            elif self.wall_sensor(room):
                self.turn_right()
            elif self.home_sensor(room):
                self.turn_off()
                break


class RandomizedReflexAgent(Agent):
    """A randmized reflex agent that can choose actions randomly based on sersor reading."""

    def run(room):
        #TODO: run the agent
        while True:
            self.actions_count += 1


class ModelBasedReflexAgent(Agent):
    """A deterministic model-based reflex agent with a small amount (2 to 3 bits) of memory 
    that represents the state. When executing each action, the agent simultaneously updates 
    the state by setting or resetting these bits according to how you specify them. 
    The actions can be based on its current state bits as well as the current percepts."""

    def run(room):
        #TODO: run the agent
        while True:
            self.actions_count += 1
        




























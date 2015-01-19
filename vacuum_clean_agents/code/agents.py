class Agent:
    """Define a vacuum agent"""

    def __init__(self, home, direction):
        """Init the starting location and direction"""
        self.location = home
        self.direction = direction
        self.actions_count = 0
        self.sucks_count = 0
        self.actions = [0]
        self.sucks = [0]

    def suck_dirt(self, room):
        room.floor.dirt[self.location.y][self.location.x] = False

    def move_forward(self):
        self.location = self.location.add(self.direction)

    def turn_right(self):
        self.direction.rotate_right()

    def turn_left(self):
        self.direction.rotate_left()

    def turn_off(self):
        #TODO: turn off the agent
        print "Agent is turned off."

    def dirt_sensor(self, room):
        return room.floor.dirt[self.location.x][self.location.y]

    def wall_sensor(self, room):
        next_location = self.location.add(self.direction)
        return (next_location.x >= room.wall.width) or (next_location.x < 0) or (next_location.y < 0) or (next_location.y >= room.wall.height)
            
    def home_sensor(self, room):
        return self.location.equal(room.home):
  

class SimpleReflexAgent(Agent):
    """A simple memoryless deterministic reflex agent."""

    def run(room):
        while True:
            if self.dirt_sensor(room):
                self.suck_dirt(room)
                self.sucks_count += 1
            elif not self.wall_sensor(room):
                self.move_forward()
                self.location.str()
            elif self.home_sensor(room):
                self.turn_off()
                break
            else:
                self.turn_right()

            self.actions_count += 1
            self.actions.append(self.actions_count)
            self.sucks.append(self.sucks_count)


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


        




























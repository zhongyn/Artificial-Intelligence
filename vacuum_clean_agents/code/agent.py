import random

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
        print "suck_dirt"
        print(self.location)

    def move_forward(self):
        self.location = self.location.add(self.direction)
        print "move_forward"
        print(self.location)

    def turn_right(self):
        print "direction:"
        print(self.direction)
        print "turn_right"
        self.direction = self.direction.rotate_right()
        print(self.direction)

    def turn_left(self):
        print "direction:"
        print(self.direction)
        print "turn_left"
        self.direction = self.direction.rotate_left()
        print(self.direction)

    def turn_off(self):
        #TODO: turn off the agent
        print "Agent is turned off."

    def dirt_sensor(self, room):
        return room.floor.dirt[self.location.y][self.location.x]

    def wall_sensor(self, room):
        next_location = self.location.add(self.direction)
        return (next_location.x >= room.wall.width) or (next_location.x < 0) or (next_location.y < 0) or (next_location.y >= room.wall.height)
            
    def home_sensor(self, room):
        return self.location.equal(room.home)

    def update_performance(self):
        self.actions_count += 1
        self.actions.append(self.actions_count)
        self.sucks.append(self.sucks_count)

    def print_performance(self):
        print "clean cells:", self.sucks_count
        print "actions taken:", self.actions_count

class SimpleReflexAgent(Agent):
    """A simple memoryless deterministic reflex agent."""

    def run(self, room):
        while True:
            if self.dirt_sensor(room):
                self.suck_dirt(room)
                self.sucks_count += 1
            elif not self.wall_sensor(room):
                self.move_forward()
            elif self.home_sensor(room):
                self.turn_off()
                break
            else:
                self.turn_right()

            print
            self.update_performance()
        self.print_performance()

class RandomizedReflexAgent(Agent):
    """A randmized reflex agent that can choose actions randomly based on sersor reading."""

    def random_move(self):
        choice = random.choice(range(3))
        if choice == 0:
            self.turn_right()
        elif choice == 1:
            self.turn_left()
        else:
            self.move_forward()

    def random_turn(self):
        choice = random.choice(range(2))
        if choice == 0:
            self.turn_right()
        else:
            self.turn_left()


    def run(self, room):
        while True:
            if self.dirt_sensor(room):
                self.suck_dirt(room)
                self.sucks_count += 1
            elif not self.wall_sensor(room):
                self.random_move()
            elif self.home_sensor(room):
                self.turn_off()
                break
            else:
                self.random_turn()

            print
            self.update_performance()
        self.print_performance()

class ModelBasedReflexAgent(Agent):
    """A deterministic model-based reflex agent with a small amount (2 to 3 bits) of memory 
    that represents the state. When executing each action, the agent simultaneously updates 
    the state by setting or resetting these bits according to how you specify them. 
    The actions can be based on its current state bits as well as the current percepts."""

    def __init__(self, home, direction):
        Agent.__init__(self, home, direction)
        self.has_turn = False
        self.has_right_turn = False
        self.has_move = True

    def run(self, room):
        while True:
            if self.dirt_sensor(room):
                self.suck_dirt(room)
                self.sucks_count += 1
            elif (not self.wall_sensor(room)):
                if self.has_turn:
                    if self.has_move:
                        if self.has_right_turn:
                            self.turn_right()
                        else:
                            self.turn_left()
                        self.has_turn = False
                    else:
                        self.move_forward()
                        self.has_move = True
                else:
                    self.move_forward()
            else:
                if self.has_turn:
                    if self.has_move:
                        if self.has_right_turn:
                            self.turn_right()
                        else:
                            self.turn_left()
                        self.has_turn = False
                    else:                        
                        self.turn_off()
                        break
                else:
                    if not self.has_right_turn:
                        self.turn_right()
                        self.has_right_turn = True
                    else:
                        self.turn_left()
                        self.has_right_turn = False
                    self.has_turn = True
                    self.has_move = False

            print
            self.update_performance()
        self.print_performance()




















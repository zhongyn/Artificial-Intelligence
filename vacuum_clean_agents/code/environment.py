class Floor:
    """Define a row*cols floor with dirt"""

    def __init__(self, width, height):
        self.dirt = [[True for j in range(width)] for i in range(height)]

class Wall:
    """Define the walls around the room"""

    def __init__(self, width, height):
        self.width = width
        self.height = height

class Environment:
    """A n*m empty rectangular room with floor and walls"""

    def __init__(self, width, height, home):
        self.floor = Floor(width, height)
        self.wall = Wall(width, height)
        self.home = home


        
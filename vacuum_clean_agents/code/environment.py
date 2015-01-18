class Floor:
    """Define a row*cols floor with dirt"""
    def __init__(self, height, width):
        self.dirt = [[1 for j in range(width)] for i in range(height)]

class Wall:
    """Define the walls around the room"""
    def __init__(self, height, width):
        self.width = width
        self.height = height

class Environment:
    """A n*m empty rectangular room with floor and walls"""
    def __init__(self, floor, wall, home):
        self.floor = floor
        self.wall = wall
        self.home = home


        
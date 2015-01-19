class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return 'Vector({self.x}, {self.y})'.format(self=self)

    def add(self, vector):
        return Vector(self.x+vector.x, self.y+vector.y)
        
    def rotate_right(self):
        self.x = self.y
        self.y = self.x * (-1)

    def rotate_left(self):
        self.x = self.y * (-1)
        self.y = self.x

    def equal(self, vector):
        return (self.x == vector.x and self.y == vector.y)


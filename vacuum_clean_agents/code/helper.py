class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return 'Vector({self.x}, {self.y})'.format(self=self)

    def add(self, vector):
        return Vector(self.x+vector.x, self.y+vector.y)
        
    def rotate_right(self):
        return Vector(self.y, -self.x)

    def rotate_left(self):
        return Vector(-self.x, self.y)

    def equal(self, vector):
        return (self.x == vector.x and self.y == vector.y)


if __name__ == '__main__':
    vec = Vector(0,1)
    vec.rotate_right()
    print(vec)
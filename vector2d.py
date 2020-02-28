#This Whole file is for rotations

import math
 
class Vector2D(tuple):
     
    def __new__(cls, x=0.0, y=0.0):
        return tuple.__new__(cls, (x, y))
     
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
         
    def __str__(self):
        return "(%s, %s)"%(self.x, self.y)
     
    @classmethod
    def next_vector(cls, args):
        return cls(args[2]-args[0], args[3]-args[1])
     
    def get_magnitude(self):
        return math.sqrt( self.x**2 + self.y**2 )
     
    def normalize(self):
        magnitude = self.get_magnitude()
        self.x /= magnitude
        self.y /= magnitude
         
    # rhs stands for Right Hand Side
    def __add__(self, rhs):
        return Vector2D(self.x + rhs.x, self.y + rhs.y)
     
    def __sub__(self, rhs):
        return Vector2D(self.x - rhs.x, self.y - rhs.y)
     
    def __neg__(self):
        return Vector2D(-self.x, -self.y)
     
    def __mul__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)
     
    def __div__(self, scalar):
        return Vector2D(self.x / scalar, self.y / scalar)

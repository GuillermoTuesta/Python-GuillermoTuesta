import math
import numbers

class Circle:
    def __init__(self, x: numbers.Number, y: numbers.Number, radius: numbers.Number): # 'number' is an abstract class with number classes (int, float, etc), simplifies checking.
        self.x = x
        self.y = y
        self.radius = radius
    
    # OVERRIDES
    def __str__(self):
        return f'''Class: Cirkel
x = {self.x}
y = {self.y}
radius = {self.radius}'''

    def __repr__(self):
        return f'cirkle{self.x , self.y, self.radius}'

    def __eq__(self, other) -> bool:
        if not isinstance(other, Circle):
            raise TypeError(f"Circle class (==): Only accepts other Circle objects, but other object is of type {type(other).__name__}")
        return self.radius == other.radius

    # METHODS
    def area(self):
        return math.pi * self.radius ** 2 
            
    def transform(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

class Rectangle:
    def __init__(self, x, y, side1, side2):
        self.x = x
        self.y = y
        self.side1 = side1
        self.side2 = side2
    
    # OVERRIDES
    def __str__(self):
        return f'''Class: Rectangle
x = {self.x}
y = {self.y}
side1 = {self.side1}
side2 = {self.side2}'''

    def __repr__(self):
        return f'cirkle{self.x , self.y, self.side1, self.side2}'

    def __eq__(self, other):
        if not isinstance(other, Rectangle):
            raise TypeError(f"Rectangle class (==): Only accepts other Rectangle objects, but other object is of type {type(other).__name__}")
        return self.area() == other.area()
    

    # METHODS
    def area(self):
        return self.side1 * self.side2
    
TestCircle = Circle('t',2,3)
TestCircle2 = Circle(2,2,3)
TestRectangle = Rectangle(1,2,3,4)
TestRectangle2 = Rectangle(1,2,4,3)

print(TestCircle.area())
print(TestCircle == TestCircle2)

print(TestRectangle.area())
print(TestRectangle == TestRectangle2)

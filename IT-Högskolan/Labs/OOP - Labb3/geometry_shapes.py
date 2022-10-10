import math
import numbers
from abc import ABC, abstractmethod

class Polygon(ABC):

    def __init__(self, x, y): # All shapes will have x,y coordinates.
        self._x = x
        self._y = y

    @abstractmethod
    def area(self):
        pass
    
    @abstractmethod
    def circumference(self):
        pass

    @abstractmethod
    def transform(self):
        pass

    @abstractmethod
    def contains(self):
        pass

    # Abstract overrides/overloads?

class Circle(Polygon):
    def __init__(self, x: numbers.Number, y: numbers.Number, radius: numbers.Number): # 'number' is an abstract class with number classes (int, float, etc), simplifies checking.
        super().__init__(x, y)
        self._radius = radius
    
    # OVERRIDES
    def __str__(self): # DONE
        return f'''Class: Cirkel
x = {self.x}
y = {self.y}
radius = {self._radius}'''

    def __repr__(self): # DONE
        return f'cirkle{self.x , self.y, self._radius}'

    def __eq__(self, other) -> bool:
        if not isinstance(other, Circle):
            raise TypeError(f"Circle class (==): Only accepts other Circle objects, but other object is of type {type(other).__name__}!")
        return self._radius == other._radius

    # METHODS
    def area(self): 
        return math.pi * self._radius ** 2 
    
    def circumference(self):
        return 2 * math.pi * self._radius
            
    def transform(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
    
    def contains(self, x_cord, y_cord):
        return ((x_cord - self._x)**2 + (y_cord - self._y)**2)**(1/2) <= self._radius # The circle is a nice shape.


class Rectangle(Polygon):
    def __init__(self, x, y, side1, side2):
        self._x = x
        self._y = y
        self._side1 = side1
        self._side2 = side2
    
    # OVERRIDES
    def __str__(self):
        return f'''Class: Rectangle
x = {self._x}
y = {self._y}
side1 = {self._side1}
side2 = {self._side2}'''

    def __repr__(self):
        return f'cirkle{self._x , self._y, self._side1, self._side2}'

    def __eq__(self, other):
        if not isinstance(other, Rectangle):
            raise TypeError(f"Rectangle class (==): Only accepts other Rectangle objects, but other object is of type {type(other).__name__}")
        return self.area() == other.area()
    
    # METHODS
    def area(self):
        return self._side1 * self._side2
    
    def circumference(self):
        return self._side1 * 2 + self._side2 * 2
    
    def transform(self):
        pass

    def contains(self, x_cord, y_cord):
        minimum_x = self._x - (self._side1/2)
        maximum_x = self._x + (self._side1/2) 
        minimum_y = self._y - (self._side2/2)
        maximum_y = self._y + (self._side2/2)
        return minimum_x <= x_cord <= maximum_x and minimum_y <= y_cord <= maximum_y # Another nice shape.
    
TestCircle = Circle(0,0,3)
TestCircle2 = Circle(2,2,3)
TestRectangle = Rectangle(0,0,4,4)
TestRectangle2 = Rectangle(1,2,4,3)

print(TestCircle.contains(3,0))
print(TestCircle.contains(3,0.1))
print(TestRectangle.contains(2,2))
print(TestRectangle.contains(2.1,2))

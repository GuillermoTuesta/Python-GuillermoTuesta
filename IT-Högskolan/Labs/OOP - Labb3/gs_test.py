from inspect import Attribute
import math
import numbers
from abc import ABC, abstractmethod

class Polygon(ABC):
	@abstractmethod
	def __init__(self):
		pass

	@property
	@abstractmethod
	def area(self):
		pass
	
	@property
	@abstractmethod
	def circumference(self):
		pass

	@abstractmethod
	def contains(self):
		pass
	
	@abstractmethod
	def __repr__(self):
		pass

	def transform(self, new_x, new_y): # Transform method will be the same for all classes
		self.x = new_x
		self.y = new_y # Still calls the class' @property.setters

	# OVERLOADS
	def __eq__(self, other):
		if not isinstance(other, type(self)):
			raise TypeError(f"__eq__(==) operator type mismatch: Can only compare same shapes: type(self) = {type(self)}, type(other) = {type(other)}")
		return self.area == other.area
	
	def __lt__(self, other):
		if not isinstance(other, type(self)):
			raise TypeError(f"__lt__(<) operator type mismatch: Can only compare same shapes: type(self) = {type(self)}, type(other) = {type(other)}")
		return self.area < other.area
	
	def __le__(self, other):
		if not isinstance(other, type(self)):
			raise TypeError(f"__le__(<=) operator type mismatch: Can only compare same shapes: type(self) = {type(self)}, type(other) = {type(other)}")	
		return self.area <= other.area
	
	def __gt__(self, other):
		if not isinstance(other, type(self)):
			raise TypeError(f"__gt__(>) operator type mismatch: Can only compare same shapes: type(self) = {type(self)}, type(other) = {type(other)}")	
		return self.area > other.area
	
	def __ge__(self, other):
		if not isinstance(other, type(self)):
			raise TypeError(f"__ge__(>=) operator type mismatch: Can only compare same shapes: type(self) = {type(self)}, type(other) = {type(other)}")	
		return self.area >= other.area


class Coordinate(): # Data descriptor class for coordinates, handles input validationg for setting, and handles getting.
	def __set_name__(self, owner, name):
		self.private_name = '_' + name

	def __get__(self, instance, owner):
		print("Descriptor get..")
		return getattr(obj, self.private_name)

	def __set__(self, instance, value):
		print("Initiating cord set..")
		if isinstance(value, float) or isinstance(value, int):
			instance.__dict__[self._name] = float(value)
		else:
			raise AttributeError(f'Given coordinate, {value} couldn''t be converted to float.')

class Circle(Polygon):
	'''A Class to represent circles.
	Child of the abstract Polygon class.'''
	def __init__(self, x: numbers.Number, y: numbers.Number, radius: numbers.Number): # 'number' is an abstract class with number classes (int, float, etc).
		self.x = x
		self.y = y
		self.radius = radius # Setter for radius also sets self._area to None.

	# OVERRIDES
	def __str__(self):
		new_string = (
			f'Class: Cirkel\n'
			f'x = {self._x}\n'
			f'y = {self._y}\n'
			f'radius = {self._radius}')
		return new_string

	def __repr__(self):
		return f"Circle{self._x, self._y, self._radius}"

	# PROPERTIES
	@property
	def x(self):
		return self._x

	@x.setter
	def x(self, value):
		if not isinstance(value, numbers.Number):
			raise TypeError(f'Given x value is of type {type(value)}')
		self._x = value

	@property
	def y(self):
		return self._y
	
	@y.setter
	def y(self, value):
		if not isinstance(value, numbers.Number):
			raise TypeError(f'Given y value is of type {type(value)}')
		self._y = value

	@property
	def radius(self):
		return self._radius

	@radius.setter
	def radius(self, value):
		if not isinstance(value, numbers.Number):
			raise TypeError(f'Circle Radius: Given value is of type {type(value)}: ')
		if value < 0:
			raise AttributeError(f"Circle Radius: value ({value}) is below zero.")
		self._radius = value
		self._area = None
		self._circumference = None

	@property
	def area(self):
		if self._area == None: # Lazy attributes - only computed once for each given radius, otherwise returns the previous answer.
			self._area = math.pi * self._radius ** 2
		return self._area

	@property
	def circumference(self):
		if self._circumference == None:
			self._circumference = 2 * math.pi * self._radius
		return self._circumference

	# METHODS
	def transform(self, new_x, new_y):
		'''Takes 2 new coordinates and assigns them as new coordinates.'''
		super().transform(new_x, new_y)

	def is_unit_circle(self) -> bool:
		'''Checks itself if it is a unit circle.'''
		return (self._x == 0 and self._y == 0 and self._radius == 1)


	def contains(self, x_cord, y_cord) -> bool:
		'''Checks if a pair of coordinates (x,y) lie within the circle.'''
		return ((x_cord - self._x)**2 + (y_cord - self._y)**2)**(1/2) <= self._radius # The circle is a nice shape.
		
	# OPERATOR OVERLOADS
	def __eq__(self, other) -> bool:
		return super().__eq__(other)
	
	def __lt__(self, other) -> bool:
		return super().__lt__(other)
	
	def __le__(self, other) -> bool:
		return super().__le__(other)
	
	def __gt__(self, other) -> bool:
		return super().__gt__(other)
	
	def __ge__(self, other) -> bool:
		return super().__ge__(other)


class Rectangle(Polygon):
	'''A Class to represent rectangles.
	Child of the abstract Polygon class.'''
	def __init__(self, x, y, base, height):
		self.x = x
		self.y = y
		self.base = base
		self.height = height # Property setter for height and base set self._area to None.

	# OVERRIDES
	def __str__(self):
		new_string = (
			f'Class: Rectangle\n'
			f'x = {self._x}\n'
			f'y = {self._y}\n'
			f'base = {self._base}\n'
			f'height = {self._height}')
		return new_string

	def __repr__(self):
		return f'Rectangle{self._x , self._y, self._base, self._height}'
	
	# PROPERTIES
	@property
	def x(self):
		return self._x
	
	@x.setter
	def x(self, value):
		if not isinstance(value, numbers.Number):
			raise TypeError(f'Given x value is of type {type(value)}')
		self._x = value
	
	@property
	def y(self):
		return self._y
	
	@y.setter
	def y(self, value):
		if not isinstance(value, numbers.Number):
			raise TypeError(f'Given y value is of type {type(value)}')
		self._y = value

	@property
	def base(self):
		return self._base
	
	@base.setter
	def base(self, value):
		if not isinstance(value, numbers.Number):
			raise TypeError(f'Given base value is of type {type(value)}')
		self._base = value
		self._area = None
		self._circumference = None
	
	@property
	def height(self):
		return self._height

	@height.setter
	def height(self, value):
		if not isinstance(value, numbers.Number):
			raise TypeError(f'Given height value is of type {type(value)}')
		self._height = value
		self._area = None
		self._circumference = None

	@property
	def area(self):
		if self._area == None:
			self._area = self.base * self.height
		return self._area
	
	@property
	def circumference(self):
		if self._circumference == None:
			self._circumference = self.base * 2 + self.height * 2
		return self._circumference

	# METHODS
	def transform(self, new_x, new_y):
		'''Takes 2 new coordinates and assigns them as new coordinates.'''
		super().transform(new_x, new_y)

	def is_square(self):
		'''Checks itself if it is a square.'''
		return self.base == self.height

	def contains(self, x_cord, y_cord):
		'''Checks if a pair of coordinates (x,y) lie within the rectangle.'''
		minimum_x = self.x - (self.base/2)
		maximum_x = self.x + (self.base/2) 
		minimum_y = self.y - (self.height/2)
		maximum_y = self.y + (self.height/2)
		return (minimum_x <= x_cord <= maximum_x) and (minimum_y <= y_cord <= maximum_y) # Another nice shape.
	
	# OVERLOADS
	def __eq__(self, other) -> bool:
		return super().__eq__(other)
	
	def __lt__(self, other) -> bool:
		return super().__lt__(other)
	
	def __le__(self, other) -> bool:
		return super().__le__(other)
	
	def __gt__(self, other) -> bool:
		return super().__gt__(other)
	
	def __ge__(self, other) -> bool:
		return super().__ge__(other)

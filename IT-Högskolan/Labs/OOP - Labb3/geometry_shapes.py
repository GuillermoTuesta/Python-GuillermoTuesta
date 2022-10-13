from inspect import Attribute
import math
import numbers
from abc import ABC, abstractmethod


# Had to comment out since I couldn't figure out how to use descriptors, I'll stick to @property decorators.
""" class Coordinate(): # Data descriptor class for coordinates, handles input validationg for setting, and handles getting.
	def __set_name__(self, owner, name):
		self._name = name

	def __get__(self, instance, owner):
		print("Initiationg cord get..")
		return instance.__dict__[self._name]

	def __set__(self, instance, value):
		print("Initiating cord set..")
		if isinstance(value, float) or isinstance(value, int):
			instance.__dict__[self._name] = float(value)
		else:
			raise ValueError(f'Given coordinate, {value} couldn''t be converted to float.') """

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

	# Abstract overrides/overloads?

class Circle(Polygon):
	def __init__(self, x: numbers.Number, y: numbers.Number, radius: numbers.Number): # 'number' is an abstract class with number classes (int, float, etc).
		self._x = x
		self._y = y
		self._radius = radius

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

	def __eq__(self, other) -> bool:
		if not isinstance(other, Circle):
			raise TypeError(f"Circle class (==): Only accepts other Circle objects, but other object is of type {type(other).__name__}!")
		return self._radius == other._radius

	# METHODS
	def transform(self, new_x, new_y):
		super().transform(new_x, new_y)

	def contains(self, x_cord, y_cord):
		return ((x_cord - self._x)**2 + (y_cord - self._y)**2)**(1/2) <= self._radius # The circle is a nice shape.


class Rectangle(Polygon):
	def __init__(self, x, y, base, height):
		self._x = x
		self._y = y
		self._base = base
		self._height = height

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
			self._area = self._base * self._height
		return self._area
	
	@property
	def circumference(self):
		if self._circumference == None:
			self._circumference = self._base * 2 + self._height * 2
		return self._circumference

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

	def __eq__(self, other):
		if not isinstance(other, Rectangle):
			raise TypeError(f"Rectangle class (==): Only accepts other Rectangle objects, but other object is of type {type(other).__name__}")
		return self._area == other._area
	
	# METHODS
	def transform(self, new_x, new_y):
		super().transform(new_x, new_y)

	def contains(self, x_cord, y_cord):
		minimum_x = self.x - (self._base/2)
		maximum_x = self.x + (self._base/2) 
		minimum_y = self.y - (self._height/2)
		maximum_y = self.y + (self._height/2)
		return (minimum_x <= x_cord <= maximum_x) and (minimum_y <= y_cord <= maximum_y) # Another nice shape.

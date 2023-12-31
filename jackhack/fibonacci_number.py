import random

class FibonacciNumber:
  """Mixin for weighting objects using the fibonacci sequence"""

  # override when inheriting to provide a maximum number that can be instantiated and default for random/reverse_random
  MAX = None

  @classmethod
  def from_value_floor(cls, value):
    """Return an object for the maximum number with a value no greater than the given value"""
    if value < 1:
      raise IndexError
    number = 0
    calc_value = 0
    while calc_value + number + 1 <= value:
      number += 1
      calc_value += number
    return cls(number)

  @classmethod
  def from_value_ceiling(cls, value):
    """Return an object for the minimum number with a value no less than the given value"""
    if value < 1:
      raise IndexError
    number = 0
    calc_value = 0
    while calc_value + number + 1 <= value:
      number += 1
      calc_value += number
    if calc_value != value:
      number += 1
    return cls(number)

  @classmethod
  def random(cls, max = None):
    """Return an object for a random number between 1 and max, weighted by values, with lower numbers the rarest"""
    if max is None:
      max = cls.MAX
    if max < 1 or (cls.MAX and cls.MAX < max):
      raise IndexError
    return cls.from_value_ceiling(random.randint(1, FibonacciNumber(max).value))

  @classmethod
  def reverse_random(cls, max = None):
    """Return an object for a random number between 1 and max, weighted by values, with higher numbers the rarest"""
    if max is None:
      max = cls.MAX
    if max < 1 or (cls.MAX and cls.MAX < max):
      raise IndexError
    return cls(max + 1 - FibonacciNumber.random(max).number)

  def __init__(self,number):
    if number < 1 or (self.MAX and self.MAX < number):
      raise IndexError
    self.number = number
    self.index = number - 1
    self.value = 0
    for i in range(1, self.number+1):
      self.value += i

  def __eq__(self, other):
    return self.number == other.number

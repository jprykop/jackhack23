import random

class FibonacciWeight:
  """Class for weighting objects using the fibonacci sequence"""

  # override when inheriting to provide a maximum number that can be instantiated and default for random/reverse_random
  MAX = None

  @classmethod
  def from_weight_floor(cls, weight):
    """Return an object for the maximum number with a weight no greater than the given weight"""
    if weight < 1:
      raise IndexError
    number = 0
    calc_weight = 0
    while calc_weight + number + 1 <= weight:
      number += 1
      calc_weight += number
    return cls(number)

  @classmethod
  def from_weight_ceiling(cls, weight):
    """Return an object for the minimum number with a weight no less than the given weight"""
    if weight < 1:
      raise IndexError
    number = 0
    calc_weight = 0
    while calc_weight + number + 1 <= weight:
      number += 1
      calc_weight += number
    if calc_weight != weight:
      number += 1
    return cls(number)

  @classmethod
  def random(cls, max = None):
    """Return an object for a random number between 1 and max, weighted by weights, with lower numbers the rarest"""
    if max is None:
      max = cls.MAX
    if max < 1 or (cls.MAX and cls.MAX < max):
      raise IndexError
    return cls.from_weight_ceiling(random.randint(1, FibonacciWeight(max).weight))

  @classmethod
  def reverse_random(cls, max = None):
    """Return an object for a random number between 1 and max, weighted by weights, with higher numbers the rarest"""
    if max is None:
      max = cls.MAX
    if max < 1 or (cls.MAX and cls.MAX < max):
      raise IndexError
    return cls(max + 1 - FibonacciWeight.random(max).number)

  def __init__(self,number):
    if number < 1 or (self.MAX and self.MAX < number):
      raise IndexError
    self.number = number
    self.index = number - 1
    self.weight = 0
    for i in range(1, self.number+1):
      self.weight += i

  def __eq__(self, other):
    return self.number == other.number
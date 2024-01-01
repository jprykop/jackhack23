import math
import random
from dataclasses import dataclass, field

def _float_from_weight(weight):
  if weight < 1:
    raise IndexError
  return (math.sqrt(1 + 8 * weight) - 1) / 2

@dataclass(frozen=True)
class TriangleWeight:
  """Class for weighting integer-associated objects using their corresponding triangle numbers (sum of positive integers up to n)"""
  number: int
  index: int = field(init=False)
  weight: int = field(init=False)

  # override when inheriting to provide a maximum number that can be instantiated and default for random/reverse_random
  MAX = None

  @classmethod
  def from_weight_floor(cls, weight):
    """Return an object for the maximum number with a weight no greater than the given weight"""
    return cls(int(_float_from_weight(weight)))

  @classmethod
  def from_weight_ceiling(cls, weight):
    """Return an object for the minimum number with a weight no less than the given weight"""
    return cls(math.ceil(_float_from_weight(weight)))

  @classmethod
  def random(cls, max = None):
    """Return an object for a random number between 1 and max, weighted by weights, with lower numbers the rarest"""
    if max is None:
      max = cls.MAX
    if max < 1 or (cls.MAX and cls.MAX < max):
      raise IndexError
    return cls.from_weight_ceiling(random.randint(1, TriangleWeight(max).weight))

  @classmethod
  def reverse_random(cls, max = None):
    """Return an object for a random number between 1 and max, weighted by weights, with higher numbers the rarest"""
    if max is None:
      max = cls.MAX
    if max < 1 or (cls.MAX and cls.MAX < max):
      raise IndexError
    return cls(max + 1 - TriangleWeight.random(max).number)

  def __post_init__(self):
    number = self.number
    if number < 1 or (self.MAX and self.MAX < number):
      raise IndexError
    object.__setattr__(self, 'index', number - 1)
    weight = int((number * (number + 1)) / 2)
    object.__setattr__(self, 'weight', weight)

  def __int__(self):
    return self.number

  def __eq__(self, other):
    if hasattr(other, 'number'):
      other = other.number
    return self.number == other

  def __hash__(self):
    return self.number

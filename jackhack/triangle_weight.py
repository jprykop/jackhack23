import math
import random
from dataclasses import dataclass, field

def _float_from_trinum(trinum):
  if trinum < 1:
    raise IndexError
  return (math.sqrt(1 + 8 * trinum) - 1) / 2

@dataclass(frozen=True)
class TriangleWeight:
  """Select integer-associated objects weighted by their values.

  For instance, the random(5) method would return an object representing an
  integer from 1 to 5 inclusive, with a 1/15 chance of it being 1, a 2/15 chance
  of being 2, etc up to a 5/15 chance of it being 5.  The denominator here is the
  sum of all positive integers up to the provided number, also known as the
  associated "triangle" number.

  Use this directly if you just need numbers, subclass if you need to associate
  other data with each number.

  When subclassing, override MAX with an integer value to enforce a maximum
  number that can be instantiated and provide a default value for random and
  reverse_random.

  Can be converted to a vanilla integer using int() and acts as an integer for
  equality and hashability (making it interchangeable with its subclasses for
  these purposes.)

  Usage:

    t = TriangleWeight(5)
    t.number              # 5
    t.trinum              # 15
    t.index               # 4

    t = TriangleWeight.from_trinum_floor(16)
    t.number              # 5
    t.trinum              # 15

    t = TriangleWeight.from_trinum_ceiling(14)
    t.number              # 5
    t.trinum              # 15

    # Return random object with the following probability for each number:
    # 1: 1/15, 2: 2/15, 3: 3/15, 4: 4/15, 5: 5/15
    t = TriangleWeight.random(5)

    # Return random object with the following probability for each number:
    # 1: 5/15, 2: 4/15, 3: 3/15, 2: 2/15, 1: 1/15
    t = TriangleWeight.reverse_random(5)

    # Subclass and specify MAX to provide limits/defaults
    class TriWeightThing(TriangleWeight):
      MAX = 5

    t = TriWeightThing(5)                      # t.number == 5
    t = TriWeightThing(6)                      # raises IndexError
    t = TriWeightThing.from_trinum_floor(20)   # t.number == 5
    t = TriWeightThing.from_trinum_floor(21)   # raises IndexError
    t = TriWeightThing.from_trinum_ceiling(15) # t.number == 5
    t = TriWeightThing.from_trinum_ceiling(16) # raises IndexError

    TriWeightThing.random()  # 1-5, same spread as TriangleWeight.random(5)
    TriWeightThing.random(4) # 1-4, same spread as TriangleWeight.random(4)
    TriWeightThing.random(6) # raises IndexError

    # The above also applies to reverse_random
  """
  number: int
  index: int = field(init=False)
  trinum: int = field(init=False)

  MAX = None

  @classmethod
  def from_trinum_floor(cls, trinum):
    """Return instance for the max number with a trinum no greater than the input"""
    return cls(int(_float_from_trinum(trinum)))

  @classmethod
  def from_trinum_ceiling(cls, trinum):
    """Return instance for the min number with a trinum no less than the input"""
    return cls(math.ceil(_float_from_trinum(trinum)))

  @classmethod
  def random(cls, max = None):
    """Return instance for a random int up to max, weighted with lower values the rarest"""
    if max is None:
      max = cls.MAX
    if max < 1 or (cls.MAX and cls.MAX < max):
      raise IndexError
    return cls.from_trinum_ceiling(random.randint(1, TriangleWeight(max).trinum))

  @classmethod
  def reverse_random(cls, max = None):
    """Return instance for a random int up to max, weighted with higher values the rarest"""
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
    trinum = int((number * (number + 1)) / 2)
    object.__setattr__(self, 'trinum', trinum)

  def __int__(self):
    return self.number

  def __eq__(self, other):
    if hasattr(other, 'number'):
      other = other.number
    return self.number == other

  def __hash__(self):
    return self.number

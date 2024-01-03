import math
import random
from dataclasses import dataclass, field

def trinum(number):
  """Return the triangle number for the given integer.

  The triangle number is the sum of all positive integers up to the provided
  number, known as such because it can be stacked like a triangle:

      *
     * *
    * * *
   * * * *
  * * * * *
  """
  number = int(number)
  if number < 1:
    raise IndexError
  return int((number * (number + 1)) / 2)

def _float_from_trinum(trinum):
  trinum = int(trinum)
  if trinum < 1:
    raise IndexError
  return (math.sqrt(1 + 8 * trinum) - 1) / 2

def from_trinum_floor(trinum):
  """Return the maximum integer with a trinum no greater than the input."""
  return int(_float_from_trinum(trinum))

def from_trinum_ceiling(trinum):
  """Return the minimum integer with a trinum no less than the input."""
  return math.ceil(_float_from_trinum(trinum))

def trirand(max):
  """Return a random int up to max, triangle-weighted with lower values the rarest.

  For instance, trirand(5) would return an integer from 1 to 5 inclusive, with
  a 1/15 chance of 1, a 2/15 chance of 2, etc up to a 5/15 chance of it being 5.
  The denominator here is the sum of all positive integers up to the provided
  number, also known as the associated triangle number."""
  if not max or max < 1:
    raise IndexError
  return from_trinum_ceiling(random.randint(1, trinum(max)))

def reverse_trirand(max):
  """Return a random int up to max, triangle-weighted with higher values the rarest.

  Similar to trirand but reversed, so reverse_trirand(5) has a 1/15 chance of
  being 5, a 2/15 chance of being 4, etc up to a 5/15 chance of being 1."""
  return 1 - trirand(max) + max

@dataclass(frozen=True)
class TriangleWeight:
  """A parent class for weighting integer-associated objects by their values.

  You can use the triangle_weight module's functions directly if you just need
  numbers.  This is a frozen dataclass intended to be subclassed so you can
  associate other data with each number.

  When subclassing, override MAX with an integer value to enforce a maximum
  number that can be instantiated and provide a default value for trirand and
  reverse_trirand.

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
    t = TriangleWeight.trirand(5)

    # Return trirand object with the following probability for each number:
    # 1: 5/15, 2: 4/15, 3: 3/15, 2: 2/15, 1: 1/15
    t = TriangleWeight.reverse_trirand(5)

    # Subclass and specify MAX to provide limits/defaults
    class TriWeightThing(TriangleWeight):
      MAX = 5

    t = TriWeightThing(5)                      # t.number == 5
    t = TriWeightThing(6)                      # raises IndexError
    t = TriWeightThing.from_trinum_floor(20)   # t.number == 5
    t = TriWeightThing.from_trinum_floor(21)   # raises IndexError
    t = TriWeightThing.from_trinum_ceiling(15) # t.number == 5
    t = TriWeightThing.from_trinum_ceiling(16) # raises IndexError

    TriWeightThing.trirand()  # 1-5, same spread as TriangleWeight.trirand(5)
    TriWeightThing.trirand(4) # 1-4, same spread as TriangleWeight.trirand(4)
    TriWeightThing.trirand(6) # raises IndexError

    # The above also applies to reverse_trirand
  """
  number: int
  index: int = field(init=False)
  trinum: int = field(init=False)

  MAX = None

  @classmethod
  def from_trinum_floor(cls, trinum):
    """Return instance for the max number with a trinum no greater than the input"""
    return cls(from_trinum_floor(trinum))

  @classmethod
  def from_trinum_ceiling(cls, trinum):
    """Return instance for the min number with a trinum no less than the input"""
    return cls(from_trinum_ceiling(trinum))

  @classmethod
  def trirand(cls, max = 0):
    """Return instance for a random int up to max, weighted with lower values the rarest"""
    max = max or cls.MAX
    if cls.MAX and cls.MAX < max:
      raise IndexError
    return cls(trirand(max))

  @classmethod
  def reverse_trirand(cls, max = 0):
    """Return instance for a random int up to max, weighted with higher values the rarest"""
    max = max or cls.MAX
    if cls.MAX and cls.MAX < max:
      raise IndexError
    return cls(reverse_trirand(max))

  def __post_init__(self):
    number = self.number
    if number < 1 or (self.MAX and self.MAX < number):
      raise IndexError
    object.__setattr__(self, 'index', number - 1)
    object.__setattr__(self, 'trinum', trinum(number))

  def __int__(self):
    return self.number

  def __eq__(self, other):
    if hasattr(other, 'number'):
      other = other.number
    return self.number == other

  def __hash__(self):
    return self.number

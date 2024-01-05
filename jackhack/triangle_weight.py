import math
import random
from dataclasses import dataclass, field

def trinum(max):
  """Return the triangle max for the given integer.

  The triangle max is the sum of all positive integers up to the provided
  max, known as such because it can be stacked like a triangle:

      *
     * *
    * * *
   * * * *
  * * * * *
  """
  max = int(max)
  if max < 1:
    raise IndexError
  return int((max * (max + 1)) / 2)

def __float_from_trinum(trinum):
  trinum = int(trinum)
  if trinum < 1:
    raise IndexError
  return (math.sqrt(1 + 8 * trinum) - 1) / 2

def from_trinum_floor(trinum):
  """Return the maximum integer with a trinum no greater than the input."""
  return int(__float_from_trinum(trinum))

def from_trinum_ceiling(trinum):
  """Return the minimum integer with a trinum no less than the input."""
  return math.ceil(__float_from_trinum(trinum))

def trirand(max):
  """Return a random int up to max, triangle-weighted with lower values the rarest.

  For instance, trirand(5) would return an integer from 1 to 5 inclusive, with
  a 1/15 chance of 1, a 2/15 chance of 2, etc up to a 5/15 chance of it being 5.
  The denominator here is the sum of all positive integers up to the provided
  max, also known as the associated triangle number."""
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
  """Set a maximum value for trirand module functions, and access them as methods.

  Usage:

    t = TriangleWeight(5)
    t.max == 5

    t.from_trinum_floor(20) == 5
    t.from_trinum_floor(21) # raises IndexError

    t.from_trinum_ceiling(15) == 5
    t.from_trinum_ceiling(16) # raises IndexError

    t.trirand()  # same spread as trirand(5)
    t.trirand(4) # same spread as trirand(4)
    t.trirand(6) # raises IndexError

    t.reverse_trirand()  # same spread as reverse_trirand(5)
    t.reverse_trirand(4) # same spread as reverse_trirand(4)
    t.reverse_trirand(6) # raises IndexError
  """
  max: int

  def __validate_number(self, number):
    if number > self.max:
      raise IndexError
    return number

  def __validate_number_input(self, number):
    return self.__validate_number(int(number or self.max))

  def trinum(self, number = None):
    global trinum
    number = self.__validate_number_input(number)
    return trinum(number)

  def from_trinum_floor(self, trinum = None):
    global from_trinum_floor
    trinum = trinum or self.trinum()
    return self.__validate_number(from_trinum_floor(trinum))

  def from_trinum_ceiling(self, trinum = None):
    global from_trinum_ceiling
    trinum = trinum or self.trinum()
    return self.__validate_number(from_trinum_ceiling(trinum))

  def trirand(self, max = None):
    global trirand
    max = self.__validate_number_input(max)
    return trirand(max)

  def reverse_trirand(self, max = None):
    global reverse_trirand
    max = self.__validate_number_input(max)
    return reverse_trirand(max)

import random
from typing import Any
from django.db import models

# Create your models here.

class Job:
  WARRIOR = 'warrior'
  HEALER = 'healer'
  THIEF = 'thief'
  WIZARD = 'wizard'
  HUNTER = 'hunter'
  JOBS = (WARRIOR, HEALER, THIEF, WIZARD, HUNTER)

class FibonacciMixin:
  """Mixin for weighting objects using the fibonacci sequence"""

  @classmethod
  def from_value_floor(cls,value):
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
  def from_value_ceiling(cls,value):
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
  def random(cls,max):
    """Return an object for a random number between 1 and max, weighted by values, with lower numbers the rarest"""
    return cls.from_value_ceiling(random.randint(1, cls(max).value))

  @classmethod
  def reverse_random(cls,max):
    """Return an object for a random number between 1 and max, weighted by values, with higher numbers the rarest"""
    return cls(max + 1 - cls.random(max).number)

  def __init__(self,number):
    if number < 1:
      raise IndexError
    self.number = number
    self.index = number - 1
    self.value = 0
    for i in range(1, self.number+1):
      self.value += i

class Element(FibonacciMixin):

  ELEMENTS = (
    ('concrete','in a parking lot','slack','Bob','rhinestone','pavement','Slackers'),
    ('time','in another dimension','warp','Cthulu','quantum','theoretical','Shoggoths'),
    ('cheese','on the moon','cheddar','Ur','meteor','moon','Aliens'),
    ('clouds','in the sky','fog','Lucy','diamond','sky','Hippies'),
    ('fire','on a volcano','magma','Ifrit','ruby','volcano','Firemen'),
    ('waves','at sea','aguaga','Poseidon','water','sea','Pirates'),
    ('flowers','in a poppy field','sleep','Elphaba','emerald','fields','Lollipops'),
    ('sand','in the desert','sandstorm','Ra','amber','desert','Fremen'),
    ('ice','in the arctic','ice','Shiva','ice','arctic','Vikings'),
    ('rock','in the mountains','quake','Buddha','stone','mountains','Masons'),
    ('mud','in a swamp','muck','Yoda','lucasite','swamp','Lizardmen'),
    ('darkness','underground','hole','Hades','black','caverns','Morlocks'),
    ('trees','in the forest','leaf','Treebush','wood','forest','Hoods'),
    ('grass','on the prairie','mow','Laura','glass','prairie','Barbarians')
  )

  def __init__(self,number):
    super.__init__(number)
    if number > len(self.ELEMENTS):
      raise IndexError
    info = self.ELEMENTS[self.index]
    self.resist = info[0]
    self.terrain = info[1]
    self.spell = info[2]
    self.god = info[3]
    self.gem = info[4]
    self.map = info[5]
    self.guild = info[6]

class Game(models.Model):
  player_name = models.CharField(max_length=16)
  warrior_xp = models.IntegerField(default=0)
  healer_xp = models.IntegerField(default=0)
  thief_xp = models.IntegerField(default=0)
  wizard_xp = models.IntegerField(default=0)
  hunter_xp = models.IntegerField(default=0)

class Day(models.Model):
  game = models.ForeignKey(Game, on_delete=models.CASCADE)
  town_gold = models.IntegerField(blank=True, null=True)
  monster_gold = models.IntegerField(blank=True, null=True)
  terrain = models.IntegerField()

import random

class InvalidMove(Exception):
  pass

class Day:
  MAX_PLAYABLE_DAYS = 99
  MAX_DAYS = MAX_PLAYABLE_DAYS + 1

  def __init__(self, *, daynum, town_gold=None, monster_gold=None, played=False):
    if daynum < 1 or daynum > self.MAX_DAYS:
      raise IndexError
    self.daynum = daynum
    self.town_gold = town_gold
    self.monster_gold = monster_gold
    self.played = played

class Days:
  def __init__(self):
    self._list = []

  def append(self, obj):
    self._list.append(obj).sort(key=Day.daynum)

  def current(self):
    next(day for day in self._list if not day.played)

  def by_day(self, daynum):
    self._list[daynum - 1]

class Game:
  # methods to override for django version

  def __init__(self, *args, **kwargs):
    self.player_name = kwargs["player_name"]
    self._days = []

  def _add_day(self, attributes):
    self._days.append(Day(**attributes))

  def days(self):
    return self._days

  # should not need to override for django version

  def _generate_day(self, daynum, dayclass=Day):
    self._add_day({
      'daynum': daynum,
      'town_gold': random.randint(1, daynum) if random.randint(1, Day.MAX_DAYS) <= Day.MAX_DAYS - daynum else None,
      'monster_gold': random.randint(1, daynum) if random.randint(1, Day.MAX_DAYS) <= daynum else None
    })

  def start(self):
    if self.days():
      raise InvalidMove("Game already started")
    for daynum in range(1, Day.MAX_DAYS):
      self._generate_day(daynum)
    self._add_day({
      'daynum': Day.MAX_DAYS,
      'town_gold': Day.MAX_DAYS,
      'monster_gold': Day.MAX_DAYS
    })

  def current_day(self):
    next((day for day in self.days() if not day.played), None)

  def day(self, daynum):
    self._get_day(self, daynum)



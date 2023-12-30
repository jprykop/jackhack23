import random
from dataclasses import dataclass, field

class InvalidMove(Exception):
  pass

@dataclass
class Day:
  daynum: int
  town_gold: int = None
  town_gold_acquired: int = None
  monster_gold: int = None
  monster_gold_acquired: int = None
  gold_spent: int = None
  played: bool = False

  MAX_DAYS = 100

  def to_dict(self):
    return {'daynum': self.daynum, 'town_gold': self.town_gold, 'monster_gold': self.monster_gold, 'played': self.played }

@dataclass
class Game:
  # methods to override for django version (including __init__)
  player_name: str
  _days: list = field(default_factory=list)

  def _add_day(self, attributes):
    self._days.append(Day(**attributes))

  def days(self):
    return self._days

  def _save_game(self):
    pass

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

  def day(self, daynum):
    return self.days()[daynum - 1]

  def current_day(self):
    return next((day for day in self.days() if not day.played), None)

  def gold(self):
    town_gold_acquired = sum([d.town_gold_acquired for d in self.days() if d.town_gold_acquired]) or 0
    monster_gold_acquired = sum([d.monster_gold_acquired for d in self.days() if d.monster_gold_acquired]) or 0
    gold_spent = sum([-d.gold_spent for d in self.days() if d.gold_spent]) or 0
    return town_gold_acquired + monster_gold_acquired + gold_spent

  def play(self):
    today = self.current_day()
    if today.town_gold is not None:
      self.gold += today.town_gold
    if today.monster_gold is not None:
      self.gold += today.monster_gold

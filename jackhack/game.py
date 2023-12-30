import random
from dataclasses import dataclass, field
from jackhack.fibonacci_mixin import FibonacciMixin

class InvalidMove(Exception):
  pass

class MonsterKind(FibonacciMixin):
  KINDS = (
    'yeti',
    'dinosaur',
    'dragon',
    'demon',
    'giant',
    'cockatrice',
    'gargoyle',
    'vampire',
    'werewolf',
    'zombie',
    'troll',
    'ogre',
    'goblin',
    'blob'
  )

  def name(self):
    self.KINDS[self.index]

  def __str__(self):
    self.name

class Element(FibonacciMixin):
  KINDS = (
    ('concrete','in a parking lot','slack','Bob','rhinestone','pavement','Slackers'),
    ('time','in another dimension','warp','Cthulu','quantum','theoretical','Shoggoths'),
    ('cheese','on the moon','cheddar','Ur','meteor','moon','Aliens'),
    ('clouds','in the sky','fog','Lucy','diamond','sky','Hippies'),
    ('fire','on a volcano','magma','Ifrit','ruby','volcano','Firemen'),
    ('waves','at sea','aguaga','Poseidon','water','sea','Pirates'),
    ('flowers','in a poppy field','sleep','Elphaba','emerald','fields','Lollipops'),
    ('sand','in the desert','sandstorm','Ra','amber','desert','Fremen'),
    ('ice','in the arctic','ice','Shiva','ice','arctic','Vikings'),
    ('rocks','in the mountains','quake','Buddha','stone','mountains','Masons'),
    ('mud','in a swamp','muck','Yoda','lucasite','swamp','Lizardmen'),
    ('darkness','underground','hole','Hades','black','caverns','Morlocks'),
    ('trees','in the forest','leaf','Treebush','wood','forest','Hoods'),
    ('grass','on the prairie','mow','Laura','glass','prairie','Barbarians')
  )

  def name(self):
    self.KINDS[self.index][0]

  def __str__(self):
    self.name

  def terrain(self):
    self.KINDS[self.index][1]

  def spell(self):
    self.KINDS[self.index][2]

  def god(self):
    self.KINDS[self.index][3]

  def gem(self):
    self.KINDS[self.index][4]

  def mapname(self):
    self.KINDS[self.index][5]

  def guild(self):
    self.KINDS[self.index][6]

@dataclass
class Monster:
  gold: int
  kind_number: int
  strength_number: int
  weakness_number: int
  attack_number: int

  def kind(self):
    MonsterKind(self.kind_number)

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

  def acquire_town_gold(self):
    self.town_gold_acquired = self.town_gold

  def acquire_monster_gold(self):
    self.monster_gold_acquired = self.monster_gold

  def spend_gold(self, amount):
    if self.gold_spent is None:
      self.gold_spent = 0
    self.gold_spent += amount

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

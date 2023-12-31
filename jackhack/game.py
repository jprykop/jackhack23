import random
from dataclasses import dataclass, field
from jackhack.fibonacci_weight import FibonacciWeight

class InvalidMove(Exception):
  pass

class MonsterKind(FibonacciWeight):
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

  MAX = len(KINDS)

  def name(self):
    self.KINDS[self.index]

  def __str__(self):
    self.name

class Element(FibonacciWeight):
  KINDS = (
    ('concrete','in a parking lot','slack','Bob','rhinestone','pavement','Slackers'),
    ('time','in another dimension','warp','Cthulu','quantum','theoretical','Shoggoths'),
    ('cheese','on the moon','cheddar','Ur','meteor','moon','Aliens'),
    ('air','in the sky','fog','Lucy','diamond','sky','Hippies'),
    ('fire','on a volcano','magma','Ifrit','ruby','volcano','Firemen'),
    ('fairy','in a poppy field','sleep','Elphaba','emerald','fields','Lollipops'),
    ('ice','in the arctic','ice','Shiva','ice','arctic','Vikings'),
    ('water','at sea','aguaga','Poseidon','water','sea','Pirates'),
    ('sand','in the desert','sandstorm','Ra','amber','desert','Fremen'),
    ('rock','in the mountains','quake','Buddha','stone','mountains','Masons'),
    ('mud','in a swamp','muck','Yoda','lucasite','swamp','Lizardmen'),
    ('dark','in a cave','hole','Hades','black','caverns','Morlocks'),
    ('wood','in the forest','leaf','Treebush','wood','forest','Hoods'),
    ('grass','on the prairie','mow','Laura','grass','prairie','Barbarians')
  )

  MAX = len(KINDS)

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

  def kind(self):
    MonsterKind(self.kind_number)

  def strength(self):
    Element(self.strength_number)

  def weakness(self):
    Element(self.weakness_number)

@dataclass
class Day:
  # only need to override these properties via __init__ in django version
  daynum: int
  town_gold: int = None
  town_gold_acquired: int = None
  monster_gold: int = None
  monster_gold_acquired: int = None
  gold_spent: int = None
  terrain_number: int = None
  monster_kind_number: int = None
  monster_strength_number: int = None
  monster_weakness_number: int = None
  job_played: str = ''
  job_item_acquired: bool = None
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

  def net_gold(self):
    net = 0
    if self.town_gold_acquired: net += self.town_gold_acquired
    if self.monster_gold_acquired: net += self.monster_gold_acquired
    if self.gold_spent: net -= self.gold_spent
    return net

  def net_xp(self):
    net = 0
    if self.played:
      if self.town_gold: net += self.town_gold
      if self.monster_gold: net += self.monster_gold
      if not net: net = self.daynum
    return net

  def monster(self):
    return Monster(
      gold=self.monster_gold,
      kind_number=self.monster_kind_number,
      strength_number=self.monster_strength_number,
      weakness_number=self.monster_weakness_number
    ) if self.monster_gold else None

  def is_last_day(self):
    return self.daynum == self.MAX_DAYS

@dataclass
class Game:
  # things to override for django version (including __init__)
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
    attributes = {
      'daynum': daynum,
      'terrain_number': Element.random().number,
      'town_gold': random.randint(1, daynum) if random.randint(1, Day.MAX_DAYS) <= Day.MAX_DAYS - daynum else None,
      'monster_gold': random.randint(1, daynum) if random.randint(1, Day.MAX_DAYS) <= daynum else None
    }
    if attributes['monster_gold']:
      attributes['monster_kind_number'] = MonsterKind.random().number
      attributes['monster_strength_number'] = MonsterKind.reverse_random().number
      attributes['monster_weakness_number'] = MonsterKind.reverse_random().number
    self._add_day(attributes)

  def start(self):
    if self.days():
      raise InvalidMove("Game already started")
    for daynum in range(1, Day.MAX_DAYS):
      self._generate_day(daynum)
    self._add_day({
      'daynum': Day.MAX_DAYS,
      'terrain_number': 1,
      'town_gold': Day.MAX_DAYS,
      'monster_gold': Day.MAX_DAYS,
      'monster_strength_number': 1,
      'monster_weakness_number': 2
    })

  def day(self, daynum):
    return self.days()[daynum - 1]

  def current_day(self):
    return next((day for day in self.days() if not day.played), None)

  def gold(self):
    return sum([day.net_gold() for day in self.days()])

  def xp(self, job=None):
    check_job = lambda day : (day.played and job == day.job_played) if job else day.played
    return sum([day.net_xp() if check_job(day) else 0 for day in self.days()])

  def level(self, job=None):
    if job:
      xp = self.xp(job)
      return FibonacciWeight.from_weight_floor(xp).number + 1 if xp else 1
    return sum([self.level(job) for job in self.JOBS])

  def items(self, job):
    return set([day.terrain_number for day in self.days() if day.job_played == job and day.job_item_acquired])

  def play(self, job=None):
    day = self.current_day()
    if day.is_last_day:
      self.final_boss(day)
    elif not job:
      raise InvalidMove("No job specified")
    elif job not in self.JOBS:
      raise InvalidMove("Unknown job")
    else:
      self.JOBS[job](self, day)

  def warrior_odds(self, day):
    pass

  def cleric_odds(self, day):
    pass

  def thief_odds(self, day):
    pass

  def wizard_odds(self, day):
    pass

  def ranger_odds(self, day):
    pass

  def final_boss_odds(self, day):
    pass

  def warrior(self, day):
    pass

  def cleric(self, day):
    pass

  def thief(self, day):
    pass

  def wizard(self, day):
    pass

  def ranger(self, day):
    pass

  def final_boss(self, day):
    pass

  JOBS = {
    'warrior': warrior,
    'cleric': cleric,
    'thief': thief,
    'wizard': wizard,
    'ranger': ranger
  }

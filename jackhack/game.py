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
  health_lost_from_town: int = None
  health_gained_from_town: int = None
  health_lost_from_monster: int = None
  health_gained_from_monster: int = None
  health_gained_otherwise: int = None
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

  def net_health(self):
    net = 0
    if self.played:
      if self.health_gained_from_monster: net += self.health_gained_from_monster
      if self.health_gained_from_town: net += self.health_gained_from_town
      if self.health_gained_otherwise: net += self.health_gained_otherwise
      if self.health_lost_from_monster: net -= self.health_lost_from_monster
      if self.health_lost_from_town: net -= self.health_lost_from_town
    return net

  def monster(self):
    return Monster(
      gold=self.monster_gold,
      kind_number=self.monster_kind_number,
      strength_number=self.monster_strength_number,
      weakness_number=self.monster_weakness_number
    ) if self.monster_gold else None

  def terrain(self):
    return Element(self.terrain_number)

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
    # TODO: make job required, this is not how we calculate aggregate final level
    return sum([self.level(job) for job in self.JOBS])

  def items(self, job):
    return set([day.terrain() for day in self.days() if day.job_played == job and day.job_item_acquired])

  def health(self):
    return 1 + sum([day.net_health() for day in self.days()])

  def stats(self, job=None):
    stats = {
      'current_day': self.current_day(),
      'gold': self.gold(),
      'health': self.health()
    }
    if job:
      stats['level'] = self.level(job)
      stats['items'] = self.items(job)
    return stats

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

  def _monster_odds(self, day, job_level, monster_level=None):
    monster = day.monster
    if not monster:
      raise InvalidMove("No monster odds without monster")
    monster_level = monster_level or monster.gold
    if day.terrain() == monster.strength():
      monster_level = monster_level * 2
    if day.terrain() == monster.weakness():
      job_level = job_level * 2
    return (job_level, monster_level)

  def _warrior_odds(self, day, job_level=None, monster_level=None):
    job = 'warrior'
    monster = day.monster
    if not monster:
      raise InvalidMove("No warrior odds without monster")
    job_level = job_level or self.level(job)
    monster_level = monster_level or monster.gold
    if monster.strength() in self.items(job):
      job_level = job_level * 2
    return (job_level, monster_level)

  def _cleric_odds(self, day, job_level=None, target_level=None):
    job = 'cleric'
    job_level = job_level or self.level(job)
    if not target_level: target_level = day.town_gold or day.daynum
    if day.terrain() in self.items(job):
      job_level = job_level * 2
    return (job_level, target_level)

  def _thief_odds(self, day, job_level=None, town_level=None):
    job = 'thief'
    if not day.town_gold:
      raise InvalidMove("No thief odds without town")
    job_level = job_level or self.level(job)
    if not town_level: town_level = day.town_gold
    if day.terrain() in self.items(job):
      town_level = town_level * 2 # it's a weakness
    return (job_level, town_level)

  def _wizard_odds(self, day, job_level=None, monster_level=None):
    job = 'warrior'
    monster = day.monster
    if not monster:
      raise InvalidMove("No wizard odds without monster")
    job_level = job_level or self.level(job)
    monster_level = monster_level or monster.gold
    if monster.weakness() in self.items(job):
      job_level = job_level * 2
    return (job_level, monster_level)

  def _ranger_odds(self, day, job_level=None, target_level=None):
    job = 'ranger'
    monster = day.monster
    town_gold = day.town_gold
    if not monster or town_gold:
      raise InvalidMove("No ranger odds without monster or town")
    job_level = job_level or self.level(job)
    target_level = target_level or (monster.gold if monster else town_gold)
    if day.terrain() in self.items(job):
      job_level = job_level * 2
    return (job_level, target_level)

  def _final_boss_odds(self, day):
    level = self._warrior_odds(day)[0]
    level += self._cleric_odds(day)[0]
    level += self._wizard_odds(day)[0]
    level += self._ranger_odds(day)[0]
    odds = self._monster_odds(day, level)
    odds = self._thief_odds(day, *odds)
    return odds

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

import random
from dataclasses import dataclass, field
import jackhack.triangle_weight as tw

# a single roll, returns a boolean
def __swing(pc_level, target_level):
  return random.randint(1, pc_level + target_level) <= pc_level

# swings target_level times, returns the number of failures (i.e. health lost) with optional max (i.e. starting health)
# update this to use random.binomialvariate once I upgrade to python 3.12
def __hack(pc_level, target_level, max=None):
  fails = sum(1 if not __swing(pc_level, target_level) else 0 for n in range(target_level))
  if max and fails > max: fails = max
  return fails

class InvalidMove(Exception):
  pass

MONSTERS = (
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

ARMOR = (
  'breastplate',
  'helm',
  'left gauntlet',
  'right gauntlet',
  'left boot',
  'right boot',
  'left vambrace',
  'right vambrace',
  'left greave',
  'right greave',
  'left pauldron',
  'right pauldron',
  'visor',
  'feather'
)

def __map_element(e):
  return {
    'name':    e[0],
    'place':   e[1],
    'terrain': e[2],
    'place':   e[3],
    'spell':   e[4],
    'god':     e[5]
  }

ELEMENTS = map(__map_element,(
  ('psyche',   'in your mind',      'the imagination',  'slack',     'Bob'),
  ('time',     'lost in time',      'history',          'warp',      'The Doctor'),
  ('space',    'on the moon',       'the moon',         'rocket',    'Luna'),
  ('air',      'in the sky',        'the sky',          'fog',       'Zeus'),
  ('fire',     'on a volcano',      'the volcano',      'fire',      'Vulcan'),
  ('fairy',    'in fairyland',      'fairyland',        'sleep',     'Titania'),
  ('ice',      'in the arctic',     'the arctic',       'ice',       'Shiva'),
  ('water',    'at sea',            'the ocean',        'water',     'Poseidon'),
  ('sand',     'in the desert',     'the desert',       'sandstorm', 'Ra'),
  ('rock',     'on a mountain',     'the mountains',    'quake',     'Buddha'),
  ('mud',      'in a swamp',        'the swamp',        'poison',    'Yoda'),
  ('darkness', 'in a cave',         'the underworld',   'darkness',  'Hades'),
  ('wood',     'in a forest',       'the forest',       'tangle',    'Artemis'),
  ('grass',    'on the prairie',    'the prairie',      'mow',       'Demeter')
))

### name/terrain/spell/gold/gem/mapname/guild
#   ORIGINAL_ELEMENTS = (
#     ('concrete','in a parking lot','slack','Bob','rhinestone','pavement','Slackers'),
#     ('time','in another dimension','warp','Cthulu','quantum','theoretical','Shoggoths'),
#     ('cheese','on the moon','cheddar','Ur','meteor','moon','Aliens'),
#     ('air','in the sky','fog','Lucy','diamond','sky','Hippies'),
#     ('fire','on a volcano','magma','Ifrit','ruby','volcano','Firemen'),
#     ('fairy','in a poppy field','sleep','Elphaba','emerald','fields','Lollipops'),
#     ('ice','in the arctic','ice','Shiva','ice','arctic','Vikings'),
#     ('water','at sea','aguaga','Poseidon','water','sea','Pirates'),
#     ('sand','in the desert','sandstorm','Ra','amber','desert','Fremen'),
#     ('rock','in the mountains','quake','Buddha','stone','mountains','Masons'),
#     ('mud','in a swamp','muck','Yoda','lucasite','swamp','Lizardmen'),
#     ('dark','in a cave','hole','Hades','black','caverns','Morlocks'),
#     ('wood','in the forest','leaf','Treebush','wood','forest','Hoods'),
#     ('grass','on the prairie','mow','Laura','grass','prairie','Barbarians')
#   )

class BaseDay:
  MAX_DAYS = 100

  DATA_ATTRIBUTES = [
    'daynum',
    'town_level',
    'town_gold_acquired',
    'monster_level',
    'monster_gold_acquired',
    'gold_spent',
    'terrain',
    'monster_kind',
    'monster_strength',
    'monster_weakness',
    'health_lost_from_town',
    'health_gained_from_town',
    'health_lost_from_monster',
    'health_gained_from_monster',
    'health_gained_otherwise',
    'job_played',
    'job_item_acquired',
    'played'
  ]

  def as_dict(self):
    out = {}
    for att in self.DATA_ATTRIBUTES:
      out[att] = getattr(self, att)
    return out

  def acquire_town_gold(self):
    self.town_gold_acquired = self.town_level

  def acquire_monster_gold(self):
    self.monster_gold_acquired = self.monster_level

  def acquire_job_item(self):
    self.job_item_acquired = True

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
      if self.town_level: net += self.town_level
      if self.monster_level: net += self.monster_level
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

  def is_last_day(self):
    return self.daynum == self.MAX_DAYS

@dataclass
class Day(BaseDay):
  daynum: int
  town_level: int = None
  town_gold_acquired: int = None
  monster_level: int = None
  monster_gold_acquired: int = None
  gold_spent: int = None
  terrain: int = None
  monster_kind: int = None
  monster_strength: int = None
  monster_weakness: int = None
  health_lost_from_town: int = None
  health_gained_from_town: int = None
  health_lost_from_monster: int = None
  health_gained_from_monster: int = None
  health_gained_otherwise: int = None
  job_played: str = ''
  job_item_acquired: bool = None
  played: bool = False

class BaseGame:
  ELEMENTS_COUNT = 14
  MONSTER_KINDS_COUNT = 14

  def __generate_day(self, daynum):
    element_maker = tw.TriangleWeight(self.ELEMENTS_COUNT)
    monster_maker = tw.TriangleWeight(self.MONSTER_KINDS_COUNT)
    attributes = {
      'daynum': daynum,
      'terrain': element_maker.trirand(),
      'town_level': random.randint(1, daynum) if random.randint(1, Day.MAX_DAYS) <= Day.MAX_DAYS - daynum else None,
      'monster_level': random.randint(1, daynum) if random.randint(1, Day.MAX_DAYS) <= daynum else None
    }
    if attributes['monster_level']:
      attributes['monster_kind'] = monster_maker.trirand()
      attributes['monster_strength'] = element_maker.reverse_trirand()
      attributes['monster_weakness'] = element_maker.reverse_trirand()
    self._add_day(attributes)

  def start(self):
    if self.days():
      raise InvalidMove("Game already started")
    for daynum in range(1, Day.MAX_DAYS):
      self.__generate_day(daynum)
    self._add_day({
      'daynum': Day.MAX_DAYS,
      'terrain': 1,
      'town_level': Day.MAX_DAYS,
      'monster_level': Day.MAX_DAYS,
      'monster_strength': 1,
      'monster_weakness': 2
    })

  def day(self, daynum):
    return self.days()[daynum - 1]

  def current_day(self):
    return next((day for day in self.days() if not day.played), None)

  # on or before current day
  def viewable_day(self, daynum):
    if daynum > self.current_day().daynum:
      return None
    return self.day(daynum)

  def gold(self):
    return sum([day.net_gold() for day in self.days()])

  def xp(self, job=None):
    check_job = lambda day : (day.played and job == day.job_played) if job else day.played
    return sum([day.net_xp() if check_job(day) else 0 for day in self.days()])

  def level(self, job):
    xp = self.xp(job)
    return tw.from_trinum_floor(xp) + 1 if xp else 1

  def items(self, job):
    return set([day.terrain for day in self.days() if day.job_played == job and day.job_item_acquired])

  def health(self):
    return 1 + sum([day.net_health() for day in self.days()])

  def play(self, job=None):
    day = self.current_day()
    if day.is_last_day():
      self.__final_boss()
    elif not job:
      raise InvalidMove("No job specified")
    elif job not in self.JOBS:
      raise InvalidMove("Unknown job")
    else:
      self.JOBS[job](self)
      day.job_played = job
    day.played = True

  def __monster_odds(self, job_level, monster_level=None):
    day = self.current_day()
    monster = day.monster
    if not monster:
      raise InvalidMove("No monster odds without monster")
    monster_level = monster_level or monster.gold
    if day.terrain == monster.strength():
      monster_level = monster_level * 2
    if day.terrain == monster.weakness():
      job_level = job_level * 2
    return (job_level, monster_level)

  def __warrior_odds(self, job_level=None, monster_level=None):
    job = 'warrior'
    day = self.current_day()
    monster = day.monster
    if not monster:
      raise InvalidMove("No warrior odds without monster")
    job_level = job_level or self.level(job)
    monster_level = monster_level or monster.gold
    if monster.strength() in self.items(job):
      job_level = job_level * 2
    return (job_level, monster_level)

  def __cleric_odds(self, job_level=None, target_level=None):
    job = 'cleric'
    day = self.current_day()
    job_level = job_level or self.level(job)
    if not target_level: target_level = day.town_level or day.daynum
    if day.terrain in self.items(job):
      job_level = job_level * 2
    return (job_level, target_level)

  def __thief_odds(self, job_level=None, town_level=None):
    job = 'thief'
    day = self.current_day()
    if not day.town_level:
      raise InvalidMove("No thief odds without town")
    job_level = job_level or self.level(job)
    if not town_level: town_level = day.town_level
    if day.terrain in self.items(job):
      town_level = town_level * 2 # it's a weakness
    return (job_level, town_level)

  def __wizard_odds(self, job_level=None, monster_level=None):
    job = 'warrior'
    day = self.current_day()
    monster = day.monster
    if not monster:
      raise InvalidMove("No wizard odds without monster")
    job_level = job_level or self.level(job)
    monster_level = monster_level or monster.gold
    if monster.weakness() in self.items(job):
      job_level = job_level * 2
    return (job_level, monster_level)

  def __ranger_odds(self, job_level=None, target_level=None):
    job = 'ranger'
    day = self.current_day()
    monster = day.monster
    town_level = day.town_level
    if not monster or town_level:
      raise InvalidMove("No ranger odds without monster or town")
    job_level = job_level or self.level(job)
    target_level = target_level or (monster.gold if monster else town_level)
    if day.terrain in self.items(job):
      job_level = job_level * 2
    return (job_level, target_level)

  def __final_boss_odds(self):
    level = self.__warrior_odds()[0]
    level += self.__cleric_odds()[0]
    level += self.__wizard_odds()[0]
    level += self.__ranger_odds()[0]
    odds = self.__monster_odds(level)
    odds = self.__thief_odds(*odds)
    return odds

  def __warrior(self):
    day = self.current_day()
    town_level = day.town_level
    monster_level = day.monster_level
    if monster_level:
      day.health_lost_from_monster = __hack(self.__monster_odds(*self.__warrior_odds()), self.health())
      if self.health() > 0:
        day.acquire_monster_gold()
        day.acquire_town_gold()
      else:
        day.health_gained_otherwise = 1
    elif town_level:
      day.acquire_job_item()

  def __cleric(self):
    day = self.current_day()
    town_level = day.town_level
    if town_level:
      if __swing(*self.__cleric_odds()):
        day.health_gained_from_town = town_level
        day.acquire_job_item()

  def __thief(self):
    day = self.current_day()
    town_level = day.town_level
    monster_level = day.monster_level
    if monster_level:
      if __swing(self.__monster_odds(self.level('thief'))):
        day.acquire_monster_gold()
      else:
        day.health_lost_from_monster = min(self.health(), self.monster_level)
    if self.health() > 0:
      if town_level:
        if __swing(self.__thief_odds()):
          day.acquire_town_gold()
        else:
          day.acquire_job_item() # weakness!
    else:
      day.health_gained_otherwise = 1

  def __wizard(self):
    day = self.current_day()
    town_level = day.town_level
    monster_level = day.monster_level
    # TODO: can only attack if health > 1
    if monster_level:
      if __swing(self.__monster_odds(*self.__wizard_odds())):
        day.acquire_monster_gold()
        day.acquire_town_gold()
      else:
        day.health_lost_from_monster = min(self.health(), monster_level)
    elif town_level:
      day.acquire_job_item()
    if self.health() <= 0:
      day.health_gained_otherwise = 1

  def __ranger(self):
    day = self.current_day()
    town_level = day.town_level
    monster_level = day.monster_level
    if monster_level:
      if __swing(self.__monster_odds(*self.__ranger_odds())):
        day.acquire_town_gold()
        day.health_gained_from_monster = monster_level
    elif town_level:
      day.health_lost_from_town = __hack(*self.__ranger_odds(), self.health())
      if self.health() > 0:
        day.acquire_town_gold()
      else:
        day.health_gained_otherwise = 1
    else:
      day.acquire_job_item()

  def __final_boss(self):
    day = self.current_day()
    if __swing(*self.__final_boss_odds()):
      day.acquire_monster_gold()
      day.acquire_town_gold()

  JOBS = {
    'warrior': __warrior,
    'cleric': __cleric,
    'thief': __thief,
    'wizard': __wizard,
    'ranger': __ranger
  }

@dataclass
class Game(BaseGame):
  player_name: str
  _days: list = field(default_factory=list)

  def _add_day(self, attributes):
    self._days.append(Day(**attributes))

  def days(self):
    return self._days

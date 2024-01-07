import random
import unittest
import jackhack.game as jh
from dataclasses import asdict

class GameTestCase(unittest.TestCase):

  @classmethod
  def game(cls):
    return jh.Game(player_name='Jack')

  @classmethod
  def started_game(cls):
    random.seed(1)
    game = cls.game()
    game.start()
    return game

  def test_player_name(self):
    self.assertEqual(self.game().player_name, "Jack")

  def test_start(self):
    actual_days = [asdict(day) for day in self.started_game().days()]
    ### Uncomment below when you need to regenerate EXPECTED_DAYS
    # for day in actual_days:
    #   print(f"{day},")
    self.assertEqual(actual_days, GameTestCase.EXPECTED_DAYS)

  def test_day(self):
    game = self.started_game()
    day = game.day(57)
    expected_day = self.EXPECTED_DAYS[56]
    self.assertEqual(asdict(day), expected_day)

  def test_current_day(self):
    game = self.started_game()
    for daynum in range(1,10):
      day = game.day(daynum)
      day.played = True
    today = game.current_day()
    expected_day = self.EXPECTED_DAYS[9]
    self.assertEqual(asdict(today), expected_day)

  def test_start_with_zero_gold(self):
    self.assertEqual(self.started_game().gold(), 0)

  def test_acquire_town_gold(self):
    game = self.started_game()
    day = game.day(6)
    day.acquire_town_gold()
    self.assertEqual(day.town_gold_acquired, 4)
    self.assertEqual(game.gold(), 4)

  def test_acquire_monster_gold(self):
    game = self.started_game()
    day = game.day(35)
    day.acquire_monster_gold()
    self.assertEqual(day.monster_gold_acquired, 31)
    self.assertEqual(game.gold(), 31)

  def test_spend_gold(self):
    game = self.started_game()
    day = game.day(18)
    day.acquire_town_gold()
    self.assertEqual(game.gold(), 16)
    day.spend_gold(5)
    self.assertEqual(day.gold_spent, 5)
    self.assertEqual(game.gold(), 11)

  def test_gold(self):
    game = self.started_game()
    tg = False
    mg = False
    sg = 1
    expected_gold = 0
    for daynum in range(1,100):
      day = game.day(daynum)
      if tg and day.town_gold:
        expected_gold += self.EXPECTED_DAYS[daynum - 1]["town_gold"]
        day.acquire_town_gold()
      if mg and day.monster_gold:
        expected_gold += self.EXPECTED_DAYS[daynum - 1]["monster_gold"]
        day.acquire_monster_gold()
      if sg == 4:
        spent_gold = int(daynum / 4)
        day.spend_gold(spent_gold)
        expected_gold -= int(spent_gold)
        sg = 1
      else:
        sg += 1
      if tg and mg: # both true, go to only mg true
        tg = False
      elif mg:      # only mg true, go to both false
        mg = False
      elif tg:      # only tg true, go to both true
        mg = True
      else:         # both false, go to only tg true
        tg = True
    # a dynamic test, in case we make changes to started_game, this should at least still pass
    self.assertEqual(game.gold(), expected_gold)
    # hard-coded value, for when we make changes that shouldn't change this value
    self.assertEqual(game.gold(), 811)

  def test_xp(self):
    game = self.started_game()
    job = 'warrior'
    for daynum in range(1,41):
      day = game.day(daynum)
      day.played = True
      day.job_played = job
      job = 'wizard' if job == 'warrior' else 'warrior'
    self.assertEqual(game.day(1).net_xp(), 1)   # town no monster, same as daynum
    self.assertEqual(game.day(3).net_xp(), 1)   # town no monster, less than daynum
    self.assertEqual(game.day(5).net_xp(), 5)   # no town or monster
    self.assertEqual(game.day(9).net_xp(), 9)   # monster no town, same as daynum
    self.assertEqual(game.day(28).net_xp(), 27) # town and monster, less than daynum
    self.assertEqual(game.day(35).net_xp(), 59) # town and monster, greater than daynum
    self.assertEqual(game.day(40).net_xp(), 15) # monster no town, less than daynum
    self.assertEqual(game.day(41).net_xp(), 0)  # not yet played
    self.assertEqual(game.xp(), 625)
    self.assertEqual(game.xp('warrior'), 313)
    self.assertEqual(game.xp('wizard'), 312)

  def test_level(self):
    game = self.started_game()
    job = 'warrior'
    for daynum in range(1,41):
      day = game.day(daynum)
      day.played = True
      day.job_played = job
      job = 'wizard' if job == 'warrior' else 'warrior'
    self.assertEqual(game.level('warrior'), 25)
    self.assertEqual(game.level('wizard'), 25)

  def test_items(self):
    game = self.started_game()
    job = 'warrior'
    for daynum in range(1,13):
      day = game.day(daynum)
      day.played = True
      day.job_played = job
      day.job_item_acquired = (daynum % 3 == 1)
      job = 'wizard' if job == 'warrior' else 'warrior'
    self.assertEqual(game.items('warrior'), set([6,14]))
    self.assertEqual(game.items('wizard'), set([11]))

  def test_health(self):
    game = self.started_game()
    for daynum in range(1,10):
      day = game.day(daynum)
      day.played = True
      # start health                                              #   1
      if daynum in range(1,5) or daynum in range(7, 9):           # + 6
        day.health_gained_from_town = 1
      day.health_lost_from_town = 2 if daynum == 6 else None      # - 2
      day.health_gained_otherwise = 5 if daynum == 5 else None    # + 5
      day.health_lost_from_monster = 4 if daynum == 9 else None   # - 4
      day.health_gained_from_monster = 9 if daynum == 9 else None # + 9
    self.assertEqual(game.health(), 15)                           # =15

  # see test_start if you need to regenerate this
  EXPECTED_DAYS = [
    {'daynum': 1, 'town_gold': 1, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 6, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 2, 'town_gold': 2, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 6, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 3, 'town_gold': 1, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 13, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 4, 'town_gold': 4, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 11, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 5, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 12, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 6, 'town_gold': 4, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 1, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 7, 'town_gold': 5, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 14, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 8, 'town_gold': 1, 'town_gold_acquired': None, 'monster_gold': 1, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 9, 'monster_kind': 10, 'monster_strength': 2, 'monster_weakness': 8, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 9, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': 9, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 10, 'monster_kind': 8, 'monster_strength': 1, 'monster_weakness': 4, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 10, 'town_gold': 4, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 11, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 11, 'town_gold': 4, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 8, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 12, 'town_gold': 1, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 11, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 13, 'town_gold': 2, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 12, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 14, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 13, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 15, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 6, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 16, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 14, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 17, 'town_gold': 7, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 10, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 18, 'town_gold': 16, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 9, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 19, 'town_gold': 2, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 10, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 20, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 8, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 21, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 10, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 22, 'town_gold': 22, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 10, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 23, 'town_gold': 15, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 10, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 24, 'town_gold': 6, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 11, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 25, 'town_gold': 16, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 10, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 26, 'town_gold': 2, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 3, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 27, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 13, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 28, 'town_gold': 21, 'town_gold_acquired': None, 'monster_gold': 6, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 12, 'monster_kind': 11, 'monster_strength': 7, 'monster_weakness': 13, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 29, 'town_gold': 18, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 14, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 30, 'town_gold': 17, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 8, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 31, 'town_gold': 15, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 12, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 32, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 13, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 33, 'town_gold': 25, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 14, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 34, 'town_gold': 34, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 11, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 35, 'town_gold': 28, 'town_gold_acquired': None, 'monster_gold': 31, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 12, 'monster_kind': 10, 'monster_strength': 3, 'monster_weakness': 3, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 36, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 7, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 37, 'town_gold': 27, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 11, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 38, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 1, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 39, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 13, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 40, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': 15, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 11, 'monster_kind': 13, 'monster_strength': 8, 'monster_weakness': 3, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 41, 'town_gold': 6, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 12, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 42, 'town_gold': 3, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 14, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 43, 'town_gold': 2, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 4, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 44, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 2, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 45, 'town_gold': 18, 'town_gold_acquired': None, 'monster_gold': 40, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 8, 'monster_kind': 7, 'monster_strength': 6, 'monster_weakness': 6, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 46, 'town_gold': 11, 'town_gold_acquired': None, 'monster_gold': 34, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 4, 'monster_kind': 7, 'monster_strength': 2, 'monster_weakness': 7, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 47, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': 30, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 13, 'monster_kind': 13, 'monster_strength': 6, 'monster_weakness': 4, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 48, 'town_gold': 2, 'town_gold_acquired': None, 'monster_gold': 25, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 11, 'monster_kind': 9, 'monster_strength': 5, 'monster_weakness': 1, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 49, 'town_gold': 7, 'town_gold_acquired': None, 'monster_gold': 47, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 7, 'monster_kind': 11, 'monster_strength': 8, 'monster_weakness': 3, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 50, 'town_gold': 15, 'town_gold_acquired': None, 'monster_gold': 26, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 11, 'monster_kind': 6, 'monster_strength': 12, 'monster_weakness': 1, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 51, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 6, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 52, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 11, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 53, 'town_gold': 41, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 12, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 54, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': 34, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 12, 'monster_kind': 13, 'monster_strength': 12, 'monster_weakness': 5, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 55, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': 43, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 13, 'monster_kind': 13, 'monster_strength': 5, 'monster_weakness': 11, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 56, 'town_gold': 9, 'town_gold_acquired': None, 'monster_gold': 4, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 14, 'monster_kind': 9, 'monster_strength': 11, 'monster_weakness': 11, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 57, 'town_gold': 48, 'town_gold_acquired': None, 'monster_gold': 27, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 9, 'monster_kind': 12, 'monster_strength': 7, 'monster_weakness': 9, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 58, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': 38, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 2, 'monster_kind': 14, 'monster_strength': 8, 'monster_weakness': 3, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 59, 'town_gold': 53, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 11, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 60, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 13, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 61, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': 23, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 3, 'monster_kind': 5, 'monster_strength': 8, 'monster_weakness': 3, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 62, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 13, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 63, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': 61, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 7, 'monster_kind': 13, 'monster_strength': 5, 'monster_weakness': 6, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 64, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': 42, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 11, 'monster_kind': 13, 'monster_strength': 5, 'monster_weakness': 6, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 65, 'town_gold': 26, 'town_gold_acquired': None, 'monster_gold': 18, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 2, 'monster_kind': 9, 'monster_strength': 5, 'monster_weakness': 8, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 66, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': 49, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 8, 'monster_kind': 12, 'monster_strength': 6, 'monster_weakness': 2, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 67, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 12, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 68, 'town_gold': 9, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 12, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 69, 'town_gold': 18, 'town_gold_acquired': None, 'monster_gold': 22, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 3, 'monster_kind': 12, 'monster_strength': 8, 'monster_weakness': 7, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 70, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 14, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 71, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': 44, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 11, 'monster_kind': 9, 'monster_strength': 10, 'monster_weakness': 6, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 72, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 8, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 73, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': 71, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 14, 'monster_kind': 14, 'monster_strength': 10, 'monster_weakness': 6, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 74, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': 49, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 3, 'monster_kind': 14, 'monster_strength': 9, 'monster_weakness': 9, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 75, 'town_gold': 49, 'town_gold_acquired': None, 'monster_gold': 74, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 9, 'monster_kind': 12, 'monster_strength': 7, 'monster_weakness': 3, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 76, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': 38, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 5, 'monster_kind': 12, 'monster_strength': 3, 'monster_weakness': 10, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 77, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': 6, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 11, 'monster_kind': 9, 'monster_strength': 13, 'monster_weakness': 2, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 78, 'town_gold': 12, 'town_gold_acquired': None, 'monster_gold': 15, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 13, 'monster_kind': 14, 'monster_strength': 12, 'monster_weakness': 8, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 79, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': 21, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 8, 'monster_kind': 5, 'monster_strength': 4, 'monster_weakness': 8, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 80, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': 14, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 13, 'monster_kind': 11, 'monster_strength': 5, 'monster_weakness': 1, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 81, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': 33, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 12, 'monster_kind': 14, 'monster_strength': 4, 'monster_weakness': 6, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 82, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 5, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 83, 'town_gold': 4, 'town_gold_acquired': None, 'monster_gold': 38, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 9, 'monster_kind': 14, 'monster_strength': 3, 'monster_weakness': 6, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 84, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': 52, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 11, 'monster_kind': 4, 'monster_strength': 11, 'monster_weakness': 6, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 85, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': 33, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 12, 'monster_kind': 7, 'monster_strength': 1, 'monster_weakness': 2, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 86, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 14, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 87, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': 34, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 11, 'monster_kind': 7, 'monster_strength': 3, 'monster_weakness': 8, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 88, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': 47, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 9, 'monster_kind': 5, 'monster_strength': 1, 'monster_weakness': 7, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 89, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': 12, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 5, 'monster_kind': 13, 'monster_strength': 3, 'monster_weakness': 2, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 90, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': 40, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 9, 'monster_kind': 3, 'monster_strength': 6, 'monster_weakness': 8, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 91, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': 32, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 9, 'monster_kind': 9, 'monster_strength': 10, 'monster_weakness': 3, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 92, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': 12, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 13, 'monster_kind': 8, 'monster_strength': 7, 'monster_weakness': 13, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 93, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': 10, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 14, 'monster_kind': 8, 'monster_strength': 3, 'monster_weakness': 11, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 94, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': 82, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 14, 'monster_kind': 2, 'monster_strength': 6, 'monster_weakness': 1, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 95, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': 61, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 14, 'monster_kind': 6, 'monster_strength': 10, 'monster_weakness': 4, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 96, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': 66, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 14, 'monster_kind': 13, 'monster_strength': 8, 'monster_weakness': 8, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 97, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': 41, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 14, 'monster_kind': 9, 'monster_strength': 10, 'monster_weakness': 2, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 98, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': 17, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 11, 'monster_kind': 7, 'monster_strength': 9, 'monster_weakness': 3, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 99, 'town_gold': None, 'town_gold_acquired': None, 'monster_gold': None, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 14, 'monster_kind': None, 'monster_strength': None, 'monster_weakness': None, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False},
    {'daynum': 100, 'town_gold': 100, 'town_gold_acquired': None, 'monster_gold': 100, 'monster_gold_acquired': None, 'gold_spent': None, 'terrain': 1, 'monster_kind': None, 'monster_strength': 1, 'monster_weakness': 2, 'health_lost_from_town': None, 'health_gained_from_town': None, 'health_lost_from_monster': None, 'health_gained_from_monster': None, 'health_gained_otherwise': None, 'job_played': '', 'job_item_acquired': None, 'played': False}
  ]

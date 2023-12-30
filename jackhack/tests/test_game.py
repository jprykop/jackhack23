import random
import unittest
import jackhack.game as jh

class GameTestCase(unittest.TestCase):
  EXPECTED_DAYS = [
    {'daynum': 1, 'town_gold': 1, 'monster_gold': None, 'played': False},
    {'daynum': 2, 'town_gold': 2, 'monster_gold': None, 'played': False},
    {'daynum': 3, 'town_gold': 2, 'monster_gold': None, 'played': False},
    {'daynum': 4, 'town_gold': 2, 'monster_gold': None, 'played': False},
    {'daynum': 5, 'town_gold': 1, 'monster_gold': None, 'played': False},
    {'daynum': 6, 'town_gold': 5, 'monster_gold': None, 'played': False},
    {'daynum': 7, 'town_gold': None, 'monster_gold': 6, 'played': False},
    {'daynum': 8, 'town_gold': 5, 'monster_gold': None, 'played': False},
    {'daynum': 9, 'town_gold': 2, 'monster_gold': None, 'played': False},
    {'daynum': 10, 'town_gold': 1, 'monster_gold': 9, 'played': False},
    {'daynum': 11, 'town_gold': 7, 'monster_gold': None, 'played': False},
    {'daynum': 12, 'town_gold': 7, 'monster_gold': None, 'played': False},
    {'daynum': 13, 'town_gold': 9, 'monster_gold': None, 'played': False},
    {'daynum': 14, 'town_gold': None, 'monster_gold': None, 'played': False},
    {'daynum': 15, 'town_gold': 9, 'monster_gold': None, 'played': False},
    {'daynum': 16, 'town_gold': 8, 'monster_gold': None, 'played': False},
    {'daynum': 17, 'town_gold': 15, 'monster_gold': None, 'played': False},
    {'daynum': 18, 'town_gold': 14, 'monster_gold': None, 'played': False},
    {'daynum': 19, 'town_gold': None, 'monster_gold': 6, 'played': False},
    {'daynum': 20, 'town_gold': None, 'monster_gold': None, 'played': False},
    {'daynum': 21, 'town_gold': 4, 'monster_gold': None, 'played': False},
    {'daynum': 22, 'town_gold': 17, 'monster_gold': None, 'played': False},
    {'daynum': 23, 'town_gold': 22, 'monster_gold': None, 'played': False},
    {'daynum': 24, 'town_gold': 10, 'monster_gold': None, 'played': False},
    {'daynum': 25, 'town_gold': 17, 'monster_gold': None, 'played': False},
    {'daynum': 26, 'town_gold': None, 'monster_gold': 16, 'played': False},
    {'daynum': 27, 'town_gold': 24, 'monster_gold': None, 'played': False},
    {'daynum': 28, 'town_gold': 22, 'monster_gold': 12, 'played': False},
    {'daynum': 29, 'town_gold': 29, 'monster_gold': None, 'played': False},
    {'daynum': 30, 'town_gold': None, 'monster_gold': None, 'played': False},
    {'daynum': 31, 'town_gold': None, 'monster_gold': None, 'played': False},
    {'daynum': 32, 'town_gold': 29, 'monster_gold': None, 'played': False},
    {'daynum': 33, 'town_gold': 7, 'monster_gold': None, 'played': False},
    {'daynum': 34, 'town_gold': 34, 'monster_gold': None, 'played': False},
    {'daynum': 35, 'town_gold': 32, 'monster_gold': None, 'played': False},
    {'daynum': 36, 'town_gold': 31, 'monster_gold': 20, 'played': False},
    {'daynum': 37, 'town_gold': None, 'monster_gold': None, 'played': False},
    {'daynum': 38, 'town_gold': None, 'monster_gold': None, 'played': False},
    {'daynum': 39, 'town_gold': 11, 'monster_gold': 33, 'played': False},
    {'daynum': 40, 'town_gold': 1, 'monster_gold': None, 'played': False},
    {'daynum': 41, 'town_gold': 35, 'monster_gold': None, 'played': False},
    {'daynum': 42, 'town_gold': 26, 'monster_gold': None, 'played': False},
    {'daynum': 43, 'town_gold': 37, 'monster_gold': None, 'played': False},
    {'daynum': 44, 'town_gold': None, 'monster_gold': 43, 'played': False},
    {'daynum': 45, 'town_gold': None, 'monster_gold': None, 'played': False},
    {'daynum': 46, 'town_gold': None, 'monster_gold': 25, 'played': False},
    {'daynum': 47, 'town_gold': None, 'monster_gold': None, 'played': False},
    {'daynum': 48, 'town_gold': 34, 'monster_gold': None, 'played': False},
    {'daynum': 49, 'town_gold': None, 'monster_gold': 28, 'played': False},
    {'daynum': 50, 'town_gold': 31, 'monster_gold': 37, 'played': False},
    {'daynum': 51, 'town_gold': None, 'monster_gold': 33, 'played': False},
    {'daynum': 52, 'town_gold': None, 'monster_gold': None, 'played': False},
    {'daynum': 53, 'town_gold': 27, 'monster_gold': 1, 'played': False},
    {'daynum': 54, 'town_gold': None, 'monster_gold': None, 'played': False},
    {'daynum': 55, 'town_gold': None, 'monster_gold': None, 'played': False},
    {'daynum': 56, 'town_gold': 30, 'monster_gold': None, 'played': False},
    {'daynum': 57, 'town_gold': 52, 'monster_gold': 41, 'played': False},
    {'daynum': 58, 'town_gold': 36, 'monster_gold': None, 'played': False},
    {'daynum': 59, 'town_gold': 56, 'monster_gold': 52, 'played': False},
    {'daynum': 60, 'town_gold': None, 'monster_gold': 3, 'played': False},
    {'daynum': 61, 'town_gold': None, 'monster_gold': 6, 'played': False},
    {'daynum': 62, 'town_gold': 29, 'monster_gold': 49, 'played': False},
    {'daynum': 63, 'town_gold': None, 'monster_gold': 16, 'played': False},
    {'daynum': 64, 'town_gold': 15, 'monster_gold': None, 'played': False},
    {'daynum': 65, 'town_gold': 45, 'monster_gold': 9, 'played': False},
    {'daynum': 66, 'town_gold': 21, 'monster_gold': 22, 'played': False},
    {'daynum': 67, 'town_gold': None, 'monster_gold': 38, 'played': False},
    {'daynum': 68, 'town_gold': None, 'monster_gold': None, 'played': False},
    {'daynum': 69, 'town_gold': None, 'monster_gold': 61, 'played': False},
    {'daynum': 70, 'town_gold': 4, 'monster_gold': 50, 'played': False},
    {'daynum': 71, 'town_gold': None, 'monster_gold': 25, 'played': False},
    {'daynum': 72, 'town_gold': None, 'monster_gold': 33, 'played': False},
    {'daynum': 73, 'town_gold': None, 'monster_gold': 27, 'played': False},
    {'daynum': 74, 'town_gold': None, 'monster_gold': 3, 'played': False},
    {'daynum': 75, 'town_gold': None, 'monster_gold': 51, 'played': False},
    {'daynum': 76, 'town_gold': 5, 'monster_gold': None, 'played': False},
    {'daynum': 77, 'town_gold': 58, 'monster_gold': None, 'played': False},
    {'daynum': 78, 'town_gold': None, 'monster_gold': None, 'played': False},
    {'daynum': 79, 'town_gold': None, 'monster_gold': 29, 'played': False},
    {'daynum': 80, 'town_gold': None, 'monster_gold': None, 'played': False},
    {'daynum': 81, 'town_gold': None, 'monster_gold': 29, 'played': False},
    {'daynum': 82, 'town_gold': None, 'monster_gold': None, 'played': False},
    {'daynum': 83, 'town_gold': 51, 'monster_gold': None, 'played': False},
    {'daynum': 84, 'town_gold': None, 'monster_gold': 81, 'played': False},
    {'daynum': 85, 'town_gold': None, 'monster_gold': 39, 'played': False},
    {'daynum': 86, 'town_gold': None, 'monster_gold': 7, 'played': False},
    {'daynum': 87, 'town_gold': None, 'monster_gold': 10, 'played': False},
    {'daynum': 88, 'town_gold': None, 'monster_gold': 21, 'played': False},
    {'daynum': 89, 'town_gold': None, 'monster_gold': 33, 'played': False},
    {'daynum': 90, 'town_gold': None, 'monster_gold': 72, 'played': False},
    {'daynum': 91, 'town_gold': 76, 'monster_gold': 73, 'played': False},
    {'daynum': 92, 'town_gold': None, 'monster_gold': 91, 'played': False},
    {'daynum': 93, 'town_gold': None, 'monster_gold': 5, 'played': False},
    {'daynum': 94, 'town_gold': None, 'monster_gold': 45, 'played': False},
    {'daynum': 95, 'town_gold': None, 'monster_gold': 74, 'played': False},
    {'daynum': 96, 'town_gold': None, 'monster_gold': 76, 'played': False},
    {'daynum': 97, 'town_gold': None, 'monster_gold': 14, 'played': False},
    {'daynum': 98, 'town_gold': None, 'monster_gold': 38, 'played': False},
    {'daynum': 99, 'town_gold': None, 'monster_gold': 3, 'played': False},
    {'daynum': 100, 'town_gold': 100, 'monster_gold': 100, 'played': False}
  ]

  @classmethod
  def game(cls):
    return jh.Game(player_name='Jack')
  
  @classmethod
  def started_game(cls):
    random.seed(1)
    game = cls.game()
    game.start()
    return game

  @classmethod
  def days_to_dicts(cls, game):
    return [day.to_dict() for day in game.days()]

  def test_player_name(self):
    self.assertEqual(self.game().player_name, "Jack")

  def test_start(self):
    self.assertEqual(self.days_to_dicts(self.started_game()), GameTestCase.EXPECTED_DAYS)

  def test_day(self):
    game = self.started_game()
    day = game.day(57)
    expected_day = self.EXPECTED_DAYS[56]
    self.assertEqual(day.to_dict(), expected_day)

  def test_current_day(self):
    game = self.started_game()
    for daynum in range(1,10):
      day = game.day(daynum)
      day.played = True
    game._save_game()
    today = game.current_day()
    expected_day = self.EXPECTED_DAYS[9]
    self.assertEqual(today.to_dict(), expected_day)

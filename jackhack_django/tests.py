from django.test import TestCase
from jackhack_django.models import SaveGame
from jackhack.tests.test_game import GameTestCase

class SaveGameTest(GameTestCase, TestCase):
  @classmethod
  def game(self):
    return SaveGame.objects.create(player_name="Jack")

  def test_player_name(self):
    game = SaveGame.objects.create(player_name="Jack")
    self.assertEqual(game.player_name, "Jack")
    game_reloaded = SaveGame.objects.get(player_name="Jack")
    self.assertEqual(game_reloaded.player_name, "Jack")

  def test_started_game_saved(self):
    game = self.started_game()
    reloaded_game = SaveGame.objects.get(id=game.id)
    self.assertEqual(GameTestCase.EXPECTED_DAYS, [{'daynum': d.daynum, 'town_gold': d.town_gold, 'monster_gold': d.monster_gold, 'played': d.played} for d in reloaded_game.days()])

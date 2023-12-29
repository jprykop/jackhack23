from django.test import TestCase
from jackhack_django.models import SaveGame
from jackhack.tests.test_game import GameTestCase

class SaveGameTest(GameTestCase, TestCase):
  @classmethod
  def game(self):
    return SaveGame.objects.create(player_name="Jack")

  def test_saved_player_name(self):
    reloaded_game = SaveGame.objects.get(id=self.game().id)
    self.assertEqual(reloaded_game.player_name, "Jack")

  def test_started_game_saved(self):
    reloaded_game = SaveGame.objects.get(id=self.started_game().id)
    self.assertEqual(self.days_to_dicts(reloaded_game), GameTestCase.EXPECTED_DAYS)

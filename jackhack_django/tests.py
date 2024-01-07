from django.test import TestCase
from jackhack_django.models import SaveGame
from jackhack.tests.test_game import GameTestCase

class SaveGameTest(GameTestCase, TestCase):
  @classmethod
  def game(self):
    return SaveGame.objects.create(player_name="Jack")

  def test_saved_player_name(self):
    initialized_game = self.game()
    initialized_game.save_game()
    reloaded_game = SaveGame.objects.get(id=initialized_game.id)
    self.assertEqual(reloaded_game.player_name, "Jack")

  def test_saved_game_started(self):
    initialized_game = self.started_game()
    initialized_game.save_game()
    reloaded_game = SaveGame.objects.get(id=initialized_game.id)
    self.assertEqual([day.as_dict() for day in reloaded_game.days()], self.EXPECTED_DAYS)

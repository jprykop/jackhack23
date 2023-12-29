from django.test import TestCase
from jackhack_django.models import SaveGame

class SaveGameTest(TestCase):
  def test_player_name(self):
    game = SaveGame.objects.create(player_name="Jack")
    self.assertEqual(game.player_name, "Jack")
    self.assertEqual(game.player_name_from_game, "Jack")
    game_reloaded = SaveGame.objects.get(player_name="Jack")
    self.assertEqual(game_reloaded.player_name, "Jack")
    self.assertEqual(game_reloaded.player_name_from_game, "Jack")

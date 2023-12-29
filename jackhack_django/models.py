from typing import Any
from django.db import models
from django.forms.models import model_to_dict
import jackhack.game

class SaveGame(jackhack.game.Game, models.Model):
  player_name = models.CharField(max_length=16)
  # warrior_xp = models.IntegerField(default=0)
  # healer_xp = models.IntegerField(default=0)
  # thief_xp = models.IntegerField(default=0)
  # wizard_xp = models.IntegerField(default=0)
  # hunter_xp = models.IntegerField(default=0)

  def __init__(self, *args, **kwargs):
    models.Model.__init__(self, *args, **kwargs)
#    gameargs = model_to_dict(self, fields=[field.name for field in self._meta.fields])
#    jackhack.game.Game.__init__(self, **gameargs)
    jackhack.game.Game.__init__(self, player_name=self.player_name)

# class Day(models.Model):
#   game = models.ForeignKey(Game, on_delete=models.CASCADE)
#   town_gold = models.IntegerField(blank=True, null=True)
#   monster_gold = models.IntegerField(blank=True, null=True)
#   terrain = models.IntegerField()

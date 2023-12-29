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

  def _add_day(self, attributes):
    SaveDay.objects.create(game=self, **attributes)

  def days(self):
    return self.saveday_set.all()

class SaveDay(jackhack.game.Day, models.Model):
  game = models.ForeignKey(SaveGame, on_delete=models.CASCADE)
  daynum = models.IntegerField(choices=[(x,x) for x in range(1,101)])
  town_gold = models.IntegerField(blank=True, null=True)
  monster_gold = models.IntegerField(blank=True, null=True)
  played = models.BooleanField(default=False)

  def __init__(self, *args, **kwargs):
    models.Model.__init__(self, *args, **kwargs)

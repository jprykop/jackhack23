from typing import Any
from django.db import models
from jackhack.game import BaseGame, BaseDay

class SaveGame(BaseGame, models.Model):
  player_name = models.CharField(max_length=16)

  def __init__(self, *args, **kwargs):
    models.Model.__init__(self, *args, **kwargs)
    self._days = None

  def _add_day(self, attributes):
    SaveDay.objects.create(game=self, **attributes)
    self._days = None

  def days(self):
    if self._days is None:
      self._days = list(self.saveday_set.all())
    return self._days

  def save_game(self):
    self.save()
    for day in self.days():
      day.save()

class SaveDay(BaseDay, models.Model):
  game = models.ForeignKey(SaveGame, on_delete=models.CASCADE)
  daynum = models.IntegerField(choices=[(x,x) for x in range(1, BaseDay.MAX_DAYS + 1)])
  town_level = models.IntegerField(blank=True, null=True, choices=[(x,x) for x in range(1, BaseDay.MAX_DAYS + 1)])
  town_gold_acquired = models.IntegerField(blank=True, null=True, choices=[(x,x) for x in range(1, BaseDay.MAX_DAYS + 1)])
  monster_level = models.IntegerField(blank=True, null=True, choices=[(x,x) for x in range(1, BaseDay.MAX_DAYS + 1)])
  monster_gold_acquired = models.IntegerField(blank=True, null=True, choices=[(x,x) for x in range(1, BaseDay.MAX_DAYS + 1)])
  gold_spent = models.IntegerField(blank=True, null=True, choices=[(x,x) for x in range(1, BaseDay.MAX_DAYS + 1)])
  terrain = models.IntegerField(blank=True, null=True, choices=[(x,x) for x in range(1, BaseGame.ELEMENTS_COUNT + 1)])
  monster_kind = models.IntegerField(blank=True, null=True, choices=[(x,x) for x in range(1, BaseGame.MONSTER_KINDS_COUNT + 1)])
  monster_strength = models.IntegerField(blank=True, null=True, choices=[(x,x) for x in range(1, BaseGame.ELEMENTS_COUNT + 1)])
  monster_weakness = models.IntegerField(blank=True, null=True, choices=[(x,x) for x in range(1, BaseGame.ELEMENTS_COUNT + 1)])
  health_lost_from_town = models.IntegerField(blank=True, null=True, choices=[(x,x) for x in range(1, BaseDay.MAX_DAYS + 1)])
  health_gained_from_town = models.IntegerField(blank=True, null=True, choices=[(x,x) for x in range(1, BaseDay.MAX_DAYS + 1)])
  health_lost_from_monster = models.IntegerField(blank=True, null=True, choices=[(x,x) for x in range(1, BaseDay.MAX_DAYS + 1)])
  health_gained_from_monster = models.IntegerField(blank=True, null=True, choices=[(x,x) for x in range(1, BaseDay.MAX_DAYS + 1)])
  health_gained_otherwise = models.IntegerField(blank=True, null=True, choices=[(x,x) for x in range(1, BaseDay.MAX_DAYS + 1)])
  job_played = models.CharField(max_length=16, blank=True)
  job_item_acquired = models.BooleanField(blank=True, null=True)
  played = models.BooleanField(default=False)

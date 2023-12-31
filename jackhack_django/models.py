from typing import Any
from django.db import models
from jackhack.game import Game, Day, MonsterKind, Element

class SaveGame(Game, models.Model):
  player_name = models.CharField(max_length=16)
  # warrior_xp = models.IntegerField(default=0)
  # healer_xp = models.IntegerField(default=0)
  # thief_xp = models.IntegerField(default=0)
  # wizard_xp = models.IntegerField(default=0)
  # hunter_xp = models.IntegerField(default=0)

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

  def _save_game(self):
    self.save()
    for day in self.days():
      day.save()

class SaveDay(Day, models.Model):
  game = models.ForeignKey(SaveGame, on_delete=models.CASCADE)
  daynum = models.IntegerField(choices=[(x,x) for x in range(1, Day.MAX_DAYS + 1)])
  town_gold = models.IntegerField(blank=True, null=True, choices=[(x,x) for x in range(1, Day.MAX_DAYS + 1)])
  town_gold_acquired = models.IntegerField(blank=True, null=True, choices=[(x,x) for x in range(1, Day.MAX_DAYS + 1)])
  monster_gold = models.IntegerField(blank=True, null=True, choices=[(x,x) for x in range(1, Day.MAX_DAYS + 1)])
  monster_gold_acquired = models.IntegerField(blank=True, null=True, choices=[(x,x) for x in range(1, Day.MAX_DAYS + 1)])
  gold_spent = models.IntegerField(blank=True, null=True, choices=[(x,x) for x in range(1, Day.MAX_DAYS + 1)])
  terrain_number = models.IntegerField(blank=True, null=True, choices=[(x,x) for x in range(1, Element.MAX + 1)])
  monster_kind_number = models.IntegerField(blank=True, null=True, choices=[(x,x) for x in range(1, MonsterKind.MAX + 1)])
  monster_strength_number = models.IntegerField(blank=True, null=True, choices=[(x,x) for x in range(1, Element.MAX + 1)])
  monster_weakness_number = models.IntegerField(blank=True, null=True, choices=[(x,x) for x in range(1, Element.MAX + 1)])
  job_played = models.CharField(max_length=16, blank=True)
  job_item_acquired = models.BooleanField(blank=True, null=True)
  played = models.BooleanField(default=False)

  def __init__(self, *args, **kwargs):
    models.Model.__init__(self, *args, **kwargs)

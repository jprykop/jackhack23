from django import forms
from jackhack.game import Game

class NewGameForm(forms.Form):
  player_name = forms.CharField(label="Character name", max_length=16)

class PlayForm(forms.Form):
  job = forms.ChoiceField(choices=Game.JOBS.keys())

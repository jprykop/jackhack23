from django.views.generic.base import View
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import SaveGame
from .forms import NewGameForm

class NewGameView(View):
  def get(self, request):
    request.session['game_id'] = ''
    new_game_form = NewGameForm()
    return render(request, "new_game.html", {
      'new_game_form': new_game_form
    })

  def post(self, request):
    new_game_form = NewGameForm(request.POST)
    if new_game_form.is_valid():
      game = SaveGame.objects.create(
        player_name = new_game_form.cleaned_data['player_name'],
        session_id = request.session.session_key
      )
      request.session['game_id'] = game.id
      game.start()
      return redirect(reverse('day', kwargs={'game_id': game.id, 'daynum': 1}))

class DayView(View):
  def get(self, request, **kwargs):
    game = SaveGame.objects.get(id=kwargs['game_id'])
    day = game.viewable_day(kwargs['daynum'])
    return render(request, "day.html", {
      'game': game,
      'day': day
    })

  def post(self, request, **kwargs):
    game = SaveGame.objects.get(id=kwargs['game_id'], session_id=request.session.session_key)

from django.urls import path
from . import views

urlpatterns = [
    path("", views.NewGameView.as_view(), name="new_game"),
    path("<int:game_id>/<int:daynum>", views.DayView.as_view(), name="day")
]

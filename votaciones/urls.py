from tkinter.font import names

from django.urls import path
from . import views

app_name = "votaciones"
urlpatterns = [
    # /Votaciones/
    path("", views.IndexView.as_view(), name="index"),
    # /Votaciones/id/
    path("<int:pk>/votar/", views.DetailView.as_view(), name="detail"),
    # /Votaciones/id/results
    path("<int:pk>/results/", views.ResultView.as_view(), name='results'),
    # /Votaciones/id/vote
    path("<int:pregunta_id>/vote/", views.vote, name="vote"),
]
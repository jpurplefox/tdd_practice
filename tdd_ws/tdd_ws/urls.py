from django.urls import path

from pokemon import views

urlpatterns = [
    path('pokemon/<int:pk>/moves/', views.Moves.as_view()),
]

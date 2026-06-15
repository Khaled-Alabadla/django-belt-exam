from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create/', views.game_create, name='create'),
    path('<int:pk>/details', views.details, name='details'),
    path('<int:pk>/edit/', views.game_update, name='edit'),
    path('<int:pk>/delete/', views.game_delete, name='delete'),
]

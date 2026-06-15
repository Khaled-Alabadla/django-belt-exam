from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from accounts.models import User


class GameManager(models.Manager):
    pass

    
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="games")
    description = models.TextField(blank=True)
    users = models.ManyToManyField(User, related_name="games")
    release_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users_who_like = models.ManyToManyField(User, related_name="liked_games")

    objects = GameManager()


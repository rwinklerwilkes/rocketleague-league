from django.db import models
from stats.models import Game

# Create your models here.
class Replay(models.Model):
    game = models.ForeignKey(Game)
    file = models.FileField(upload_to='replays/',null=True)

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from stats.models import Player, GameStats
import os.path

@receiver(post_save,sender=GameStats)
@receiver(post_delete,sender=GameStats)
def update_player_stats(sender,instance,**kwargs):
    p = instance.player
    p.update_stats()

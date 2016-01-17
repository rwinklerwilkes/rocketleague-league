from django.contrib import admin

from .models import Player, Team, Season, GameWeek
from .models import Game, GameStats

# Register your models here.
admin.site.register(Player)
admin.site.register(Team)
admin.site.register(Season)
admin.site.register(GameWeek)
admin.site.register(Game)
admin.site.register(GameStats)

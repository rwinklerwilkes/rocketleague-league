from django.db import models
from django.core.urlresolvers import reverse

class Team(models.Model):
    key = models.SlugField(unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name + ' ' + '(%s)'%self.key

# Create your models here.
class Player(models.Model):
    player_first_name = models.CharField(max_length=200)
    player_last_name = models.CharField(max_length=200)
    player_nickname = models.CharField(max_length=200,primary_key=True)
    lifetime_goals = models.IntegerField(default=0)
    lifetime_assists = models.IntegerField(default=0)
    lifetime_saves = models.IntegerField(default=0)
    lifetime_shots = models.IntegerField(default=0)
    lifetime_points = models.IntegerField(default=0)

    player_team = models.ForeignKey(Team,default=0)

    class Meta:
        ordering = ['-player_last_name']

    def update_stats(self):
        gs = GameStats.objects.filter(player=self)
        self.lifetime_goals = gs.aggregate(models.Sum('goals'))['goals__sum']
        self.lifetime_assists = gs.aggregate(models.Sum('assists'))['assists__sum']
        self.lifetime_saves = gs.aggregate(models.Sum('saves'))['saves__sum']
        self.lifetime_shots = gs.aggregate(models.Sum('shots'))['shots__sum']
        self.lifetime_points = gs.aggregate(models.Sum('points'))['points__sum']

    def get_absolute_url(self):
        return reverse('stats.views.player',args=[player_nickname])

    def __str__(self):
        return self.player_nickname

class Season(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class GameWeek(models.Model):
    season = models.ForeignKey(Season)
    number = models.PositiveIntegerField()
    starts_at = models.DateField()
    ends_at = models.DateField()

    class Meta:
        unique_together = [('season','number')]

    def __str__(self):
        return '%s Week %i'%(self.season,self.number)

class Game(models.Model):
    gameweek = models.ForeignKey(GameWeek)
    outcome = models.CharField(max_length=8)
    series_number = models.PositiveSmallIntegerField(default=1)

    home_team = models.ForeignKey(Team,related_name='home_games')
    home_team_score = models.PositiveSmallIntegerField()

    away_team = models.ForeignKey(Team,related_name='away_games')
    away_team_score = models.PositiveSmallIntegerField()

    def __str__(self):
        return '%s vs. %s Game %i'%(self.home_team,self.away_team,self.series_number)

class GameStats(models.Model):
    game = models.ForeignKey(Game)
    player = models.ForeignKey(Player)

    goals = models.PositiveIntegerField()
    assists = models.PositiveIntegerField()
    saves = models.PositiveIntegerField()
    shots = models.PositiveIntegerField()
    points = models.PositiveIntegerField()

    class Meta:
        unique_together = [('game','player')]

    def __str__(self):
        return 'Game: %s Player %s'%(self.game,self.player)
    

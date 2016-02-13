from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class Team(models.Model):
    key = models.SlugField(unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name + ' ' + '(%s)'%self.key

# Create your models here.
class Player(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    player_first_name = models.CharField(max_length=200)
    player_last_name = models.CharField(max_length=200)
    player_nickname = models.CharField(max_length=200,primary_key=True)

    profile_pic = models.ImageField(upload_to='avatars/',null=True)
    
    lifetime_goals = models.IntegerField(default=0)
    lifetime_assists = models.IntegerField(default=0)
    lifetime_saves = models.IntegerField(default=0)
    lifetime_shots = models.IntegerField(default=0)
    lifetime_points = models.IntegerField(default=0)

    player_team = models.ForeignKey(Team,default=0)

    class Meta:
        ordering = ['-player_last_name','player_first_name']

    def update_stats(self):
        gs = GameStats.objects.filter(player=self)
        self.lifetime_goals = gs.aggregate(models.Sum('goals'))['goals__sum']
        self.lifetime_assists = gs.aggregate(models.Sum('assists'))['assists__sum']
        self.lifetime_saves = gs.aggregate(models.Sum('saves'))['saves__sum']
        self.lifetime_shots = gs.aggregate(models.Sum('shots'))['shots__sum']
        self.lifetime_points = gs.aggregate(models.Sum('points'))['points__sum']

    def get_absolute_url(self):
        return reverse('stats.views.player',args=[player_nickname])

    def get_prof_pic(self):
        if self.profile_pic != None:
            return self.profile_pic.url
        else:
            return '#'

    def get_prof_stats(self):
        pts = [('goals',self.lifetime_goals,self.lifetime_goals*100),('assists',self.lifetime_assists,self.lifetime_assists*50),('saves',self.lifetime_saves,self.lifetime_saves*50),('shots',self.lifetime_shots,self.lifetime_shots*20)]
        pts = sorted(pts,key=lambda x:x[2],reverse=True)
        print(pts)
        return pts[:2]

    def _shot_pct(self):
        try:
            out = round(self.lifetime_goals/self.lifetime_shots,3)
        except:
            out = 0
        return "{0:3.1f}%".format(out*100)
    shot_pct = property(_shot_pct)

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
    home_team_score = models.PositiveSmallIntegerField(default=0)

    away_team = models.ForeignKey(Team,related_name='away_games')
    away_team_score = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return '%s vs. %s Game %i'%(self.home_team,self.away_team,self.series_number)

class GameStats(models.Model):
    game = models.ForeignKey(Game)
    player = models.ForeignKey(Player)

    goals = models.PositiveIntegerField(default=0)
    assists = models.PositiveIntegerField(default=0)
    saves = models.PositiveIntegerField(default=0)
    shots = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = [('game','player')]

    def __str__(self):
        return 'Game: %s Player %s'%(self.game,self.player)
    

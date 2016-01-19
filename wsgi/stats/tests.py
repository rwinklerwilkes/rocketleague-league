from django.test import TestCase
from django.utils import timezone

from .models import GameWeek,GameStats,Game,Season,Team,Player

# Create your tests here.
class SignalTests(TestCase):
    def test_gamestats_add_signal(self):
        test_team = Team(key='C',name='test')
        test_team.save()
        test_season = Season(slug='2016',name='test')
        test_season.save()
        test_gameweek = GameWeek(season = test_season,number=1,starts_at = timezone.now(), ends_at = timezone.now())
        test_gameweek.save()
        test_game = Game(gameweek=test_gameweek,outcome='C',home_team = test_team,home_team_score=300,away_team_score=300,away_team=test_team)
        test_game.save()
        test_player = Player(player_first_name='Test',player_last_name='Tester',player_nickname='Testes',player_team=test_team)
        test_player.save()
        test_gamestats = GameStats(game=test_game,player=test_player,goals=3,assists=3,saves=3,shots=3,points=300)
        test_gamestats.save()
        self.assertEqual(test_player.lifetime_points,test_gamestats.points)

import csv, datetime

from django.db.models import Q, Max
from .models import *

#defines how a header should look
def test_header(header,header_template):
    assert len(header)==len(header_template)
    for i in range(0,len(header)):
        assert header[i]==header_template[i]

def import_games(path):
    game_hdr=['Season','Week','Game','Home Team','Away Team','Home Team Score','Away Team Score']
    with open(path) as f:
        reader = csv.reader(f)
        #test and eat header
        header = next(reader)
        test_header(header,game_hdr)
        for row in reader:
            season, season_created = Season.objects.get_or_create(slug=row[0])
            
            #Get the previous week - we'll use the ends_at date to figure the next starts_at
            previous_week = GameWeek.objects.get(number=int(row[1])-1)
            #starts at - default value is 1 day after the latest end time
            sad = previous_week.ends_at + datetime.timedelta(days=1)
            #ends at - default value is 7 days after the start day
            ead = sad + datetime.timedelta(days=7)
            
            week, week_created = GameWeek.objects.get_or_create(number=int(row[1]),season=season,starts_at=sad,ends_at=ead)

            #team should already exist
            home_team, ht_created = Team.objects.get_or_create(key=row[3])
            assert not ht_created
            away_team, at_created = Team.objects.get_or_create(key=row[4])
            assert not at_created

            hts = row[5]
            ats = row[6]

            oc = ''
            if hts > ats:
                oc = home_team.key
            else:
                oc = away_team.key
            
            game_defaults = {'outcome':oc,'home_team_score':hts,'away_team_score':ats}
            game, game_created = Game.objects.get_or_create(gameweek=week,series_number=int(row[2]),home_team=home_team,away_team=away_team,defaults=game_defaults)
            assert game_created

def import_player_scores(path):
    player_hdr = ['Season','Week','Game','Player','Score','Goals','Assists','Saves','Shots']
    with open(path) as f:
        reader = csv.reader(f)
        #test and eat header
        header = next(reader)
        test_header(header,player_hdr)
        for row in reader:
            #season, week, player, and game must already exist
            season, season_created = Season.objects.get_or_create(slug=row[0])
            assert not season_created
            week, week_created = GameWeek.objects.get_or_create(number=int(row[1]),season=season)
            assert not week_created
            player = Player.objects.get(player_nickname=row[3])
            t = player.player_team.key
            #find which game we need to add the stats to
            game_result = Game.objects.get(Q(home_team__key=t)|Q(away_team__key=t),Q(series_number=row[2]),Q(gameweek__number=week.number))

            gs_defaults = {'goals':int(row[5]),'assists':int(row[6]),'saves':int(row[7]),'shots':int(row[8]),'points':int(row[4])}
            gamestats,gs_created = GameStats.objects.get_or_create(game=game_result,player=player,defaults=gs_defaults)
            assert gs_created

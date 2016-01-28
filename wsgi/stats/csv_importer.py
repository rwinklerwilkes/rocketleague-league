import csv, datetime

from django.db.models import Q, Max
from django.contrib.auth.models import User
from .models import *

#defines how a header should look
def test_header(header,header_template):
    assert len(header)==len(header_template)
    for i in range(0,len(header)):
        assert header[i]==header_template[i]

def parse_key(key):
    assert len(key) == 10
    #GameKey should be of the form SeasonWeekGameTeam1Team2
    out = {}
    out['season'] = key[:6]
    out['week'] = key[6:7]
    out['game'] = key[7:8]
    out['ht'] = key[8:9]
    out['at'] = key[9:]
    return out

#rewrite import processes to better handle files
def import_file(path):
    game_hdr=['GameKey','Season','Week','Game','Team','Result','Player','Score','Goals','Assists','Saves','Shots']
    players_modified = []
    
    with open(path) as f:
        reader = csv.reader(f)
        header = next(reader)
        test_header(header,game_hdr)
        for row in reader:
            k = parse_key(row[0])
            #k now has which season, week, game, and teams played for this particular row.
            
            #if any of these don't exist, we should create them
            #start with: season
            season, season_created = Season.objects.get_or_create(slug=k['season'])

            #next, week
            def_start_date = '2016-01-10'
            def_end_date = '2016-01-16'

            #if the prior week doesn't exist or hasn't been created yet, set current week up with default
            #we can always fix it later
            try:
                pw = GameWeek.objects.get(season=season,number=int(k['week'])-1)
                sad = pw.ends_at + datetime.timedelta(days=1)
                ead = sad + datetime.timedelta(days=6)
            except:
                sad = def_start_date
                ead = def_end_date
                
            week, week_created = GameWeek.objects.get_or_create(number=int(k['week']),season=season,starts_at=sad,ends_at=ead)

            #next, make sure that the teams exist
            #'team' in our key will give the initials of the two teams playing
            #the team column will give us the initials AND their name
            #only split the value twice - this allows for team names to have spaces
            team_in = row[4].split(maxsplit=2)
            team_key = team_in[1]
            team_name = team_in[0]+' ' + team_in[2]

            team_line, cr = Team.objects.get_or_create(key=team_key,defaults={'name':team_name})

            #this happens when the object already exists (was seen in an earlier line) but didn't have the name set
            if team_line.name is None:
                team_line.name = team_name
                team_line.save()

            if k['ht'] == team_key:
                ht = team_line
                at = k['at']
                ot = at
            else:
                ht = k['at']
                at = team_line
                ot = ht

            #create the other team using the row key
            team_two, ttcr = Team.objects.get_or_create(key=ot)
                
            if k['ht']==team_key:
                ht = team_line
                at = team_two
            else:
                ht = team_two
                at = team_line

            #then, make sure that the players exist
            #while we're at it, if the player was created, create a user to go along with it
            player_def = {'player_nickname':row[6].split()[0]}
            player,pcreated = Player.objects.get_or_create(player_first_name=row[6].split()[0],player_last_name=row[6].split()[1],player_team=team_line,defaults=player_def)
            if pcreated:
                #player was created
                #add a user, associate the two
                #username will be first name
                #email will be blank
                #password will be temp
                user = User.objects.create_user(username=row[6].split()[0],password='temp')
                player.user = user
                player.save()

            #then, create the games
            game, gamecreated = Game.objects.get_or_create(gameweek=week,series_number=int(row[3]),home_team=ht,away_team=at)
            if gamecreated:
                if k['ht'] == team_key:
                    game.home_team_score = int(row[5])
                else:
                    game.away_team_score = int(row[5])
                game.save()

            #lastly, add the stats
            gs, gscreated = GameStats.objects.get_or_create(game=game,player=player)
            #should match the data if it already exists
            if not gscreated:
                assert gs.points == int(row[7])
                assert gs.goals == int(row[8])
                assert gs.assists == int(row[9])
                assert gs.saves == int(row[10])
                assert gs.shots == int(row[11])
            else:
                players_modified.append(gs.player)
                gs.points = int(row[7])
                gs.goals = int(row[8])
                gs.assists = int(row[9])
                gs.saves = int(row[10])
                gs.shots = int(row[11])
                gs.save()

        #done with reading
                    
    #fix the game outcomes now
    for g in Game.objects.all():
        if g.home_team_score > g.away_team_score:
            g.outcome = g.home_team.key
        elif g.home_team_score < g.away_team_score:
            g.outcome = g.away_team.key
        else:
            g.outcome = 'T'
        g.save()

    for p in players_modified:
        p.update_stats()

def import_2():
    p = os.environ.get('OPENSHIFT_REPO_DIR')
    p = os.path.join(p,'data')
    p = os.path.join(p,'Season 1.csv')
    import_file(p)
        
##
##def import_games(path):
##    game_hdr=['Season','Week','Game','Home Team','Away Team','Home Team Score','Away Team Score']
##    with open(path) as f:
##        reader = csv.reader(f)
##        #test and eat header
##        header = next(reader)
##        test_header(header,game_hdr)
##        for row in reader:
##            season, season_created = Season.objects.get_or_create(slug=row[0])
##            
##            #Get the previous week - we'll use the ends_at date to figure the next starts_at
##            previous_week = GameWeek.objects.get(number=int(row[1])-1)
##            #starts at - default value is 1 day after the latest end time
##            sad = previous_week.ends_at + datetime.timedelta(days=1)
##            #ends at - default value is 6 days after the start day
##            ead = sad + datetime.timedelta(days=6)
##            
##            week, week_created = GameWeek.objects.get_or_create(number=int(row[1]),season=season,starts_at=sad,ends_at=ead)
##
##            #team should already exist
##            home_team, ht_created = Team.objects.get_or_create(key=row[3])
##            assert not ht_created
##            away_team, at_created = Team.objects.get_or_create(key=row[4])
##            assert not at_created
##
##            hts = row[5]
##            ats = row[6]
##
##            oc = ''
##            if hts > ats:
##                oc = home_team.key
##            else:
##                oc = away_team.key
##            
##            game_defaults = {'outcome':oc,'home_team_score':hts,'away_team_score':ats}
##            game, game_created = Game.objects.get_or_create(gameweek=week,series_number=int(row[2]),home_team=home_team,away_team=away_team,defaults=game_defaults)
##            assert game_created
##
##def import_player_scores(path):
##    player_hdr = ['Season','Week','Game','Player','Score','Goals','Assists','Saves','Shots']
##    with open(path) as f:
##        reader = csv.reader(f)
##        #test and eat header
##        header = next(reader)
##        test_header(header,player_hdr)
##        for row in reader:
##            #season, week, player, and game must already exist
##            season, season_created = Season.objects.get_or_create(slug=row[0])
##            assert not season_created
##            week, week_created = GameWeek.objects.get_or_create(number=int(row[1]),season=season)
##            assert not week_created
##            player = Player.objects.get(player_nickname=row[3])
##            t = player.player_team.key
##            #find which game we need to add the stats to
##            game_result = Game.objects.get(Q(home_team__key=t)|Q(away_team__key=t),Q(series_number=row[2]),Q(gameweek__number=week.number))
##
##            gs_defaults = {'goals':int(row[5]),'assists':int(row[6]),'saves':int(row[7]),'shots':int(row[8]),'points':int(row[4])}
##            gamestats,gs_created = GameStats.objects.get_or_create(game=game_result,player=player,defaults=gs_defaults)
##            assert gs_created

#! usr/bin/python

import urllib2
import json
from pprint import pprint
import ast
import os
import datetime
from collections import namedtuple
from collections import OrderedDict
import urllib
import urlparse

'''
    I need to output last 5 matches for a team for the team (tendency and result)
'''
class FootballAPIWrapper:
    def __init__(self):
        self.__premier_league_id = '1204'
        self.__base_url = 'http://football-api.com/api/?Action='

    @staticmethod
    def get_beginning_year(current_month, current_year):
        'checking in which year the season began'
        if current_month > 7:
            season_began_in_year = current_year
        else:
            season_began_in_year = current_year - 1
        return season_began_in_year

    def call_api(self, action=None, **kwargs):
        """ Call the Football API
        :param action: Football API action: competition, standings, today, fixtures, commentaries
        :param kwargs: e.g
        :return: output as a json object
        :raise (Exception('Error: Action was not passed')):
        """
        if action is None:
            raise(Exception('Error: Action not passed to call_api'))

        # use ordered dictionary, so API key is always in the beginning

        params = OrderedDict()
        output_data = dict()

        params['APIKey'] = self.api_key

        for kwarg in kwargs:
            params[kwarg] = kwargs[kwarg]

        url = self.__base_url \
               + action \
               + '&comp_id=' + self.__premier_league_id

        params = urllib.urlencode(params)
        print ("My url {}").format(url + '&%s' % params)

        try:
            my_json = urllib2.urlopen(url + '&%s' % params)
        except urllib2.URLError, e:
            print 'URL error: ' + str(e.reason)
        except Exception:
            print 'Other exception'
        else:
            output_data = json.load(my_json)

        return output_data

    def feed_teams_ids(self):
        'Create an team name -> id relationship'
        action = 'standings'
        data_standings = self.call_api(action)
        output_data = {}

        # feeding the dictionary
        output_data = {
            team["stand_team_name"] : team["stand_team_id"]
            for team in data_standings['teams']
        }

        return output_data

    def form_and_tendency(self, action):
        'I need to output last 5 matches for a team for the team (tendency and result)'
        action = 'fixtures'
        params = {'from_date': '01.08.' + str(self.date_tuple.beginning_year), 'to_date' :str(self.date_tuple.today)}

        data_matches = self.call_api(action, **params)

        for match in data_matches["matches"]:
            if match["match_status"] == "FT":
                if match["match_localteam_id"] == '9260' or match["match_visitorteam_id"] == '9260':
                    pass
                    #print match["match_formatted_date"], match["match_localteam_name"], match["match_visitorteam_name"], match["match_ft_score"]


    def feed_league_table(self):
        'cracking a standard league table (a dictionary ordered by position)'
        action = 'standings'
        data_standings = self.call_api(action)
        league_table = {}
        TeamInfo = namedtuple('TeamInfo', 'position team_name matches_played w d l goals_for goals_against gp points')

     #   for sortedKey in sorted(dictionary):
    #print dictionary[sortedKeY] # gives the values sorted by key

        for team in data_standings['teams']:
            league_table[team['stand_team_id']] = TeamInfo(team['stand_position'], team['stand_team_name'], team['stand_round'],
                           team['stand_overall_w'], team['stand_overall_d'], team['stand_overall_l'],
                           team['stand_overall_gs'], team['stand_overall_ga'], team['stand_gd'], team['stand_points'])

        #for sortedValue in sorted(league_table['position'].values()):
        #    print sortedValue # gives the values sorted by value

        return league_table

    @property
    def api_key(self):
        raise AttributeError('API is a non-readable attribute!')

    @api_key.setter
    def api_key(self, value):
        self.api_key = value

    @property
    def teams_ids(self):
        self.teams_ids = self.feed_teams_ids()
        return self.teams_ids

    @property
    def league_table(self):
        self.league_table = self.feed_league_table()
        return self.league_table

    @property
    def date_tuple(self):
        today = datetime.date.today()
        today_formatted = today.strftime("%d.%m.%Y")

        beginning_year = self.get_beginning_year(today.month, today.year)
        Dates = namedtuple("Dates", "today month beginning_year")
        return Dates(today_formatted, today.month, beginning_year)


'''
# cracking a standard league table
# position, win, draw, loss, points, last 10 games (tendency)

Example endpoints
api/?Action=competitions&APIKey=####
api/?Action=standings&comp_id=1204&APIKey=####
api/?Action=today&comp_id=1204&APIKey=####
api/?Action=fixtures&comp_id=1024&&match_date=[DATE_IN_d.m.Y_FORMAT]&APIKey=####
api/?Action=commentaries&APIKey=###&match_id=[MATCH_ID]

API2:
http://api2.football-api.com/api/?Action=player&APIKey=[YOUR_API_KEY]&player_id=193
http://api2.football-api.com/api/?Action=team&APIKey=[YOUR_API_KEY]&team_id=[team]
'''
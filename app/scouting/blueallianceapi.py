# Functions and defaults to work with "The Blue Alliance" api

import json
import requests as rq
from requests.exceptions import HTTPError

x_tba_key = 'w3eIaK7689U3oyAoe0smSosQ9DS5I9FXXyyl2yxlhMBBw1qk5MZwklQWIc3sAkAT'
accept = 'application/json'
parm = {'accept' : accept, 'X-TBA-Auth-Key' : x_tba_key}

matchTypes = {
    'qual' : '_qm',
    'quart1' : 'qf1m',
    'quart2' : 'qf2m',
    'quart3' : 'qf3m',
    'quart4' : 'qf4m',
    'sem1' : 'sf1m',
    'sem2' : 'sf2m',
    'final' : 'f1m'
}

def bytes_to_dict(binary : bytes):
    return json.loads(binary.decode('utf-8'))

def check_response(response : rq.Response):
    """
    Error check for HTTP errors when requesting TBA data
    """
    if (response.status_code is 200):
        return True
    return False

def request_match(year : int, event : str, matchNum : int, matchType : str = 'qual'):
    """
    Requests data on a specific match through "The Blue Alliance" API
    https://www.thebluealliance.com/apidocs/v3
    
    Parameters: 
    
    year (int) : the season of the match. Ex: Deep Space -> 2019, Infinite REcharge -> 2020

    event (str) : event code. Ex: North Bay Ontario -> 'onnob'. Look at "The Blue Alliance" for event codes

    matchNum (int) : match number, in terms of the match type.

    matchType (str) : match type. Ex: Qualifier -> 'qual', Quarter Final 2 -> 'quart2'.

    return (dict) : full data on the match requested or False if an error occured
    """
    url = 'https://www.thebluealliance.com/api/v3/match/'
    url += str(year) + event.lower() + matchTypes[matchType] + str(matchNum)
    response = rq.get(url, params=parm)
    if check_response(response):
        return bytes_to_dict(response.content)
    return False;

def get_robot_num(alliance : str, teamNum : int, matchObject : dict):
    """


    Parameters:
    alliance (str) : either 'red' or 'blue'

    teamNum (int) : team number

    matchObject (dict) : the match data dict

    return (str) : the corresponding robot in the match data
    """
    teamList = matchObject["alliances"][alliance.lower()]["team_keys"]
    num = teamList.index('frc' + str(teamNum)) + 1
    return 'Robot' + str(num)

def get_alliance_score(alliance : str, matchObject : dict):
    return matchObject["alliances"][alliance.lower()]["score"]

if __name__ == "__main__":
    match = request_match(2019, 'ONNOB', 3)
    robot = get_robot_num('blue', 4783, match)
    score = get_alliance_score('blue', match)
    print(robot)
    print(score)
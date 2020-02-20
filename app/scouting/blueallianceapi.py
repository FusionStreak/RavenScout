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

def check_response(response):
    pass

def request_match(year : int, event : str, matchType : str, matchNum : int):
    """
    Requests data on a specific match through "The Blue Alliance" API
    https://www.thebluealliance.com/apidocs/v3
    
    Parameters:
    year (int) : the season of the match. Ex: Deep Space -> 2019, Infinite REcharge -> 2020

    event (str) : event code. Ex: North Bay Ontario -> 'onnob'. Look at "The Blue Alliance" for event codes

    matchType (str) : match type. Ex: Qualifier -> 'qual', Quarter Final 2 -> 'quart2'.

    matchNum (int) : match number, in terms of the match type.
    """
    url = 'https://www.thebluealliance.com/api/v3/match/'
    url += str(year) + event.lower() + matchTypes[matchType] + str(matchNum)
    response = rq.get(url, params=parm)
    return bytes_to_dict(response.content)


if __name__ == "__main__":
    print(request_match(2018, 'ONNON', 'qual', 3))
# Functions for deailing with 2020 Infinite Recharge scouting data

import pandas as pd
import numpy as np
import blueallianceapi as tba
from collections import namedtuple

pointValues = {
    'autoLine' : 5, # Crossed Auto Line
    'autoBot' : 2, # Balls scored in bottom port in Autonomous
    'autoOut' : 4, # Balls scored in outer port in Autonomous
    'autoIn' : 6, # Balls scored in inner port in Autonomous
    'teleBot' : 1, # Balls scored in bottom port in Teleop
    'teleOut' : 2, # Balls scored in outer port in Teleop
    'teleIn' : 3,  # Balls scored in inner port in Teleop
    'ctrlRot' : 10, # Completed Control Panel rotation
    'ctrlPos' : 20, # Completed Control Panel positioning
    'hang' : 25, # Climbed Shield Generator
    'park' : 5, # Parked inside Sheild Generator
    'level' : 15 # If the Shield Generator was level
}

def validate_endgame(dataFrame : pd.DataFrame, scoutRecord : tuple, scoreBreakdown : dict, robotNum : str):
    """
    Validates the records endgame data

    Paramaters:

    dataFrame (pd.DataFrame) :

    scoutRecord (tuple) :

    scoreBreakdown (dict) :

    robotNum (str) :
    """
    tba_endgame = scoreBreakdown['endgame' + robotNum]
    if (tba_endgame is 'Park'):
        if (scoutRecord.park is False):
            dataFrame.at[scoutRecord.Index, 'park'] = True
    if (tba_endgame is 'Hang'):
        if (scoutRecord.climb is False):
            dataFrame.at[scoutRecord.Index, 'climb'] = True
    if (tba_endgame is 'None'):
        if (scoutRecord.park is True):
            dataFrame.at[scoutRecord.Index, 'park'] = False
        if (scoutRecord.climb is True):
            dataFrame.at[scoutRecord.Index, 'climb'] = False

def validate_auto(dataFrame : pd.DataFrame, scoutRecord : tuple, scoreBreakdown : dict, robotNum : str):
    """
    Validates the records auto data

    Paramaters:

    dataFrame (pd.DataFrame) :

    scoutRecord (tuple) :

    scoreBreakdown (dict) :

    robotNum (str) :
    """
    if (scoreBreakdown['initLine'  + robotNum] is 'Exited'):
        if (scoutRecord.left_line is False):
            dataFrame.at[scoutRecord.Index, 'left_line'] = True
    if (scoreBreakdown['initLine'  + robotNum] is 'None'):
        if (scoutRecord.left_line is True):
            dataFrame.at[scoutRecord.Index, 'left_line'] = False

def validate_record(dataFrame : pd.DataFrame, scoutRecord : tuple, matchObject : dict):
    """
    Validates a record from the data frame 
    """
    refNum = tba.get_robot_num(scoutRecord.alliance, scoutRecord.team_num, matchObject)
    allianceScoreBreakdown = matchObject['score_breakdown'][scoutRecord.alliance.lower()]
    validate_endgame(dataFrame, scoutRecord, allianceScoreBreakdown, refNum)
    pass

def validate_file(dataFrame : pd.DataFrame, event : str):
    for row in dataFrame.itertuples(name='Record'):
        match = tba.request_match(2020, event, row.match)
        if (match is False):
            continue
        validate_record(row, match)
    pass

def calc_contributed(scoutRecord : tuple):
    """
    Calculates the score contributed by the specific team

    Paramaters:

    scoutRecord (tuple) : the record from the data frame containign scout data
    """
    score = 0
    if (scoutRecord.left_line is 'TRUE'):
        score += pointValues['autoLine']
    score += scoutRecord.auto_in * pointValues['autoIn']
    score += scoutRecord.auto_out * pointValues['autoOut']
    score += scoutRecord.auto_bot * pointValues['autoBot']
    score += scoutRecord.tele_in * pointValues['teleIn']
    score += scoutRecord.tele_out * pointValues['teleOut']
    score += scoutRecord.tele_bot * pointValues['teleBot']
    if (scoutRecord.ctrl_rot):
        score += pointValues['ctrlRot']
    if (scoutRecord.ctrl_pos):
        score += pointValues['ctrlPos']
    if (scoutRecord.park):
        score += pointValues['park']
    if (scoutRecord.climb):
        score += pointValues['hang']
    return score

def update_season_profile(team : int, scoutRecord : tuple):
    pass

def generate_data(dataFrame : pd.DataFrame, event : str):
    """
    Goes through each record in the dataFrame. Preforms basic 
    stats calculations and validation.

    Paramaters:

    dataFrame (DataFrame) : the data frame to be parsed

    event (str) : event code
    """
    dataFrame['alliance_score'] = pd.Series(index=dataFrame.index)
    dataFrame['team_score'] = pd.Series(index=dataFrame.index)
    dataFrame['contributed'] = pd.Series(index=dataFrame.index)
    for row in dataFrame.itertuples(name='Record'):
        match = tba.request_match(2020, event, row.match)
        if (match is False):
            continue
        allScore = tba.get_alliance_score(row.match, match)
        teamScore = calc_contributed(row)
        dataFrame.at[row.Index, 'alliance_score'] = allScore
        dataFrame.at[row.Index, 'team_score'] = teamScore
        dataFrame.at[row.Index, 'contributed'] = (teamScore / allScore) * 100
    dataFrame.to_csv('generated.csv')

if __name__ == "__main__":
    pass

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

def validate_endgame(dataFrame : pd.DataFrame, scoutRecord : namedtuple, scoreBreakdown : dict, robotNum : str):
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

def validate_auto(dataFrame : pd.DataFrame, scoutRecord : namedtuple, scoreBreakdown : dict, robotNum : str):
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

def validate_record(dataFrame : pd.DataFrame, scoutRecord : namedtuple, matchObject : dict):
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
        validate_record(dataFrame, row, match)
    return dataFrame

def calc_contributed(scoutRecord :namedtuple):
    """
    Calculates the score contributed by the specific team

    Paramaters:

    scoutRecord (tuple) : the record from the data frame containign scout data
    """
    score = 0
    if (scoutRecord.left_line):
        score += pointValues['autoLine']
    score += scoutRecord.auto_out * pointValues['autoOut']
    score += scoutRecord.auto_bot * pointValues['autoBot']
    score += scoutRecord.tele_out * pointValues['teleOut']
    score += scoutRecord.tele_bot * pointValues['teleBot']
    if (scoutRecord.ctrl_rot):
        score += pointValues['ctrlRot']
    if (scoutRecord.ctrl_pos):
        score += pointValues['ctrlPos']
    # if (scoutRecord.park):
    #    score += pointValues['park']
    if (scoutRecord.climb):
        score += pointValues['hang']
    return score

def calc_accuracy(scoutRecord : namedtuple):
    totalCellsIn = scoutRecord.auto_bot + scoutRecord.auto_out
    totalCellsIn += scoutRecord.tele_bot + scoutRecord.tele_out
    if totalCellsIn is 0:
        return 0
    return (scoutRecord.cells_dropped / totalCellsIn) * 100

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
    dataFrame['contributed(%)'] = pd.Series(index=dataFrame.index)
    dataFrame['cell_accuracy'] = pd.Series(index=dataFrame.index)
    dataFrame['foul_points'] = pd.Series(index=dataFrame.index)
    dataFrame['foul_contribution'] = pd.Series(index=dataFrame.index)
    for row in dataFrame.itertuples(name='Record'):
        match = tba.request_match(2020, event, row.match)
        if (match is False):
            continue
        allScore = tba.get_alliance_score(row.alliance, match)
        teamScore = calc_contributed(row)
        foulPoints = tba.get_alliance_foul_points(row.alliance, match)
        dataFrame.at[row.Index, 'alliance_score'] = allScore
        dataFrame.at[row.Index, 'team_score'] = teamScore
        if allScore > 0:
            dataFrame.at[row.Index, 'contributed(%)'] = (teamScore / allScore) * 100
        else:
            dataFrame.at[row.Index, 'contributed(%)'] =  0
        dataFrame.at['cell_accuracy'] = calc_accuracy(row)
        dataFrame.at[row.Index, 'foul_points'] = foulPoints
        dataFrame.at[row.Index, 'foul_contribution'] = foulPoints / 3
    dataFrame.to_csv('app/scouting/Test/generated.csv',index=False)

newNames = {
        'Team Number' : 'team_num',
        'Match Number' : 'match',
        'Crossed line' : 'left_line_old',
        'Rotation CP?' : 'ctrl_rot_old',
        'Position CP?' : 'ctrl_pos_old',
        'Can it climb?' : 'climb_old',
        'Low Auto' : 'auto_bot',
        'High Auto' : 'auto_out',
        'Low Tele' : 'tele_bot',
        'High Tele' : 'tele_out',
        'Field Position' : 'alliance',
        'Cells dropped' : 'cells_dropped'
    }

def fix_scout_entries(dataFrame : pd.DataFrame):
    dataFrame = dataFrame.drop(['Scout', 'Broken?', 'Did robot tip?', 'Travel through trench', 'Power Cell Capacity'], axis=1)
    dataFrame = dataFrame.drop(['Can pickup PC from floor?', 'Penalty', 'Park Time', 'Climb Time', 'Rotation Time'], axis=1)
    dataFrame = dataFrame.drop(['Position Time', 'Hanging Mobility', 'Balance', 'Assist', 'Missed Auto'] , axis=1)
    dataFrame = dataFrame.drop(['Missed Tele', 'Blocked Tele', 'Ground Pickup', 'Loading Pickup'], axis=1)
    dataFrame = dataFrame.rename(columns=newNames)
    dataFrame['left_line'] = pd.Series(index=dataFrame.index, dtype=bool)
    dataFrame['ctrl_rot'] = pd.Series(index=dataFrame.index, dtype=bool)
    dataFrame['ctrl_pos'] = pd.Series(index=dataFrame.index, dtype=bool)
    dataFrame['climb'] = pd.Series(index=dataFrame.index, dtype=bool)
    for row in dataFrame.itertuples(name='Record'):
        dataFrame.at[row.Index, 'alliance'] = row.alliance[:-2]
        # Fix left_line
        if ('Yes' in row.left_line_old):
            dataFrame.at[row.Index, 'left_line'] = True
        else:
            dataFrame.at[row.Index, 'left_line'] = False
        # Fix climb
        if ('Yes' in row.climb_old):
            dataFrame.at[row.Index, 'climb'] = True
        else:
            dataFrame.at[row.Index, 'climb'] = False
        # Fix ctrl_pos
        if ('Yes' in row.ctrl_pos_old):
            dataFrame.at[row.Index, 'ctrl_pos'] = True
        else:
            dataFrame.at[row.Index, 'ctrl_pos'] = False
        #Fix ctrl_rot
        if ('Yes' in row.ctrl_rot_old):
            dataFrame.at[row.Index, 'ctrl_rot'] = True
        else:
            dataFrame.at[row.Index, 'ctrl_rot'] = False
    dataFrame = dataFrame.drop(['left_line_old', 'climb_old', 'ctrl_pos_old', 'ctrl_rot_old'], axis=1)
    return dataFrame


if __name__ == "__main__":
    mainFrame = pd.read_csv('app/scouting/Test/Scout-entry.csv')
    mainFrame = fix_scout_entries(mainFrame)
    print(mainFrame)
    generate_data(mainFrame, 'ONOSH')
    
    
# Functions for deailing with 2020 Infinite Recharge scouting data

import pandas as pd
import numpy as np
import blueallianceapi as tba

pointValues = {
    'autoLine' : 5,
    'autoBot' : 2,
    'autoOut' : 4,
    'autoIn' : 6,
    'teleBot' : 1,
    'teleOut' : 2,
    'teleIn' : 3,
    'ctrlRot' : 10,
    'ctrlPos' : 20,
    'hang' : 25,
    'park' : 5,
    'level' : 15
}

def calc_contributed(scoutRecord : tuple):
    pass

def generate_data(dataFrame : pd.DataFrame, event : str):
    dataFrame['matchScore'] = pd.Series(index=dataFrame.index)
    dataFrame['teamScore'] = pd.Series(index=dataFrame.index)
    dataFrame['contributedScore'] = pd.Series(index=dataFrame.index)
    for row in dataFrame.intertuples():
        match= tba.request_match(2020, event, row[1])
        if (match is False):
            continue
        dataFrame.at[row[2], 'matchScore'] = tba.get_alliance_score(row[2], match)

def calculate_team_score():
    pass
# Functions for deailing with 2020 Infinite Recharge scouting data

import pandas as pd
import numpy as np
import blueallianceapi as tba

def generate_data(dataFrame : pd.DataFrame, event : str):
    dataFrame['matchScore'] = pd.Series(index=dataFrame.index)
    dataFrame['teamScore'] = pd.Series(index=dataFrame.index)
    dataFrame['contrinutedScore'] = pd.Series(index=dataFrame.index)
    for row in dataFrame.intertuples():
        match= tba.request_match(2020, event, row[1])
        if (match is False):
            continue
        dataFrame.at[row[2], 'matchScore'] = tba.get_alliance_score(row[2], match)

def calculate_team_score():
    pass
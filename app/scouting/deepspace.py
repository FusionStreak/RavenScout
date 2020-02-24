# Functions for deailing with 2019 Deep Space scouting data

import pandas as pd
import numpy as np
import blueallianceapi as tba

def generate_data(dataFrame : pd.DataFrame, event : str):
    dataFrame['matchScore'] = pd.Series(index=dataFrame.index)
    dataFrame['teamScore'] = pd.Series(index=dataFrame.index)
    dataFrame['contributedScore'] = pd.Series(index=dataFrame.index)
    for row in dataFrame.itertuples(index=False):
        match = tba.request_match(2019, event, row[0])
        if (match is False):
            continue
        robot = tba.get_robot_num(row[1], row[3], match)
        

    pass

if __name__ == "__main__":
    pass
# Main file to load and parse data from uploaded scouting files

import pandas as pd
import numpy as np
import app.scouting.deepspace as ds
import app.scouting.infiniterecharge as ir

def parseData(csvFile, year, event):
    currentDF = pd.read_csv(csvFile)
    

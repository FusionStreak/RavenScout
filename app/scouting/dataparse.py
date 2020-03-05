# Main file to load and parse data from uploaded scouting files

import pandas as pd
import numpy as np
import infiniterecharge as ir

season = {
    2020 : ir.generate_data
}

def parse_data(csvFile : str, year : int, event : str):
    currentDF = pd.read_csv(csvFile)
    season.get(year)(currentDF, event)

if __name__ == "__main__":
    pass
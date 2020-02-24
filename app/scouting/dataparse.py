# Main file to load and parse data from uploaded scouting files

import pandas as pd
import numpy as np
import deepspace as ds
import infiniterecharge as ir

season = {
    2019 : ds.generate_data,
    2020 : ir.generate_data
}

def parse_data(csvFile : str, year : int, event : str):
    currentDF = pd.read_csv(csvFile)
    season.get(year)(currentDF, event)

if __name__ == "__main__":
    pass
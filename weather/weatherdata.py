import pandas as import pd
import os

global filelist = []
global globalDf = pd.DataFrame()

for file in os.listdir(".\Datasets"):
    if file.endswith(".csv")
        filelist.append(file)

def create_globalDf():
    for i in filelist:
        
    


import pandas as pd

# Get data - reading the CSV file
import mpu.pd
df = mpu.pd.example_df()

# Convert
lists = [[row[col] for col in df.columns] for row in df.to_dict('records')]


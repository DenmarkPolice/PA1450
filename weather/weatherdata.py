import pandas as pd
import os

def getDataFrames():
    df_list = []

    for file in os.listdir(os.getcwd()):
        if file.endswith(".csv"):
            df_list.append(pd.read_csv(file))
    
    for df in df_list:
        df.drop(['Kvalitet','Tidsutsnitt'])

    return df_list

def merge_dataFrame_list(dataFrame_list):
    df_collection = pd.DataFrame()
    for df in dataFrame_list:
        if (df_collection.empty() == True):
            df_collection.append(df)
        else:
            pd.merge(df_collection, df)


def get_Parameters():
    #return some list
    return 0

for data in getDataFrames():
    print (data)
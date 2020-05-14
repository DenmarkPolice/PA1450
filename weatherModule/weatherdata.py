import pandas as pd 
import os
import glob

class weatherdata:

    def __init__(self):
        self.data_frame = pd.DataFrame()

    def import_to_dataset(self, filePath):
        all_files = glob.glob(filePath + "/*.csv")

        df_list = []

        for filename in all_files:
            df_list.append(pd.read_csv(filename, sep = ";"))
            

        for df in df_list:
            print(df.info())
            print (df.head())
            df.drop(columns = ["Tidsutsnitt", "Kvalitet"])
            

        self.data_frame = df_list

    def get_dataset(self):
        return self.data_frame

data = weatherdata()


filePath = os.getcwd() + "\\rawData"
print(filePath)
data.import_to_dataset(filePath)


print(data.get_dataset())
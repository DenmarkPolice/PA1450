import pandas as pd 
import os
import glob

class weatherdata:

    def __init__(self, filePath):
        self.data_frame_list = []
        self.filePath = filePath

    def import_to_data(self):
        all_files = glob.glob(self.filePath + "/*.csv")

        df_list = []

        for filename in all_files:
            df_list.append(pd.read_csv(filename, sep = ","))            

        self.data_frame = df_list

    def get_data_frames(self):
        return self.data_frame
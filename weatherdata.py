import pandas as pd
import os
import glob

class weatherdata:

    def __init__(self, filePath):
        self.data_frame_list = []
        self.filePath = filePath

    def import_data(self):
        all_files = glob.glob(self.filePath + "/*.csv")

        df_list = []

        for filename in all_files:
            df_list.append(pd.read_csv(filename, sep = ","))            

        self.data_frame_list = df_list

    def get_ranged_df(self, start_date, end_date):
        if start_date <= end_date:
            ranged_df_list = []

            for df in self.data_frame_list:
                mask = (df['Datum'] > start_date) & (df['Datum'] <= end_date)
                ranged_df_list.append(df.loc[mask])
            
            return ranged_df_list
        else:
            return "start_date must be smaller than end_date"
    
    def makeExcel(self):

        # Calculate sunshine % for each day
        index = 0
        reportData = []
        column_day = 0
        df = self.data_frame_list[-1]

        for a, row in df.iterrows():
            column_day += int(row["Solskenstid"])
            index += 1
            if index % 24 == 0:
               reportData.append(column_day / (3600 * 24))
               column_day = 0
               index = 0
        
        del df['Solskenstid']
        del df['Tid (UTC)']

        export_df = df.drop_duplicates()

        export_df["Sunshine %"] = ""

        index = 0
        for i, row in export_df.iterrows():                
            try:
                row["Sunshine %"] = reportData[index]
                index += 1
                
            except IndexError:
                break    

        export_df.to_excel("report.xlsx")
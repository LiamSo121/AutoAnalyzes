import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from helpers.Assistant import Assistant

assist = Assistant()

class Visual:
    def half_hour_plot(self):
        half_hour_data = pd.read_excel('continuesLiam.xlsx',sheet_name='Hit By 30 Minutes')
        half_hour_data = half_hour_data.transpose()
        half_hour_data.columns = half_hour_data.iloc[0]
        times = list(half_hour_data.index)
        del times[0]
        values = list(half_hour_data['Hourly Avg'])
        del values[0]
        title = "Hit percentage by half hour"
        assist.seaborn_time_hit_line_plots(times,values,title)


    def hour_plot(self):
        hour_data = pd.read_excel('continuesLiam.xlsx',sheet_name='Hit By 1 Hour')
        hour_data = hour_data.transpose()
        hour_data.columns = hour_data.iloc[0]
        times = list(hour_data.index)
        del times[0]
        values = list(hour_data['Hourly Avg'])
        del values[0]
        title = "Hit percentage by hour"
        assist.seaborn_time_hit_line_plots(times,values,title)
        

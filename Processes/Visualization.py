from calendar import month_name
from turtle import color
from click import style
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from helpers.Assistant import Assistant
import numpy as np

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
        assist.seaborn_line_plots(times,values,title)

    def hour_plot(self):
        hour_data = pd.read_excel('continuesLiam.xlsx',sheet_name='Hit By 1 Hour')
        hour_data = hour_data.transpose()
        hour_data.columns = hour_data.iloc[0]
        times = list(hour_data.index)
        del times[0]
        values = list(hour_data['Hourly Avg'])
        del values[0]
        title = "Hit percentage by hour"
        assist.seaborn_line_plots(times,values,title)

    def sum_of_positions_by_time(self):
        profitData = pd.read_excel("continuesLiam.xlsx",sheet_name='Profits By Time')
        lossesData = pd.read_excel("continuesLiam.xlsx",sheet_name='Loses By Time')
        profitData = assist.fix_type_df(profitData)
        lossesData = assist.fix_type_df(lossesData)
        data = assist.fix_type_before_plot(profitData,lossesData)
        sns.set(style='white',rc = {'figure.figsize':(15,8)})
        ax = data.plot(kind='bar',stacked=True,width = 0.7,color=['steelblue', 'red'])
        for bar in ax.patches:
            height = bar.get_height()
            width = bar.get_width()
            x = bar.get_x()
            y = bar.get_y()
            label_text = height 
            label_x = (x + width / 2) 
            label_y = (y + height / 2) 
            ax.text(label_x, label_y, int(label_text), ha='center',    
                    va='center')
        plt.title('Number Of Positions By Time')
        plt.legend(loc='upper center')
        plt.xlabel('Time')
        plt.ylabel('Number Of Positions')
        plt.savefig(f'Graphs\\Number Of Positions By Time.png',dpi=300)
        plt.show()
     
    def hit_percentage_by_month_plot(self):
        data = pd.read_excel("continuesLiam.xlsx",sheet_name="Summary")
        month_names = ['January','February','March','April','May','June','July',
                    'August','September','October','November','December']
        hit_percentages = list(data['Hit Percentage'])
        hit_percentages.pop()
        title = "Hit Percentage By Month"
        assist.seaborn_line_plots(month_names,hit_percentages,title)


    def sum_of_positions_by_type(self):
        data = pd.read_excel("continuesLiam.xlsx",sheet_name= 'Type Distribution')
        data.loc[1,'type'] = 'HUMMER'
        data.loc[3,'type'] = 'OKAR/B'
        data.loc[5,'type'] = 'OKAR/S'
        data.loc[7,'type'] = 'SHOOTING-STAR'
        assist.plot_type(data)

        




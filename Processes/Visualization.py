from cProfile import label
from calendar import month_name
from turtle import color
from click import style
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from helpers.Assistant import Assistant
from os import walk
assist = Assistant()

class Visual:
    def half_hour_plot(self,output_file_name):
        half_hour_data = pd.read_excel(f'Outputs\\{output_file_name}.xlsx',sheet_name='Hit By 30 Minutes')
        half_hour_data = half_hour_data.transpose()
        half_hour_data.columns = half_hour_data.iloc[0]
        times = list(half_hour_data.index)[1:-1]
        values = list(half_hour_data['Hourly Avg'])[1:-1]
        title = "Hit percentage by half hour"
        xLable = "Time"
        yLable = "Hit percentage"
        assist.seaborn_line_plots(times,values,title,xLable,yLable)

    def hour_plot(self,output_file_name):
        hour_data = pd.read_excel(f'Outputs\\{output_file_name}.xlsx',sheet_name='Hit By 1 Hour')
        hour_data = hour_data.transpose()
        hour_data.columns = hour_data.iloc[0]
        times = list(hour_data.index)
        del times[0]
        values = list(hour_data['Hourly Avg'])
        del values[0]
        title = "Hit percentage by hour"
        xLable = "Time"
        yLable = "Hit percentage"
        assist.seaborn_line_plots(times,values,title,xLable,yLable)

    def sum_of_positions_by_time(self,output_file_name):
        profitData = pd.read_excel(f'Outputs\\{output_file_name}.xlsx',sheet_name='Profits By Time')
        lossesData = pd.read_excel(f'Outputs\\{output_file_name}.xlsx',sheet_name='Loses By Time')
        profitData = assist.fix_type_df(profitData)
        lossesData = assist.fix_type_df(lossesData)
        data = assist.fix_type_before_plot(profitData,lossesData)
        sns.set_theme(style='darkgrid',rc = {'figure.figsize':(15,8)})
        ax = data.plot(kind='bar',stacked=True,width = 0.7)
        sns.set_palette('pastel')
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
     
    def hit_percentage_by_month_plot(self,output_file_name):
        data = pd.read_excel(f'Outputs\\{output_file_name}.xlsx',sheet_name="Summary")
        month_names = ['January','February','March','April','May','June','July',
                    'August','September','October','November','December']
        hit_percentages = list(data['Hit Percentage'])
        hit_percentages.pop()
        title = "Hit Percentage By Month"
        xLable = "Month"
        yLable = "Hit Percentage"
        assist.seaborn_line_plots(month_names,hit_percentages,title,xLable,yLable)
        yields = list(data['Yield Percantage'])
        yields.pop()
        title = "Yield Percentage By Month"
        yLable = "Yield Percentage"
        assist.seaborn_line_plots(month_names,yields,title,xLable,yLable)

    def sum_of_positions_by_type(self,output_file_name):
        data = pd.read_excel(f'Outputs\\{output_file_name}.xlsx',sheet_name= 'Type Distribution')
        data.loc[1,'type'] = 'HUMMER'
        data.loc[3,'type'] = 'OKAR/B'
        data.loc[5,'type'] = 'OKAR/S'
        data.loc[7,'type'] = 'SHOOTING-STAR'
        assist.plot_type(data)





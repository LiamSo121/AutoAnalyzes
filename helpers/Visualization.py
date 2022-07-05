import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


class Visual:
    def half_hour_plot(self):
        half_hour_data = pd.read_excel('continuesLiam.xlsx',sheet_name='Hit By 30 Minutes')
        half_hour_data = half_hour_data.transpose()
        half_hour_data.columns = half_hour_data.iloc[0]
        times = list(half_hour_data.index)
        del times[0]
        values = list(half_hour_data['Hourly Avg'])
        del values[0]
        sns.set(rc = {'figure.figsize':(15,8)})
        sns.lineplot(x= times,y=values,color='red',marker='o',mec='k',markersize = 8)
        plt.title('Hit percentage by half hour')
        plt.xlabel('Time')
        plt.ylabel('Hit Percentage')
        plt.show()


    def hour_plot(self):
        hour_data = pd.read_excel('continuesLiam.xlsx',sheet_name='Hit By 30 Minutes')
        

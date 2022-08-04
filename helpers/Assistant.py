import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import seaborn as sns
import matplotlib.pyplot as plt

class Assistant:
    def calc_avg(self,df):
        df['Hourly Avg'] = round(df.mean(axis=1),2)
        return df

    def fix_hourly_index(self,df):
        times = []
        startTime = datetime.strptime('16:00:00', '%H:%M:%S')
        for i in range(len(df)):
            times.append(startTime)
            startTime += timedelta(minutes=60)
        df['interval'] = times
        for time in range(len(df['interval'])):
            df.loc[time,'interval'] = df.loc[time,'interval'].time()
        df = df.set_index('interval')
        return df   
    

    def fix_half_hour_index(self,df):
        times = []
        startTime = datetime.strptime('16:30:00', '%H:%M:%S')
        for i in range(len(df)):
            times.append(startTime)
            startTime += timedelta(minutes=30)
        df['interval'] = times
        for time in range(len(df['interval'])):
            df.loc[time,'interval'] = df.loc[time,'interval'].time()
        df = df.set_index('interval')
        return df 

    def seaborn_line_plots(self,x_values,y_values,title,xlables,ylables):
        sns.set(rc = {'figure.figsize':(15,8)})
        sns.lineplot(x= x_values,y= y_values,color='red',marker='o',mec='k',markersize = 8)
        plt.title(title)
        plt.xlabel(xlables)
        plt.ylabel(ylables)
        plt.savefig(f'Graphs\\{title}.png',dpi=300)
        plt.show()
        


    def fix_type_df(self,data: pd.DataFrame):
        data['30Min Split'] = pd.to_datetime(data['30Min Split'])
        data['Time'] = [d.time() for d in data['30Min Split']]
        data.drop(columns='30Min Split',inplace=True)
        data = data.set_index('Time')
        return data

    def fix_type_before_plot(self,profitData: pd.DataFrame,lossesData: pd.DataFrame):
        profits = np.array(profitData['pl'])
        loses = np.array(lossesData['pl'])
        times = list(profitData.index)
        data = pd.DataFrame(data=[profits,loses],columns= times)
        data.iloc[0,2] = data.iloc[0,2] + data.iloc[0,0]
        data.iloc[1,2] = data.iloc[1,2] + data.iloc[1,0]
        data.iloc[0,3] = data.iloc[0,3] + data.iloc[0,1]
        data.iloc[1,3] = data.iloc[1,3] + data.iloc[1,1]
        data = data.iloc[: , 2:]
        data = data.transpose()
        data.columns = ['Profits','Loses']
        return data

    def plot_type(self,data: pd.DataFrame):
        sns.set(style='white',rc = {'figure.figsize':(15,8)})
        ax = sns.barplot(x= 'type',y='pl.1',hue='pl',data=data,palette='pastel')
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
        plt.title('Positions By Type')
        plt.ylabel('Amount')
        plt.xlabel('Type')
        plt.savefig(f'Graphs\\Positions By Type.png',dpi=300)
        plt.show()


    def calculate_risk(self,fund,risk):
        daily_fund_risk = fund * risk
        return round(daily_fund_risk,2)

    def calculate_quantity(self,position_attributes: list):
        if position_attributes[1] == 'BUY':
            return round(position_attributes[0] / (position_attributes[2] - position_attributes[4]))
        else:
            return round(position_attributes[0] / (position_attributes[4] - position_attributes[2]))

    def calculate_commision(self,quantity):
        if quantity > 250:
            return ((quantity - 250) * 0.01) + 3
        else:
            return 3

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import seaborn as sns
import matplotlib.pyplot as plt

class Assistant:
    def calc_avg(self,df):
        df['Hourly Avg'] = round(df.mean(axis=1),2)
        return df

    def remove_problem_dates(self, summary_by_month: pd.DataFrame):
        summary_by_month['date'] = pd.to_datetime(summary_by_month['date'])
        problemDates = ['2021-03-15','2021-03-16','2021-03-17','2021-03-19','2021-03-22','2021-03-23','2021-03-24','2021-03-25','2021-11-01','2021-11-02','2021-11-03','2021-11-04','2021-11-05']
        problemDates = pd.to_datetime(problemDates)
        for date in problemDates:
            summary_by_month = summary_by_month[summary_by_month['date'] != date]
        
        return summary_by_month

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

    def seaborn_time_hit_line_plots(self,times,values,title):
        sns.set(rc = {'figure.figsize':(15,8)})
        plot = sns.lineplot(x= times,y=values,color='red',marker='o',mec='k',markersize = 8)
        plt.title(title)
        plt.xlabel('Time')
        plt.ylabel('Hit Percentage')
        plt.show()
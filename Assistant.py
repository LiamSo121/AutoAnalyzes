import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class Assistant:
    def calc_avg(self,df):
        df.loc['Avg'] = np.nan
        for col in df.columns:
            df.loc['Avg',col] = round(df[col].mean(),2)
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


    def export_to_excel(self,to_excel_list: pd.DataFrame):
        sheet_names_list = ['Data','Summary','Type Distribution','Profits By Time','Loses By Time','Splitted Month Summary','Hit By 30 Minutes','Hit By 1 Hour']
        writer = pd.ExcelWriter('continuesLiam.xlsx', engine='xlsxwriter')
        i = 0
        for excel_sheet in to_excel_list:
            excel_sheet.to_excel(writer,sheet_name = sheet_names_list[i])
            i += 1
        writer.save()


    # def export_to_excel(self,summary,yearlySum,groupByType,profitsBy30Min,losesBy30Min,by_period_df,hit_by_30_minutes,hourly_df):
    #     # Output xlsx file name
    #     writer = pd.ExcelWriter('continuesLiam.xlsx', engine='xlsxwriter')
    #     summary.to_excel(writer,sheet_name="Data")
    #     yearlySum.to_excel(writer,sheet_name="Summary")
    #     groupByType.to_excel(writer,sheet_name="Type Distribution")
    #     profitsBy30Min.to_excel(writer,sheet_name= "Profits By Time")
    #     losesBy30Min.to_excel(writer,sheet_name= "Loses By Time")
    #     by_period_df.to_excel(writer,sheet_name= 'Splitted Month Summary')
    #     hit_by_30_minutes.to_excel(writer, sheet_name = 'Hit By 30 Minutes')
    #     hourly_df.to_excel(writer,sheet_name = 'Hit By 1 Hour')
    #     writer.save()
        

# change function to fit list of dataframes to export
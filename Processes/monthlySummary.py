from email.errors import StartBoundaryNotFoundDefect
import pandas as pd
import numpy as np
import math
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from Processes.GroupBy import GroupBy
from helpers.Assistant import Assistant

assist = Assistant()

class monthlySummary:
    def create_df(self) -> pd.DataFrame:
        cols = ['Month','Monthly Positions','Profits','Losses','Hit Percentage','Yield Percantage','Gross','Commision','Change','Neto']
        monthlySum = pd.DataFrame(columns= cols).set_index('Month') 
        monthlySum.fillna('-',inplace=True)
        return monthlySum


    def calc_monthly(self,summary: pd.DataFrame,annual_summary: pd.DataFrame,fund) -> pd.DataFrame:
        summary['Month'] = pd.DatetimeIndex(summary['date']).month
        print(list(summary['Month']))
        months = summary['Month'].unique()
        for month in months:
            monthlyData = summary[summary['Month'] == month]
            annual_summary.loc[month,'Profits'] = len(monthlyData[monthlyData['pl'] == 'P'])
            annual_summary.loc[month,'Losses'] = len(monthlyData[monthlyData['pl'] == 'L'])
            annual_summary.loc[month,'Monthly Positions'] = len(monthlyData)
            annual_summary.loc[month,'Hit Percentage'] = round(annual_summary.loc[month,'Profits'] / annual_summary.loc[month,'Monthly Positions'],4)
            if month == 1:
                annual_summary.loc[month,'Gross'] = monthlyData['real_pl'].sum() + fund
            else:
                annual_summary.loc[month,'Gross'] = monthlyData['real_pl'].sum() + annual_summary.loc[month-1,'Neto']
            annual_summary.loc[month,'Commision'] = monthlyData['commision'].sum()
            annual_summary.loc[month,'Neto'] = annual_summary.loc[month,'Gross'] - annual_summary.loc[month,'Commision']
            if month == 1:
                annual_summary.loc[month,'Yield Percantage'] = round(((annual_summary.loc[month,'Neto'] - fund) / fund) * 100,2)
                annual_summary.loc[month,'Change'] = '-'
            else:
                annual_summary.loc[month,'Yield Percantage'] = round(((annual_summary.loc[month,'Neto'] - annual_summary.loc[month-1,'Neto']) / annual_summary.loc[month-1,'Neto']) * 100,2)
                annual_summary.loc[month,'Change'] = annual_summary.loc[month,'Neto'] - annual_summary.loc[month-1,'Neto']
        summaryWithMonth = summary.copy()
        summary.drop(columns='Month',inplace=True)
        return annual_summary,summaryWithMonth


    def calc_annual_sums(self,yearly_sum: pd.DataFrame,fund:float) -> pd.DataFrame:
        yearly_sum.loc['Annual'] = np.nan
        yearly_sum.loc['Annual','Monthly Positions'] = yearly_sum['Monthly Positions'].drop('Annual',axis=0).sum()
        yearly_sum.loc['Annual','Profits'] = yearly_sum['Profits'].drop('Annual',axis=0).sum()
        yearly_sum.loc['Annual','Losses'] = yearly_sum['Losses'].drop('Annual',axis=0).sum()
        yearly_sum.loc['Annual','Hit Percentage'] = round(yearly_sum['Hit Percentage'].mean(),2)
        yearly_sum.loc['Annual','Yield Percantage'] = round((yearly_sum.loc[12,'Neto'] - fund) * 100 / fund,2)
        print(yearly_sum.loc[12,'Neto'],fund)
        yearly_sum.loc['Annual','Commision'] = yearly_sum['Commision'].drop('Annual',axis=0).sum()
        yearly_sum.loc['Annual','Gross'] = yearly_sum.loc[12,'Gross']
        yearly_sum.loc['Annual','Neto'] = yearly_sum.loc[12,'Neto']
        yearly_sum.loc['Annual','Change'] = '-'


        return yearly_sum
       
    def n_days_distribution(self,summary_by_month:pd.DataFrame,n: int):
        month_list = summary_by_month['Month'].unique()
        summary_by_month['date'] = pd.to_datetime(summary_by_month['date'])
        lables = ['January 1','Januray 2','February 1','February 2','March 1','March 2','April 1','April 2','May 1','May 2','June 1','June 2','July 1','July 2',
                    'August 1','August 2','September 1','September 2','October 1','October 2','November 1','November 2','December 1','December 2']
        hit_percentage_list = []
        number_of_profits_list = []
        number_of_loses_list = []
        for month in month_list:
            current_month_positions = summary_by_month[summary_by_month['Month'] == month]
            dates_list = current_month_positions['date'].unique()
            split_date = dates_list[n-1]
            first_period_positions = current_month_positions[current_month_positions['date'] < split_date]
            second_period_posisions = current_month_positions[current_month_positions['date'] >= split_date]
            first_period_profits_num = first_period_positions[first_period_positions['pl'] == 'P'].count()['pl']
            first_period_loses_num = first_period_positions[first_period_positions['pl'] == 'L'].count()['pl']
            second_period_profits_num = second_period_posisions[second_period_posisions['pl'] == 'P'].count()['pl']
            second_period_loses_num = second_period_posisions[second_period_posisions['pl'] == 'L'].count()['pl']
            number_of_profits_list.append(first_period_profits_num)
            number_of_profits_list.append(second_period_profits_num)
            number_of_loses_list.append(first_period_loses_num)
            number_of_loses_list.append(second_period_loses_num)
            hit_percentage_list.append(round((first_period_profits_num / (first_period_loses_num + first_period_profits_num) * 100),2))
            hit_percentage_list.append(round((second_period_profits_num / (second_period_loses_num + second_period_profits_num) * 100),2))
            
        pl_df = pd.DataFrame(columns=['Month','Hit Percentage','Number Of Profits','Number Of Loses'])
        pl_df['Month'] = lables
        pl_df['Hit Percentage'] = hit_percentage_list
        pl_df['Number Of Profits'] = number_of_profits_list
        pl_df['Number Of Loses'] = number_of_loses_list
        pl_df = pl_df.set_index('Month')

        return pl_df

    def half_hour_distribution(self,summary_by_month: pd.DataFrame):
        months_names = ['January','February','March','April','May','June','July',
                    'August','September','October','November','December']
        summary_by_month['30Min Split'] = pd.to_datetime('2021-04-01' + " " + summary_by_month['time'])
        month_list = summary_by_month['Month'].unique()
        month_num = 0
        for month in month_list:
            current_month_positions = summary_by_month[summary_by_month['Month'] == month]
            month_profits = current_month_positions[current_month_positions['pl'] == 'P']
            month_loses = current_month_positions[current_month_positions['pl'] == 'L']
            month_profits_by_30_min = month_profits.resample('30Min',on='30Min Split')
            month_loses_by_30_min = month_loses.resample('30Min',on='30Min Split')
            profits_num = month_profits_by_30_min['pl'].count()
            if(month == 1):
                df = pd.DataFrame(columns= months_names)
            loses_num = month_loses_by_30_min['pl'].count()
            profits_length = len(profits_num)
            loses_length = len(loses_num)
            month_hit_perc = []
            if(profits_length == loses_length):
                for i in range(profits_length):
                    hit_perc = round(profits_num[i] / (profits_num[i] + loses_num[i]) * 100,2)
                    month_hit_perc.append(hit_perc)
            elif (profits_length > loses_length):
                diff = profits_length - loses_length
                for i in range(loses_length):
                    hit_perc = round(profits_num[i] / (profits_num[i] + loses_num[i]) * 100,2)
                    month_hit_perc.append(hit_perc)
                for i in range(diff):
                    hit_perc = 100
                    month_hit_perc.append(hit_perc)
            else:
                diff = loses_length - profits_length
                for i in range(profits_length):
                    hit_perc = round(profits_num[i] / (profits_num[i] + loses_num[i]) * 100,2)
                    month_hit_perc.append(hit_perc)
                for i in range(diff):
                    hit_perc = 0
                    month_hit_perc.append(hit_perc)
            try:
                df[months_names[month_num]] = month_hit_perc
                month_num += 1
            except Exception as e:
                print(e)
        df = assist.fix_half_hour_index(df)
        df = assist.calc_avg(df)
        df = df.transpose()
        return df

    def hour_distribution(self,summary_by_month):
        months_names = ['January','February','March','April','May','June','July',
                    'August','September','October','November','December']
        summary_by_month['1Hour Split'] = pd.to_datetime('2021-04-01' + " " + summary_by_month['time'])
        month_list = summary_by_month['Month'].unique()
        month_num = 0
        for month in month_list:
            current_month_positions = summary_by_month[summary_by_month['Month'] == month]
            month_profits = current_month_positions[current_month_positions['pl'] == 'P']
            month_loses = current_month_positions[current_month_positions['pl'] == 'L']
            month_profits_by_30_min = month_profits.resample('60Min',on='1Hour Split')
            month_loses_by_30_min = month_loses.resample('60Min',on='1Hour Split')
            profits_num = month_profits_by_30_min['pl'].count()
            if(month == 1):
                df = pd.DataFrame(columns= months_names)
            loses_num = month_loses_by_30_min['pl'].count()
            profits_length = len(profits_num)
            loses_length = len(loses_num)
            month_hit_perc = []
            if(profits_length == loses_length):
                for i in range(profits_length):
                    hit_perc = round(profits_num[i] / (profits_num[i] + loses_num[i]) * 100,2)
                    month_hit_perc.append(hit_perc)
            elif (profits_length > loses_length):
                diff = profits_length - loses_length
                for i in range(loses_length):
                    hit_perc = round(profits_num[i] / (profits_num[i] + loses_num[i]) * 100,2)
                    month_hit_perc.append(hit_perc)
                for i in range(diff):
                    hit_perc = 100
                    month_hit_perc.append(hit_perc)
            else:
                diff = loses_length - profits_length
                for i in range(profits_length):
                    hit_perc = round(profits_num[i] / (profits_num[i] + loses_num[i]) * 100,2)
                    month_hit_perc.append(hit_perc)
                for i in range(diff):
                    hit_perc = 0
                    month_hit_perc.append(hit_perc)
            try:
                df[months_names[month_num]] = month_hit_perc
                month_num += 1
            except Exception as e:
                print(e)
        df = assist.fix_hourly_index(df)
        df = assist.calc_avg(df)
        df = df.transpose()
        return df

 

            
            
  
            

            
            
            













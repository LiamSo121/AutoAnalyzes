from email.errors import StartBoundaryNotFoundDefect
import pandas as pd
import numpy as np
import math
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from GroupBy import GroupBy
from Assistant import Assistant

assist = Assistant()

class monthlySummary:
    def create_df(self) -> pd.DataFrame:
        cols = ['Months','Profit','Lose','Monthly Sum','Positions Number','Profit Pos Number','Lose Pos Number','Hit Percentage','Yield Percantage','Fund']
        monthlySum = pd.DataFrame(columns= cols).set_index('Months') 
        monthlySum.fillna('-',inplace=True)
        return monthlySum


    def calc_monthly(self,summary: pd.DataFrame,annual_summary: pd.DataFrame) -> pd.DataFrame:
        summary['Month'] = pd.DatetimeIndex(summary['date']).month
        months = summary['Month'].unique()
        for month in months:
            monthlyData = summary[summary['Month'] == month]
            nextMonthData = summary[summary['Month'] == month+1]
            monthlyProfits = 0
            monthlyLoses = 0
            for d_change in monthlyData['change']:
                if(d_change > 0):
                    monthlyProfits += d_change
                else:
                    monthlyLoses -= d_change
            annual_summary.loc[month,'Profit'] = monthlyProfits
            annual_summary.loc[month,'Lose'] = monthlyLoses
            annual_summary.loc[month,'Monthly Sum'] = monthlyProfits - monthlyLoses
            annual_summary.loc[month,'Profit Pos Number'] = monthlyData[(monthlyData['pl'] == 'P')].shape[0]
            annual_summary.loc[month,'Lose Pos Number'] = monthlyData[(monthlyData['pl'] == 'L')].shape[0]
            annual_summary.loc[month,'Positions Number'] = monthlyData[(monthlyData['pl'] == 'P')].shape[0] + monthlyData[(monthlyData['pl'] == 'L')].shape[0]
            annual_summary.loc[month,'Hit Percentage'] = round((annual_summary.loc[month,'Profit Pos Number'] / annual_summary.loc[month,'Positions Number']) * 100,2)
            startOfMonthFund = monthlyData.loc[monthlyData[monthlyData['present value daily'] !='-'].first_valid_index(),'present value daily']
            if (month != 12):
                endOfMonthFund = nextMonthData.loc[nextMonthData[nextMonthData['present value daily'] != '-'].first_valid_index(),'present value daily']
            else:
                endOfMonthFund = monthlyData.loc[monthlyData[monthlyData['present value daily'] !='-'].last_valid_index(),'present value daily']
            annual_summary.loc[month,'Yield Percantage'] = round(((endOfMonthFund - startOfMonthFund) / startOfMonthFund) * 100,2)
            annual_summary.loc[month,'Fund'] = round(startOfMonthFund,2)
            if (month == 12):
                annual_summary.loc['Annual'] = np.nan
                annual_summary.loc['Annual','Fund'] = annual_summary.loc[12,'Fund'] + annual_summary.loc[12,'Monthly Sum']
        summaryWithMonth = summary.copy()
        summary.drop(columns='Month',inplace=True)
        return annual_summary,summaryWithMonth


    def calc_annual_sums(self,monthlySum: pd.DataFrame) -> pd.DataFrame:
        monthlySum.loc['Annual','Positions Number'] = monthlySum['Positions Number'].drop('Annual',axis=0).sum()
        monthlySum.loc['Annual','Profit'] = monthlySum['Profit'].drop('Annual',axis=0).sum()
        monthlySum.loc['Annual','Lose'] = monthlySum['Lose'].drop('Annual',axis=0).sum()
        monthlySum.loc['Annual','Monthly Sum'] = monthlySum['Monthly Sum'].drop('Annual',axis=0).sum()
        monthlySum.loc['Annual','Profit Pos Number'] = monthlySum['Profit Pos Number'].drop('Annual',axis=0).sum()
        monthlySum.loc['Annual','Lose Pos Number'] = monthlySum['Lose Pos Number'].drop('Annual',axis=0).sum()
        monthlySum.loc['Annual','Hit Percentage'] = round(monthlySum['Hit Percentage'].mean(),2)
        monthlySum.loc['Annual','Yield Percantage'] = monthlySum['Yield Percantage'].drop('Annual',axis=0).sum()
        return monthlySum
       
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

        return pl_df

    def half_hour_distribution(self,summary_by_month: pd.DataFrame, n: int):
        months_names = ['January','February','March','April','May','June','July',
                    'August','September','October','November','December']
        summary_by_month = assist.remove_problem_dates(summary_by_month)
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
            df[months_names[month_num]] = month_hit_perc
            month_num += 1
        df = assist.fix_half_hour_index(df)
        df = assist.calc_avg(df)
        df = df.transpose()
        return df

    def hour_distribution(self,summary_by_month):
        months_names = ['January','February','March','April','May','June','July',
                    'August','September','October','November','December']
        summary_by_month = assist.remove_problem_dates(summary_by_month)
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
            df[months_names[month_num]] = month_hit_perc
            month_num += 1
        df = assist.fix_hourly_index(df)
        df = assist.calc_avg(df)
        df = df.transpose()
        return df

 

            
            
  
            

            
            
            













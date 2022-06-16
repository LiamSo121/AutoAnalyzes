import pandas as pd
import numpy as np
import math
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

class monthlySummary:
    def create_df(self) -> pd.DataFrame:
        cols = ['Months','Profit','Lose','Monthly Sum','Positions Number','Profit Pos Number','Lose Pos Number','Hit Percentage','Yield Percantage','Fund']
        monthlySum = pd.DataFrame(columns= cols).set_index('Months') 
        monthlySum.fillna('-',inplace=True)
        return monthlySum


    def calc_monthly(self,summary: pd.DataFrame,monthlySum: pd.DataFrame) -> pd.DataFrame:
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
            monthlySum.loc[month,'Profit'] = monthlyProfits
            monthlySum.loc[month,'Lose'] = monthlyLoses
            monthlySum.loc[month,'Monthly Sum'] = monthlyProfits - monthlyLoses
            monthlySum.loc[month,'Profit Pos Number'] = monthlyData[(monthlyData['pl'] == 'P')].shape[0]
            monthlySum.loc[month,'Lose Pos Number'] = monthlyData[(monthlyData['pl'] == 'L')].shape[0]
            monthlySum.loc[month,'Positions Number'] = monthlyData[(monthlyData['pl'] == 'P')].shape[0] + monthlyData[(monthlyData['pl'] == 'L')].shape[0]
            monthlySum.loc[month,'Hit Percentage'] = round((monthlySum.loc[month,'Profit Pos Number'] / monthlySum.loc[month,'Positions Number']) * 100,2)
            startOfMonthFund = monthlyData.loc[monthlyData[monthlyData['present value daily'] !='-'].first_valid_index(),'present value daily']
            if (month != 12):
                endOfMonthFund = nextMonthData.loc[nextMonthData[nextMonthData['present value daily'] != '-'].first_valid_index(),'present value daily']
            else:
                endOfMonthFund = monthlyData.loc[monthlyData[monthlyData['present value daily'] !='-'].last_valid_index(),'present value daily']
            monthlySum.loc[month,'Yield Percantage'] = round(((endOfMonthFund - startOfMonthFund) / startOfMonthFund) * 100,2)
            monthlySum.loc[month,'Fund'] = round(startOfMonthFund,2)
            if (month == 12):
                monthlySum.loc['Annual'] = np.nan
                monthlySum.fillna('-',inplace=True)
                monthlySum.loc['Annual','Fund'] = monthlySum.loc[12,'Fund'] + monthlySum.loc[12,'Monthly Sum']
        summaryWithMonth = summary.copy()
        summary.drop(columns='Month',inplace=True)
        return monthlySum,summaryWithMonth


    def calc_sums(self,monthlySum: pd.DataFrame) -> pd.DataFrame:
        monthlySum.loc['Annual','Positions Number'] = monthlySum['Positions Number'].drop('Annual',axis=0).sum()
        monthlySum.loc['Annual','Profit'] = monthlySum['Profit'].drop('Annual',axis=0).sum()
        monthlySum.loc['Annual','Lose'] = monthlySum['Lose'].drop('Annual',axis=0).sum()
        monthlySum.loc['Annual','Monthly Sum'] = monthlySum['Monthly Sum'].drop('Annual',axis=0).sum()
        monthlySum.loc['Annual','Profit Pos Number'] = monthlySum['Profit Pos Number'].drop('Annual',axis=0).sum()
        monthlySum.loc['Annual','Lose Pos Number'] = monthlySum['Lose Pos Number'].drop('Annual',axis=0).sum()
        monthlySum.loc['Annual','Hit Percentage'] = round((monthlySum.loc['Annual','Profit Pos Number'] / monthlySum.loc['Annual','Positions Number']) * 100,2)
        monthlySum.loc['Annual','Yield Percantage'] = monthlySum['Yield Percantage'].drop('Annual',axis=0).sum()
        return monthlySum
       
    def distribution_by_month_and_time(self,summary_by_month:pd.DataFrame,n: int):
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



            

            
            
            













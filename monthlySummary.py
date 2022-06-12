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

    def two_weeks_summary(self,two_weeks_summary):
        month_list = two_weeks_summary['Month'].unique()
        for month in month_list[0:2]:
            dates = []
            first_pl_results = []


            current_month_positions = two_weeks_summary[two_weeks_summary['Month'] == month]
            current_month_positions['date'] = pd.to_datetime(current_month_positions['date'])
            first_date_in_month =current_month_positions.iloc[0,8]
            last_date_in_month = current_month_positions.iloc[-1,8]
            middle_of_the_month = first_date_in_month + (last_date_in_month - first_date_in_month) / 2
            first_two_weeks_positions = current_month_positions[current_month_positions['date'] < middle_of_the_month]
            second_two_weeks_positions = current_month_positions[current_month_positions['date'] >= middle_of_the_month]
            # print(first_two_weeks_positions['pl'].value_counts())
            # print(second_two_weeks_positions['pl'].value_counts())
            first_two_weeks_profit_num = first_two_weeks_positions[first_two_weeks_positions['pl'] == 'P'].count()['pl']
            first_two_weeks_loses_num = first_two_weeks_positions[first_two_weeks_positions['pl'] == 'L'].count()['pl']
            second_two_weeks_profit_num = second_two_weeks_positions[second_two_weeks_positions['pl'] == 'P'].count()['pl']
            second_two_weeks_loses_num = second_two_weeks_positions[second_two_weeks_positions['pl'] == 'L'].count()['pl']


       
      
        xlables = ['January First P','Januray second L','February first P','February second L']
        # sns.set_style('darkgrid')
        # sns.barplot(x= xlables,y = pl_ressults)
        print(first_pl_results)
        # plt.show()


            

            
            
            













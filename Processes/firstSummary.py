from matplotlib.pyplot import axis
import pandas as pd
import numpy as np
from datetime import datetime,timedelta,time


class summaryAutomation:
    def fix_data(self,summary) -> pd.DataFrame:
        summary['stop_at'] =  pd.to_datetime(summary['stop_at'])
        summary.drop(['high','low','risk','stop_loss_type'],axis=1,inplace=True)
        summary['change'] = np.nan
        summary['present value daily'] = np.nan
        summary.fillna('-',inplace=True)
        return summary


    def clean_data(self,summary: pd.DataFrame) -> pd.DataFrame:
        summary = summary[summary['pl'] != 'C'].reset_index(drop=True)
        return summary

    
    def calculate_pl(self,summary: pd.DataFrame,risk: float, fund: float) -> pd.DataFrame:
        dates = summary['date'].unique()
        print(f'There are {len(dates)} trading days')
        for date in dates:
            startOfTheDayFund = fund
            daily_fund_risk = fund * risk
            daily_fund_risk = round(daily_fund_risk,2)
            summary['change'].mask((summary['date'] == date) & (summary['pl'] == 'P'),daily_fund_risk,inplace= True)
            summary['change'].mask((summary['date'] == date) & (summary['pl'] == 'L'),daily_fund_risk * (-1),inplace= True)
            profits_num = summary[(summary['date'] == date) & (summary['pl'] == 'P')].shape[0]
            loses_num = summary[(summary['date'] == date) & (summary['pl'] == 'L')].shape[0]
            daily_change = (profits_num - loses_num) * daily_fund_risk
            fund += daily_change
            rowNumber = summary[summary['date'] == date].index[-1]
            summary.loc[rowNumber,'present value daily'] = round(startOfTheDayFund)



        return summary

    def calculate_commision(self,summary: pd.DataFrame) -> np.array:
        quantities = np.array(summary['quantity'])   
        commisions = np.where(quantities < 250,4,((quantities-250) * 0.008) + 4)
        return commisions


    def fix_problem_dates(self,summary: pd.DataFrame):
        summary['time'] = pd.to_datetime(summary['time'])
        summary['time'] = [time.time() for time in summary['time']]
        summary['date'] = pd.to_datetime(summary['date'])
        problem_dates_index_list = summary[summary['time'] < time(16,00)]['date']
        problem_dates_index_list = problem_dates_index_list.unique()
        summary['newDateTime'] = np.nan
        for index,row in summary.iterrows():
            if row['date'] in problem_dates_index_list:
                row['newDateTime'] = datetime.combine(row['date'],row['time'])
                row['newDateTime'] += timedelta(hours=1)
                summary.loc[index,'time'] = row['newDateTime'].time()

        summary['time'] = summary['time'].astype(str)
        summary.drop(columns='newDateTime',axis=1,inplace=True)
        return summary

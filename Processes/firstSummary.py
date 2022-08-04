from matplotlib.pyplot import axis
import pandas as pd
import numpy as np
from datetime import datetime,timedelta,time
from helpers.Assistant import Assistant



assist = Assistant()
class summaryAutomation:
    
    def fix_data(self,summary) -> pd.DataFrame:
        summary['stop_at'] =  pd.to_datetime(summary['stop_at'])
        summary.drop(['high','low','risk','stop_loss_type','gap','cost','leverage_cost','highest','lowest','bp_filled_at'],axis=1,inplace=True)
        summary['real_pl'] = np.nan
        summary['commision'] = np.nan
        summary['Neto'] = np.nan
        summary.fillna('-',inplace=True)
        return summary


    def clean_data(self,summary: pd.DataFrame) -> pd.DataFrame:
        summary = summary[summary['pl'] != 'C'].reset_index(drop=True)
        return summary


    
    
    def calculate_pl(self,summary: pd.DataFrame,risk: float, fund: float) -> pd.DataFrame:
        i = 0
        dates = summary['date'].unique()
        for date in dates:
            daily_pl = 0
            daily_risk = assist.calculate_risk(fund,risk)
            daily_df = summary[summary['date'] == date]
            for index,row in daily_df.iterrows():
                position_attributes = [daily_risk,row['action'],row['buy_point'],row['take_profit'],row['stop_loss']]
                summary.loc[index,'quantity'] = assist.calculate_quantity(position_attributes)
                summary.loc[index,'commision'] = assist.calculate_commision(summary.loc[index,'quantity'])
                if row['pl'] == 'P' and row['action'] == 'BUY':
                    summary.loc[index,'real_pl'] = round(summary.loc[index,'quantity'] * (summary.loc[index,'take_profit'] - summary.loc[index,'buy_point']),2)
                elif row['pl'] == 'P' and row['action'] == 'SELL':
                    summary.loc[index,'real_pl'] = round(summary.loc[index,'quantity']  * (summary.loc[index,'buy_point'] - summary.loc[index,'take_profit']),2)
                elif row['pl'] == 'L' and row['action'] == 'BUY':
                    summary.loc[index,'real_pl'] =  round(-1 * (summary.loc[index,'quantity'] * (summary.loc[index,'buy_point'] - summary.loc[index,'stop_loss'])),2)
                elif row['pl'] == 'L' and row['action'] == 'SELL':
                    summary.loc[index,'real_pl'] = round(-1 * (summary.loc[index,'quantity'] * (summary.loc[index,'stop_loss'] - summary.loc[index,'buy_point'])),2)
                summary.loc[index,'Neto'] = summary.loc[index,'real_pl'] - summary.loc[index,'commision']    
                i += 1
                
            fund += summary[summary['date'] == date]['Neto'].sum()
            rowNumber = summary[summary['date'] == date].index[-1]
            summary.loc[rowNumber,'present value daily'] = round(fund,2)
        return summary
    
    def calculate_pl_after_commision(self,summary: pd.DataFrame):
        pl_array = np.array(summary['Real_pl'])
        commision_array = np.array(summary['commision'])
        neto_pl = pl_array - commision_array
        return neto_pl

    def fix_problem_dates(self,summary: pd.DataFrame) -> pd.DataFrame:
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

from operator import index
from matplotlib.pyplot import axis
import pandas as pd
import numpy as np
from datetime import datetime,timedelta,time
from helpers.Assistant import Assistant



assist = Assistant()
class summaryAutomation:
    
    def fix_data(self,summary) -> pd.DataFrame:
        summary['real_pl'] = np.nan
        summary['commision'] = np.nan
        summary['new_quantity'] = np.nan
        summary['Neto'] = np.nan
        summary.fillna('-',inplace=True)
        return summary


    def clean_data(self,summary: pd.DataFrame) -> pd.DataFrame:
        summary.drop(['bp_filled_price','bp_filled_at','stop_at','created_at','pl_amount','highest','lowest','pl_filled_price'],axis=1,inplace=True)
        summary = summary[summary['pl'] != 'C'].reset_index(drop=True)
        return summary


    
    
    def calculate_pl(self,summary: pd.DataFrame,risk: float, fund: float) -> pd.DataFrame:
        i = 0
        summary['date'] = pd.to_datetime(summary['date'])
        dates = summary['date'].unique()
        daily_risk = assist.calculate_risk(fund,risk)
        for date in dates:
            daily_df = summary[summary['date'] == date]
            for index,row in daily_df.iterrows():
                position_attributes = [daily_risk,row['action'],row['buy_point'],row['take_profit'],row['stop_loss']]
                summary.loc[i,'new_quantity'] = assist.calculate_quantity(position_attributes)
                summary.loc[i,'commision'] = assist.calculate_commision(summary.loc[i,'new_quantity'])
                if row['pl'] == 'P' and row['action'] == 'BUY':
                    summary.loc[i,'real_pl'] = round(summary.loc[i,'new_quantity'] * (summary.loc[i,'take_profit'] - summary.loc[i,'buy_point']),2)
                elif row['pl'] == 'P' and row['action'] == 'SELL':
                    summary.loc[i,'real_pl'] = round(summary.loc[i,'new_quantity']  * (summary.loc[i,'buy_point'] - summary.loc[i,'take_profit']),2)
                elif row['pl'] == 'L' and row['action'] == 'BUY':
                    summary.loc[i,'real_pl'] =  round(-1 * (summary.loc[i,'new_quantity'] * (summary.loc[i,'buy_point'] - summary.loc[i,'stop_loss'])),2)
                elif row['pl'] == 'L' and row['action'] == 'SELL':
                    summary.loc[i,'real_pl'] = round(-1 * (summary.loc[i,'new_quantity'] * (summary.loc[i,'stop_loss'] - summary.loc[i,'buy_point'])),2)
                summary.loc[i,'Neto'] = summary.loc[i,'real_pl'] - summary.loc[i,'commision']
                i += 1
            fund += summary[summary['date'] == date]['Neto'].sum()
            rowNumber = summary[summary['date'] == date].index[-1]
            summary.loc[rowNumber,'present value daily'] = round(fund,2)
            daily_risk = assist.calculate_risk(summary.loc[rowNumber,'present value daily'],risk)
        return summary
    
    def calculate_pl_after_commision(self,summary: pd.DataFrame):
        pl_array = np.array(summary['Real_pl'])
        commision_array = np.array(summary['commision'])
        neto_pl = pl_array - commision_array
        return neto_pl

  
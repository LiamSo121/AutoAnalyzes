from matplotlib.pyplot import axis
import pandas as pd
import numpy as np
import datetime as dt


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




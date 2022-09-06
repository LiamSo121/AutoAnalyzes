from itertools import count
from tokenize import group
import pandas as pd
import numpy as np
from datetime import date, datetime
import seaborn as sns
import matplotlib.pyplot as plt
from helpers.Assistant import Assistant
assist = Assistant()
class GroupBy:
    
    def groupByTime(self,summaryOrigin: pd.DataFrame):
        summary = summaryOrigin.copy()
        summary['30Min Split'] = pd.to_datetime('2021-04-01' + " " + summary['time'])
        profits = summary[summary['pl'] == 'P']
        loses = summary[summary['pl'] == 'L']
        profitSummary = profits.resample('30Min',on='30Min Split')['pl'].count()
        losesSummary = loses.resample('30Min',on='30Min Split')['pl'].count()
        return profitSummary,losesSummary

    def groupByType(self,summary: pd.DataFrame):
        summaryGroupedByType = summary.groupby(by=['type','pl'],sort= True)['pl'].count()
        return summaryGroupedByType

    def hit_perc_by_symbol(self,summary:pd.DataFrame):
        symbols_df = pd.DataFrame(columns=['Symbol','Total Positions','Profits','Losses','Hit Percentage'])
        symbols = summary['symbol'].unique()
        for symbol in symbols:
            symbol_df = summary[summary['symbol'] == symbol]
            symbol_positions = len(symbol_df)
            symbol_profits = len(symbol_df[symbol_df['pl'] == 'P'])
            symbol_loses = len(symbol_df[symbol_df['pl'] == 'L'])
            symbol_hit_percentage = round((symbol_profits / symbol_positions) * 100,3)
            temp_df = pd.DataFrame({'Symbol':[symbol],'Total Positions': [symbol_positions],'Profits': symbol_profits,'Losses':[symbol_loses],'Hit Percentage':[symbol_hit_percentage]})
            symbols_df = pd.concat([symbols_df,temp_df])
        symbols_df = symbols_df.sort_values(by=['Total Positions','Hit Percentage'],ascending=[False,False]).set_index('Symbol')
        return symbols_df

    def group_by_gap_percent(self,summary:pd.DataFrame):
        gaps_array = np.arange(1,102,5)
        profit_df = summary[summary['pl'] == 'P'][['gap','pl']]
        losses_df = summary[summary['pl'] == 'L'][['gap','pl']]
        profit_df['new_gap'] = pd.cut(profit_df['gap'],gaps_array)
        losses_df['new_gap'] = pd.cut(losses_df['gap'],gaps_array)
        profit_df.dropna(subset=['new_gap'],inplace=True)
        losses_df.dropna(subset=['new_gap'],inplace=True)
        profit_pivot = pd.pivot_table(profit_df,values=['pl'],index='new_gap',aggfunc= 'count')
        losses_pivot = pd.pivot_table(losses_df,values=['pl'],index='new_gap',aggfunc= 'count')
        profit_pivot.reset_index(inplace=True)
        losses_pivot.reset_index(inplace=True)
        total_positions = profit_pivot['pl'] + losses_pivot['pl']
        hit_percentages = (profit_pivot['pl'] / total_positions) * 100
        final_table = pd.DataFrame()
        final_table['gap'] = profit_pivot['new_gap']
        final_table['hit_perc'] = hit_percentages

        return final_table 





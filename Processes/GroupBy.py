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
        types = summary['type'].unique()
        summaryGroupedByType = summary.groupby(by=['type','pl'],sort= True)['pl'].count()
        return summaryGroupedByType



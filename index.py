import pandas as pd
from helpers.AnalyzeHelpers import AnalizeHelpers
from Processes.Visualization import Visual
from os import walk
import numpy as np
import csv


pd.options.mode.chained_assignment = None  # default='warn'
visual = Visual()
analize_helper = AnalizeHelpers()
path = './Outputs'
file_names = next(walk(path),(None,None,[]))[2]
# Define risk percantage
risk = 0.002
# Define Starting Fund
fund = 100000

df = pd.DataFrame(columns=['Symbol','Total Positions','Profits','Losses','Hit Percentage'])
for filename in file_names:
    summaryOrigin = pd.read_excel(f"Outputs\\{filename}",sheet_name='Hit By Symbol')
    summaryOrigin = summaryOrigin[summaryOrigin['Hit Percentage'] > 50]
    df = pd.concat([df,summaryOrigin])
print(df)

table = pd.pivot_table(df,values=['Total Positions','Profits','Losses','Hit Percentage'],index=['Symbol'],
                        aggfunc={'Total Positions': np.sum,'Profits':np.sum,'Losses':np.sum,'Hit Percentage':np.mean}).reset_index()

print(list(table['Symbol']))
table.to_excel('stocks-sl0.02.xlsx')
print('done')

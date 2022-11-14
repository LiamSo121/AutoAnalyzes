from pickle import FALSE
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
name = '2021-no-change'
df = pd.DataFrame(columns=['Symbol','Total Positions','Profits','Losses'])
for filename in file_names:
    summaryOrigin = pd.read_excel(f"Outputs\\{filename}",sheet_name='Hit By Symbol')
    summaryOrigin = summaryOrigin[summaryOrigin['Hit Percentage'] > 50]
    df = pd.concat([df,summaryOrigin])


table = pd.pivot_table(df,values=['Total Positions','Profits','Losses'],index=['Symbol'],
                        aggfunc={'Total Positions': np.sum,'Profits':np.sum,'Losses':np.sum}).reset_index()

total_Positions = np.array(table['Total Positions'])
profits = np.array(table['Profits'])
table['Hit Percentage'] = np.divide(profits,total_Positions) * 100
df = table.reindex(table.sort_values(by=['Total Positions','Hit Percentage'], ascending=[False,False]).index)
f= open(f"stocks-{name}.txt","w+")
f.write(str(list(df['Symbol'])))
f.close()
table.to_excel(f'stocks-{name}.xlsx')

print('done')

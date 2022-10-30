import pandas as pd
from helpers.AnalyzeHelpers import AnalizeHelpers
from Processes.Visualization import Visual
from os import walk
import csv
import re


pd.options.mode.chained_assignment = None  # default='warn'
visual = Visual()
analize_helper = AnalizeHelpers()
path = './Outputs'
file_names = next(walk(path),(None,None,[]))[2]
# Define risk percantage
risk = 0.004
# Define Starting Fund
fund = 14300


years_list = ['2015','2016','2017', '2018', '2019', '2020','2021']
dict = {}
for year in years_list:
    dict[year] = {}
    i = 0
    for filename in file_names:
        if year in filename:
            filename = filename[:-5] + '.xlsx'
            data = pd.read_excel(f"Outputs\\{filename}",sheet_name= 'Summary')
            dict[year][f'0.0{i}'] = data.loc[12,'Hit Percentage']
            #dict[year][f'0.0{i}'] = data.loc[12,'Neto']



               
            i += 1



print(dict)
analize_helper.visualize(dict)






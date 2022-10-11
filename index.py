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


    # output_file_name = filename + '-Analyzed'
    # summaryOrigin = pd.read_csv(f"Outputs\\{filename}")
    # summary = summaryOrigin.copy()
    # # Stage 1 - Analyze daily positions
    # summary = analize_helper.add_daily_change(summary,risk,fund)
    # # Stage 2 - Analize Monthly
    # yearlySum,half_hour_hit_percantage,hourly_hit_percantage = analize_helper.calc_yearly(summary,fund)
    # # Stage 3 - Grouping By
    # groupByType,profitsBy30Min,losesBy30Min,groupBySymbol,groupByGap = analize_helper.group_by(summary)
    # # Stage 4 - Export all the data to xlsx file
    # export_list = [summary,yearlySum,groupByType,profitsBy30Min,losesBy30Min,half_hour_hit_percantage,hourly_hit_percantage,groupBySymbol,groupByGap]
    # analize_helper.export_to_excel(export_list,output_file_name)
    #stage 5 - Visualization

years_list = [ '2018', '2019', '2020','2021']
dict = {}
for year in years_list:
    dict[year] = {}
    i = 0
    for filename in file_names:
        if year in filename:
            if f'0.0{i}' in filename:
                filename = filename[:-5] + '.xlsx'
                data = pd.read_excel(f"Outputs\\{filename}",sheet_name= 'Summary')
                #y_values.append(data.loc[12,'Hit Percentage'])
                dict[year][f'0.0{i}'] = data.loc[12,'Hit Percentage']
            else:
                filename = filename[:-5] + '.xlsx'
                data = pd.read_excel(f"Outputs\\{filename}",sheet_name= 'Summary')
                #y_values.append(data.loc[12,'Hit Percentage'])
                dict[year][f'0.00'] = data.loc[12,'Hit Percentage']
            i += 1
print(dict)



analize_helper.visualize(dict)






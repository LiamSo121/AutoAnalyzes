import pandas as pd
from helpers.AnalyzeHelpers import AnalizeHelpers
from Processes.Visualization import Visual
from os import walk
import csv


pd.options.mode.chained_assignment = None  # default='warn'
visual = Visual()
analize_helper = AnalizeHelpers()
path = './Excel_files'
file_names = next(walk(path),(None,None,[]))[2]
# Define risk percantage
risk = 0.002
# Define Starting Fund
fund = 100000
for filename in file_names:
    output_file_name = filename + '-Analyzed-filtered-stocks'
    summaryOrigin = pd.read_csv(f"Excel_files\\{filename}")
    
    summary = summaryOrigin.copy()
    # Stage 1 - Analyze daily positions
    summary = analize_helper.add_daily_change(summary,risk,fund)
    # Stage 2 - Analize Monthly
    yearlySum,half_hour_hit_percantage,hourly_hit_percantage = analize_helper.calc_yearly(summary,fund)
    # Stage 3 - Grouping By
    groupByType,profitsBy30Min,losesBy30Min,groupBySymbol,groupByGap = analize_helper.group_by(summary)
    # Stage 4 - Export all the data to xlsx file
    export_list = [summary,yearlySum,groupByType,profitsBy30Min,losesBy30Min,half_hour_hit_percantage,hourly_hit_percantage,groupBySymbol,groupByGap]
    analize_helper.export_to_excel(export_list,output_file_name)
    #stage 5 - Visualization
    #analize_helper.visualize(output_file_name)
    print(f'{filename} Is done :)')


print("All files have been analyzed")



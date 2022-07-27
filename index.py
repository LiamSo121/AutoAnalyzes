from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from helpers.AnalyzeHelpers import AnalizeHelpers
from Processes.Visualization import Visual
from datetime import datetime,time
from datetime import timedelta


pd.options.mode.chained_assignment = None  # default='warn'
visual = Visual()
analize_helper = AnalizeHelpers()

# Input xlsx file
summaryOrigin = pd.read_excel("orders-low-tp.xlsx")
summary = summaryOrigin.copy()

# Define risk percantage
risk = 0.005
# Define Starting Fund
fund = 30960
# Define output name
output_file_name = 'highLiam'

# # Stage 1 - Analyze daily positions
# summary = analize_helper.add_daily_change(summary,risk,fund)
# # Stage 2 - Analize Monthly
# yearlySum,by_period_df,half_hour_hit_percantage,hourly_hit_percantage = analize_helper.calc_yearly(summary)
# # Stage 3 - Grouping By
# groupByType,profitsBy30Min,losesBy30Min = analize_helper.group_by(summary)
# # Stage 4 - Export all the data to xlsx file
# export_list = [summary,yearlySum,groupByType,profitsBy30Min,losesBy30Min,by_period_df,half_hour_hit_percantage,hourly_hit_percantage]
# analize_helper.export_to_excel(export_list,output_file_name)
# #stage 5 - Visualization
# analize_helper.visualize(output_file_name)





def find_problem_dates(summary: pd.DataFrame):
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
            row['time'] = row['newDateTime'].time()
            print(row['time'])
    


    
  


find_problem_dates(summary)


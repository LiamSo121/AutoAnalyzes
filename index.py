import pandas as pd
import numpy as np
from helpers.AnalyzeHelpers import AnalizeHelpers
from Processes.Visualization import Visual


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
output_file_name = 'check'

# Stage 1 - Analyze daily positions
summary = analize_helper.add_daily_change(summary,risk,fund)
# Stage 2 - Analize Monthly
yearlySum,by_period_df,half_hour_hit_percantage,hourly_hit_percantage = analize_helper.calc_yearly(summary)
# Stage 3 - Grouping By
groupByType,profitsBy30Min,losesBy30Min = analize_helper.group_by(summary)
# Stage 4 - Export all the data to xlsx file
export_list = [summary,yearlySum,groupByType,profitsBy30Min,losesBy30Min,by_period_df,half_hour_hit_percantage,hourly_hit_percantage]
analize_helper.export_to_excel(export_list,output_file_name)
#stage 5 - Visualization
analize_helper.visualize(output_file_name)






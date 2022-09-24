import pandas as pd
import numpy as np
from helpers.AnalyzeHelpers import AnalizeHelpers
from Processes.Visualization import Visual


pd.options.mode.chained_assignment = None  # default='warn'
visual = Visual()
analize_helper = AnalizeHelpers()
# Input xlsx file
input_file_name = 'historicalorder-2021'
output_file_name = 'newReportTry'
summaryOrigin = pd.read_csv(f"Excel_files\\{input_file_name}.csv")
summary = summaryOrigin.copy()

# Define risk percantage
risk = 0.004
# Define Starting Fund
fund = 14300
# Define output name


# Stage 1 - Analyze daily positions
summary = analize_helper.add_daily_change(summary,risk,fund)
# Stage 2 - Analize Monthly
yearlySum,by_period_df,half_hour_hit_percantage,hourly_hit_percantage = analize_helper.calc_yearly(summary,fund)
# Stage 3 - Grouping By
groupByType,profitsBy30Min,losesBy30Min,groupBySymbol,groupByGap = analize_helper.group_by(summary)
# Stage 4 - Export all the data to xlsx file
export_list = [summary,yearlySum,groupByType,profitsBy30Min,losesBy30Min,by_period_df,half_hour_hit_percantage,hourly_hit_percantage,groupBySymbol,groupByGap]
analize_helper.export_to_excel(export_list,output_file_name)
#stage 5 - Visualization
#analize_helper.visualize(output_file_name)






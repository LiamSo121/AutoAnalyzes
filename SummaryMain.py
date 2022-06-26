import pandas as pd
import numpy as np
from AnalyzeHelpers import AnalizeHelpers


pd.options.mode.chained_assignment = None  # default='warn'

analize_helper = AnalizeHelpers()
# Input xlsx file
summaryOrigin = pd.read_excel("continues.xlsx")
summary = summaryOrigin.copy()

# Define risk percantage
risk = 0.005
# Define Starting Fund
fund = 30960

to_excel_list = []

# Stage 1 - Analyze daily positions
#summary = analize_helper.add_daily_change(summary,risk,fund)
to_excel_list.append(analize_helper.add_daily_change(summary,risk,fund))
# Stage 2 - Analize Monthly
to_excel_list.append(analize_helper.calc_yearly(to_excel_list[0]))
#yearlySum,by_period_df,half_hour_hit_percantage,hourly_hit_percantage = analize_helper.calc_yearly(summary)
# Stage 3 - Grouping By
to_excel_list.append(analize_helper.group_by(summary))
#groupByType,profitsBy30Min,losesBy30Min = analize_helper.group_by(summary)
# Stage 4 - Export all the data to xlsx file
#analize_helper.export_to_excel(summary,yearlySum,groupByType,profitsBy30Min,losesBy30Min,by_period_df,half_hour_hit_percantage,hourly_hit_percantage)
analize_helper.export_to_excel(to_excel_list)





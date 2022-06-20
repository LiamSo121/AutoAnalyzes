import pandas as pd
import numpy as np
from AnalyzeHelpers import AnalizeHelpers


pd.options.mode.chained_assignment = None  # default='warn'

analize_helper = AnalizeHelpers()
# Input xlsx file
summaryOrigin = pd.read_excel("orders-1-1-stop-loss.xlsx")
summary = summaryOrigin.copy()

# Define risk percantage
risk = 0.005
# Define Starting Fund
fund = 30960

# Stage 1 - Analyze daily positions
summary = analize_helper.add_daily_change(summary,risk,fund)
# Stage 2 - Analize Monthly
yearlySum,by_period_df,hit_by_30_minutes = analize_helper.calc_yearly(summary)
# Stage 3 - Grouping By
groupByType,profitsBy30Min,losesBy30Min = analize_helper.group_by(summary)
# Stage 4 - Export all the data to xlsx file
analize_helper.export_to_excel(summary,yearlySum,groupByType,profitsBy30Min,losesBy30Min,by_period_df,hit_by_30_minutes)






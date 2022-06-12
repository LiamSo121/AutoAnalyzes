import pandas as pd
import numpy as np
from AnalyzeHelpers import AnalizeHelpers

analize_helper = AnalizeHelpers()
# Input xlsx file
summaryOrigin = pd.read_excel("ExcelExample.xlsx")
summary = summaryOrigin.copy()

# Define risk percantage
risk = 0.005
# Define Starting Fund
fund = 30960

# Stage 1 - Analyze daily positions
summary = analize_helper.stage_1(summary,risk,fund)
# Stage 2 - Analize Monthly
yearlySum = analize_helper.stage_2(summary)
# Stage 3 - Grouping By
groupByType,profitsBy30Min,losesBy30Min = analize_helper.stage_3(summary)
# Stage 4 - Export all the data to xlsx file
analize_helper.stage_4(summary,yearlySum,groupByType,profitsBy30Min,losesBy30Min)






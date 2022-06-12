import pandas as pd
import numpy as np
from firstSummary import summaryAutomation
from monthlySummary import monthlySummary
from GroupBy import GroupBy


monthSumObj = monthlySummary()
summaryObj = summaryAutomation()
groupObj = GroupBy()

class AnalizeHelpers:
    
    def stage_1(self,summary: pd.DataFrame,risk:float,fund: float) -> pd.DataFrame:
        summary = summaryObj.fix_data(summary)
        summary = summaryObj.clean_data(summary)
        summary = summaryObj.calculate_pl(summary,risk,fund)

        return summary

    def stage_2(self,summary: pd.DataFrame) -> pd.DataFrame:
        yearlySum = monthSumObj.create_df()
        yearlySum,summaryPerMonth = monthSumObj.calc_monthly(summary,yearlySum)
        yearlySum = monthSumObj.calc_sums(yearlySum)
        monthSumObj.two_weeks_summary(summaryPerMonth)
        return yearlySum

    def stage_3(self,summary: pd.DataFrame):
        groupByType = groupObj.groupByType(summary)
        profitsBy30Min,losesBy30Min = groupObj.groupByTime(summary)
        return groupByType,profitsBy30Min,losesBy30Min

    def stage_4(self,summary,yearlySum,groupByType,profitsBy30Min,losesBy30Min):
        # Output xlsx file name
        writer = pd.ExcelWriter('outputExample.xlsx', engine='xlsxwriter')
        
        summary.to_excel(writer,sheet_name="Data")
        yearlySum.to_excel(writer,sheet_name="Summary")
        groupByType.to_excel(writer,sheet_name="Type Distribution")
        profitsBy30Min.to_excel(writer,sheet_name= "Profits By Time")
        losesBy30Min.to_excel(writer,sheet_name= "Loses By Time")
        writer.save()

        


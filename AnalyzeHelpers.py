import pandas as pd
import numpy as np
from firstSummary import summaryAutomation
from monthlySummary import monthlySummary
from GroupBy import GroupBy


monthSumObj = monthlySummary()
summaryObj = summaryAutomation()
groupObj = GroupBy()

class AnalizeHelpers:
    
    def add_daily_change(self,summary: pd.DataFrame,risk:float,fund: float) -> pd.DataFrame:
        summary = summaryObj.fix_data(summary)
        summary = summaryObj.clean_data(summary)
        summary = summaryObj.calculate_pl(summary,risk,fund)

        return summary

    def calc_yearly(self,summary: pd.DataFrame) -> pd.DataFrame:
        yearlySum = monthSumObj.create_df()
        yearlySum,summaryPerMonth = monthSumObj.calc_monthly(summary,yearlySum)
        yearlySum = monthSumObj.calc_sums(yearlySum)
        # n = number of days to split the month
        by_period_df = monthSumObj.distribution_by_month_and_time(summaryPerMonth,5)
        return yearlySum,by_period_df

    def stage_3(self,summary: pd.DataFrame) -> pd.DataFrame:
        groupByType = groupObj.groupByType(summary)
        profitsBy30Min,losesBy30Min = groupObj.groupByTime(summary)
        return groupByType,profitsBy30Min,losesBy30Min

    def export_to_excel(self,summary,yearlySum,groupByType,profitsBy30Min,losesBy30Min,by_period_df):
        # Output xlsx file name
        writer = pd.ExcelWriter('orders-1-1-stop-lossLiam.xlsx', engine='xlsxwriter')
        summary.to_excel(writer,sheet_name="Data")
        yearlySum.to_excel(writer,sheet_name="Summary")
        groupByType.to_excel(writer,sheet_name="Type Distribution")
        profitsBy30Min.to_excel(writer,sheet_name= "Profits By Time")
        losesBy30Min.to_excel(writer,sheet_name= "Loses By Time")
        by_period_df.to_excel(writer,sheet_name= 'Splitted Month Summary')
        writer.save()

        


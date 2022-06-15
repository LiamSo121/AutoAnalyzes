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
        monthSumObj.distribution_by_month_and_time(summaryPerMonth)
        hit_by_two_weeks = monthSumObj.two_weeks_summary(summaryPerMonth)
        return yearlySum,hit_by_two_weeks

    def stage_3(self,summary: pd.DataFrame) -> pd.DataFrame:
        groupByType = groupObj.groupByType(summary)
        profitsBy30Min,losesBy30Min = groupObj.groupByTime(summary)
        return groupByType,profitsBy30Min,losesBy30Min

    def export_to_excel(self,summary,yearlySum,groupByType,profitsBy30Min,losesBy30Min,hit_by_two_weeks):
        # Output xlsx file name
        writer = pd.ExcelWriter('orders-1-1-stop-lossLiam.xlsx', engine='xlsxwriter')
        summary.to_excel(writer,sheet_name="Data")
        yearlySum.to_excel(writer,sheet_name="Summary")
        groupByType.to_excel(writer,sheet_name="Type Distribution")
        profitsBy30Min.to_excel(writer,sheet_name= "Profits By Time")
        losesBy30Min.to_excel(writer,sheet_name= "Loses By Time")
        hit_by_two_weeks.to_excel(writer,sheet_name= 'Hit Perc By Two Weeks')
        writer.save()

        


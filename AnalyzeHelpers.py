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
        anuual_summary = monthSumObj.create_df()
        anuual_summary,summaryPerMonth = monthSumObj.calc_monthly(summary,anuual_summary)
        anuual_summary = monthSumObj.calc_annual_sums(anuual_summary)
        # n = number of days to split the month
        n_days_summary = monthSumObj.n_days_distribution(summaryPerMonth,5)
        return anuual_summary,n_days_summary

    def group_by(self,summary: pd.DataFrame) -> pd.DataFrame:
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

        


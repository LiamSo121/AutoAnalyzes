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
        # hit_perc_by_30_minutes is available only for all day trading
        hit_perc_by_30_minutes = monthSumObj.half_hour_distribution(summaryPerMonth)
        hit_perc_by_1_hour = monthSumObj.hour_distribution(summaryPerMonth)
        return anuual_summary,n_days_summary,hit_perc_by_30_minutes,hit_perc_by_1_hour

    def group_by(self,summary: pd.DataFrame) -> pd.DataFrame:
        groupByType = groupObj.groupByType(summary)
        profitsBy30Min,losesBy30Min = groupObj.groupByTime(summary)
        return groupByType,profitsBy30Min,losesBy30Min

    def export_to_excel(self,summary,yearlySum,groupByType,profitsBy30Min,losesBy30Min,by_period_df,hit_by_30_minutes,hit_perc_by_1_hour):
        # Output xlsx file name
        writer = pd.ExcelWriter('continuesLiam.xlsx', engine='xlsxwriter')
        summary.to_excel(writer,sheet_name="Data")
        yearlySum.to_excel(writer,sheet_name="Summary")
        groupByType.to_excel(writer,sheet_name="Type Distribution")
        profitsBy30Min.to_excel(writer,sheet_name= "Profits By Time")
        losesBy30Min.to_excel(writer,sheet_name= "Loses By Time")
        by_period_df.to_excel(writer,sheet_name= 'Splitted Month Summary')
        hit_by_30_minutes.to_excel(writer, sheet_name = 'Hit By 30 Minutes')
        hit_perc_by_1_hour.to_excel(writer,sheet_name = 'Hit By 1 Hour')
        writer.save()

        


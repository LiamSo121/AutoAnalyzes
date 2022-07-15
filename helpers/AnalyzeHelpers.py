import pandas as pd
import numpy as np
from Processes.firstSummary import summaryAutomation
from Processes.monthlySummary import monthlySummary
from Processes.GroupBy import GroupBy
from Processes.Visualization import Visual

visualObj = Visual()
monthSumObj = monthlySummary()
summaryObj = summaryAutomation()
groupObj = GroupBy()

class AnalizeHelpers:
    
    def add_daily_change(self,summary: pd.DataFrame,risk:float,fund: float) -> pd.DataFrame:
        summary = summaryObj.fix_data(summary)
        summary = summaryObj.clean_data(summary)
        summary = summaryObj.calculate_pl(summary,risk,fund)
        summary = summaryObj.fix_additional_columns(summary)

        return summary

    def calc_yearly(self,summary: pd.DataFrame) -> pd.DataFrame:
        anuual_summary = monthSumObj.create_df()
        anuual_summary,summaryPerMonth = monthSumObj.calc_monthly(summary,anuual_summary)
        anuual_summary = monthSumObj.calc_annual_sums(anuual_summary)
        # n = number of days to split the month
        n_days_summary = monthSumObj.n_days_distribution(summaryPerMonth,5)
        hit_perc_by_30_minutes = monthSumObj.half_hour_distribution(summaryPerMonth,5)
        hourly_hit_percentage = monthSumObj.hour_distribution(summaryPerMonth)
        return anuual_summary,n_days_summary,hit_perc_by_30_minutes,hourly_hit_percentage

    def group_by(self,summary: pd.DataFrame) -> pd.DataFrame:
        groupByType = groupObj.groupByType(summary)
        profitsBy30Min,losesBy30Min = groupObj.groupByTime(summary)
        return groupByType,profitsBy30Min,losesBy30Min

    def export_to_excel(self,export_list: list):
        sheets_names = ['Data','Summary','Type Distribution','Profits By Time','Loses By Time','Splitted Month Summary','Hit By 30 Minutes','Hit By 1 Hour']
        # Output xlsx file name
        writer = pd.ExcelWriter('continuesLiam.xlsx', engine='xlsxwriter')
        i = 0
        for file in export_list:
            file.to_excel(writer,sheet_name= sheets_names[i])
            i += 1
        writer.save()
    def visualize(self):
        visualObj.half_hour_plot()
        visualObj.hour_plot()
        visualObj.sum_of_positions_by_time()
        visualObj.hit_percentage_by_month_plot()
        visualObj.sum_of_positions_by_type()
        visualObj.hit_percentage_by_month_plot()
                


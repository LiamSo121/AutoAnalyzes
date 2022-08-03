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
        summary = summaryObj.fix_problem_dates(summary)
        summary['commision'] = summaryObj.calculate_commision(summary)
        summary = summaryObj.calculate_pl(summary,risk,fund)
        print("Proccess 1 Fix and add daily change - Done:)")

        return summary

    def calc_yearly(self,summary: pd.DataFrame,fund:float) -> pd.DataFrame:
        anuual_summary = monthSumObj.create_df()
        anuual_summary,summaryPerMonth = monthSumObj.calc_monthly(summary,anuual_summary,fund)
        anuual_summary = monthSumObj.calc_annual_sums(anuual_summary,fund)
        # n = number of days to split the month
        n_days_summary = monthSumObj.n_days_distribution(summaryPerMonth,5)
        hit_perc_by_30_minutes = monthSumObj.half_hour_distribution(summaryPerMonth)
        hourly_hit_percentage = monthSumObj.hour_distribution(summaryPerMonth)
        print("Proccess 2 Summarized months and year - Done:)")
        return anuual_summary,n_days_summary,hit_perc_by_30_minutes,hourly_hit_percentage

    def group_by(self,summary: pd.DataFrame) -> pd.DataFrame:
        groupByType = groupObj.groupByType(summary)
        profitsBy30Min,losesBy30Min = groupObj.groupByTime(summary)
        print("Proccess 3 Group by - Done:)")
        return groupByType,profitsBy30Min,losesBy30Min

    def export_to_excel(self,export_list: list,output_file_name: str):
        sheets_names = ['Data','Summary','Type Distribution','Profits By Time','Loses By Time','Splitted Month Summary','Hit By 30 Minutes','Hit By 1 Hour']
        # Output xlsx file name
        writer = pd.ExcelWriter(f'{output_file_name}.xlsx', engine='xlsxwriter')
        i = 0
        for file in export_list:
            file.to_excel(writer,sheet_name= sheets_names[i])
            i += 1
        writer.save()
        print("Proccess 4 Export to excel - Done:)")

    def visualize(self,output_file_name):
        visualObj.half_hour_plot(output_file_name)
        visualObj.hour_plot(output_file_name)
        visualObj.sum_of_positions_by_time(output_file_name)
        visualObj.hit_percentage_by_month_plot(output_file_name)
        visualObj.sum_of_positions_by_type(output_file_name)
        visualObj.hit_percentage_by_month_plot(output_file_name)
        print("Proccess 5  Visualization- Done:)")
                


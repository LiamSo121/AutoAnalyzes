import pandas as pd
import numpy as np
from firstSummary import summaryAutomation
from monthlySummary import monthlySummary
from GroupBy import GroupBy


secondStg = monthlySummary()
firstStg = summaryAutomation()
thirdStg = GroupBy()

class AnalizeHelpers:
    
    def add_daily_change(self,summary: pd.DataFrame,risk:float,fund: float) -> pd.DataFrame:
        summary = firstStg.fix_data(summary)
        summary = firstStg.clean_data(summary)
        summary = firstStg.calculate_pl(summary,risk,fund)
        summary = firstStg.fix_additional_columns(summary)

        return summary

    def calc_yearly(self,summary: pd.DataFrame) -> pd.DataFrame:
        anuual_summary = secondStg.create_df()
        anuual_summary,summaryPerMonth = secondStg.calc_monthly(summary,anuual_summary)
        anuual_summary = secondStg.calc_annual_sums(anuual_summary)
        # n = number of days to split the month
        n_days_summary = secondStg.n_days_distribution(summaryPerMonth,5)
        hit_perc_by_30_minutes = secondStg.half_hour_distribution(summaryPerMonth,5)
        hourly_hit_percentage = secondStg.hour_distribution(summaryPerMonth)
        return anuual_summary,n_days_summary,hit_perc_by_30_minutes,hourly_hit_percentage

    def group_by(self,summary: pd.DataFrame) -> pd.DataFrame:
        groupByType = thirdStg.groupByType(summary)
        profitsBy30Min,losesBy30Min = thirdStg.groupByTime(summary)
        return groupByType,profitsBy30Min,losesBy30Min



    def export_to_excel(self,to_excel_list: pd.DataFrame) -> None:
        sheet_names_list = ['Data','Summary','Type Distribution','Profits By Time','Loses By Time','Splitted Month Summary','Hit By 30 Minutes','Hit By 1 Hour']
        writer = pd.ExcelWriter('continuesLiam.xlsx', engine='xlsxwriter')
        i = 0

        for excel_sheet in to_excel_list:
            excel_sheet.to_excel(writer,sheet_name = sheet_names_list[i])
            i += 1

        writer.save()
        

# change function to fit list of dataframes to export


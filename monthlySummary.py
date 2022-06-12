import pandas as pd
import numpy as np

class monthlySummary:
    def create_df(self) -> pd.DataFrame:
        cols = ['Months','Profit','Lose','Monthly Sum','Positions Number','Profit Pos Number','Lose Pos Number','Hit Percentage','Yield Percantage','Fund']
        monthlySum = pd.DataFrame(columns= cols).set_index('Months') 
        monthlySum.fillna('-',inplace=True)
        return monthlySum


    def calc_monthly(self,summary: pd.DataFrame,monthlySum: pd.DataFrame) -> pd.DataFrame:
        summary['Month'] = pd.DatetimeIndex(summary['date']).month
        months = summary['Month'].unique()
        for month in months:
            monthlyData = summary[summary['Month'] == month]
            nextMonthData = summary[summary['Month'] == month+1]
            monthlyProfits = 0
            monthlyLoses = 0
            for d_change in monthlyData['daily change']:
                if(d_change > 0):
                    monthlyProfits += d_change
                else:
                    monthlyLoses -= d_change
            monthlySum.loc[month,'Profit'] = monthlyProfits
            monthlySum.loc[month,'Lose'] = monthlyLoses
            monthlySum.loc[month,'Monthly Sum'] = monthlyProfits - monthlyLoses
            monthlySum.loc[month,'Profit Pos Number'] = monthlyData[(monthlyData['pl'] == 'P')].shape[0]
            monthlySum.loc[month,'Lose Pos Number'] = monthlyData[(monthlyData['pl'] == 'L')].shape[0]
            monthlySum.loc[month,'Positions Number'] = monthlyData[(monthlyData['pl'] == 'P')].shape[0] + monthlyData[(monthlyData['pl'] == 'L')].shape[0]
            monthlySum.loc[month,'Hit Percentage'] = round((monthlySum.loc[month,'Profit Pos Number'] / monthlySum.loc[month,'Positions Number']) * 100,2)
            startOfMonthFund = monthlyData.loc[monthlyData[monthlyData['present value daily'] !='-'].first_valid_index(),'present value daily']
            if (month != 12):
                endOfMonthFund = nextMonthData.loc[nextMonthData[nextMonthData['present value daily'] != '-'].first_valid_index(),'present value daily']
            else:
                endOfMonthFund = monthlyData.loc[monthlyData[monthlyData['present value daily'] !='-'].last_valid_index(),'present value daily']
            monthlySum.loc[month,'Yield Percantage'] = round(((endOfMonthFund - startOfMonthFund) / startOfMonthFund) * 100,2)
            monthlySum.loc[month,'Fund'] = round(startOfMonthFund,2)
            if (month == 12):
                monthlySum.loc['Annual'] = np.nan
                monthlySum.fillna('-',inplace=True)
                monthlySum.loc['Annual','Fund'] = monthlySum.loc[12,'Fund'] + monthlySum.loc[12,'Monthly Sum']
        summary.drop(columns='Month',inplace=True)
        return monthlySum


    def calc_sums(self,monthlySum: pd.DataFrame) -> pd.DataFrame:
        monthlySum.loc['Annual','Positions Number'] = monthlySum['Positions Number'].drop('Annual',axis=0).sum()
        monthlySum.loc['Annual','Profit'] = monthlySum['Profit'].drop('Annual',axis=0).sum()
        monthlySum.loc['Annual','Lose'] = monthlySum['Lose'].drop('Annual',axis=0).sum()
        monthlySum.loc['Annual','Monthly Sum'] = monthlySum['Monthly Sum'].drop('Annual',axis=0).sum()
        monthlySum.loc['Annual','Profit Pos Number'] = monthlySum['Profit Pos Number'].drop('Annual',axis=0).sum()
        monthlySum.loc['Annual','Lose Pos Number'] = monthlySum['Lose Pos Number'].drop('Annual',axis=0).sum()
        monthlySum.loc['Annual','Hit Percentage'] = round((monthlySum.loc['Annual','Profit Pos Number'] / monthlySum.loc['Annual','Positions Number']) * 100,2)
        monthlySum.loc['Annual','Yield Percantage'] = monthlySum['Yield Percantage'].drop('Annual',axis=0).sum()
        
        

        return monthlySum













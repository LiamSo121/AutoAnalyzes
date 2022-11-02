from operator import index
from matplotlib.pyplot import axis
import pandas as pd
import numpy as np
from datetime import datetime,timedelta,time
from helpers.Assistant import Assistant



assist = Assistant()
class summaryAutomation:
    
    def fix_data(self,summary) -> pd.DataFrame:
        summary['real_pl'] = np.nan
        summary['commision'] = np.nan
        summary['new_quantity'] = np.nan
        summary['Neto'] = np.nan
        summary.fillna('-',inplace=True)
        return summary


    def clean_data(self,summary: pd.DataFrame) -> pd.DataFrame:
        summary.drop(['bp_filled_price','bp_filled_at','stop_at','created_at','pl_amount','highest','lowest','pl_filled_price'],axis=1,inplace=True)
        summary = summary[summary['pl'] != 'C'].reset_index(drop=True)
        return summary

    def take_out_stocks_under_X_hit_percent(self,summary:pd.DataFrame) -> pd.DataFrame:
        symbols_list = ['TSLA', 'BYND', 'BA', 'UAL', 'CCL', 'DAL', 'SPCE', 'AAL', 'NCLH', 'WDC', 'MRNA', 'ENPH', 'ROKU', 'NKLA', 'WYNN', 'ZM', 'CZR', 'MU', 'MAR', 'AMD', 'SAVE', 'SPG', 'INO', 'UBER', 'OSTK', 'CGC', 'WKHS', 'VLO', 'MGM', 'PDD', 'LYFT', 'CAR', 'BILI', 'PLAY', 'SQ', 'SPR', 'C', 'META', 'BIDU', 'PARA', 'JPM', 'PYPL', 'PAAS', 'CRWD', 'IQ', 'FANG', 'QCOM', 'LUV', 'MCHP', 'MRVL', 'DFS', 'JWN', 'FITB', 'BABA', 'BLNK', 'TXN', 'BE', 'BNTX', 'TDOC', 'ETSY', 'DIS', 'ACB', 'AIG', 'ON', 'TCOM', 'GE', 'CAT', 'TWTR', 'JMIA', 'COP', 'GM', 'OKE', 'SNAP', 'GOLD', 'ATVI', 'APA', 'XPEV', 'PRU', 'PINS', 'PLUG', 'EBAY', 'CHPT', 'LAZR', 'EOG', 'GS', 'SYF', 'RIDE', 'MSFT', 'NKE', 'CNK', 'AXP', 'DDOG', 'FDX', 'DOCU', 'SRNE', 'BBY', 'MS', 'X', 'TFC', 'RKT', 'CODX', 'GRWG', 'SPWR', 'APPS', 'PLTR', 'UNH', 'QS', 'CRM', 'SCHW', 'FSR', 'BUD', 'USFD', 'SWKS', 'KEY', 'BBWI', 'CRON', 'PEP', 'BLDP', 'FTNT', 'MDT', 'MOMO', 'CFG', 'DBX', 'WBA', 'ADBE', 'TTD', 'ALLY', 'MTCH', 'PK', 'SU', 'AG', 'FUBO', 'BBBY', 'EXC', 'SIX', 'V', 'FAST', 'WELL', 'MET', 'MUR', 'HOG', 'CARR', 'SHOP', 'TWLO', 'CPRI', 'AMGN', 'VXRT', 'PBF', 'MCD', 'PFE', 'EPD', 'FL', 'NHWK', 'EAT', 'RAD', 'KIM', 'APT', 'CPE', 'WMB', 'VIPS', 'NET', 'SNOW', 'MMM', 'ORCL', 'KODK', 'AVGO', 'STNE', 'HD', 'MNST', 'WB', 'TNXP', 'WY', 'AYTU', 'HST', 'VTR', 'ADI', 'AZN', 'NFLX', 'PNC', 'BSX', 'CIT', 'CNQ', 'BLMN', 'TEVA', 'KR', 'NTNX', 'TER', 'FISV', 'PM', 'EA', 'LEN', 'DHI', 'TRGP', 'UPS', 'VLDR', 'LYV', 'PPBT', 'TLRY', 'ZI', 'KSS', 'MGNI', 'VOD', 'PCG', 'TAL', 'ACN', 'DISCA', 'DLTR', 'SFIX', 'IP', 'LMND', 'MNDT', 'XL', 'GFI', 'HON', 'HPQ', 'MP', 'CVS', 'GPS', 'HA', 'KMI', 'SPLK', 'CHGG', 'TTE', 'LLY', 'UNP', 'OVV', 'CAH', 'QLGN', 'TTNP', 'VFC', 'SIG', 'AI', 'DRI', 'PACB', 'NWL', 'RMO', 'CLVS', 'TRIP', 'ARCC', 'SDC', 'Z', 'UPWK', 'EL', 'FTV', 'SWBI', 'CUK', 'HOLX', 'ATNM', 'EMR', 'LITE', 'TSN', 'KBH', 'NTAP', 'EXEL', 'MOS', 'CMA', 'GRPN', 'LRCX', 'NNVC', 'URBN', 'FCEL', 'YUMC', 'GSK', 'IGT', 'LTHM', 'AVPT', 'SAP', 'SRRK', 'DHR', 'BHC', 'TME', 'ARCT', 'BEKE', 'LAKE', 'MRK', 'TTCF', 'FUV', 'M', 'TGT', 'DM', 'GDRX', 'OMC', 'SO', 'FLR', 'WRK', 'ABNB', 'CTSH', 'DE', 'GOOS', 'BMY', 'CIEN', 'DLR', 'UNFI', 'CNX', 'COTY', 'DKS', 'COF', 'LULU', 'SUMO', 'TXRH', 'WIMI', 'APDN', 'COUP', 'EGHT', 'HBAN', 'APPN', 'BJ', 'DASH', 'EW', 'GOEV', 'MAC', 'TOL', 'BIOL', 'FIVE', 'HUYA', 'MCRB', 'MO', 'APTV', 'CROX', 'FLEX', 'AKAM', 'NKTR', 'SAVA', 'ANF', 'AXSM', 'CPB', 'CRSR', 'CSCO', 'EXPE', 'KL', 'SBUX', 'SSRM', 'WMT', 'BWA', 'ASAN', 'JNPR', 'PAYX', 'CNC', 'KMB', 'MAXR', 'MT', 'TPX', 'VMW', 'AMTD', 'CSIQ', 'LRN', 'OHI', 'SSNC', 'SY', 'TANH', 'TSM', 'YUM', 'BIOC', 'DT', 'KPTI', 'NOV', 'PH', 'RPRX', 'ADAP', 'ADM', 'BKR', 'BXMT', 'CB', 'EQH', 'ERIC', 'GP', 'HDB', 'INPX', 'MPC', 'NSC', 'SGMO', 'SNDX', 'COMM', 'CORT', 'BZUN', 'EPR', 'HPE', 'KMX', 'MAT', 'MGNX', 'MYOV', 'PAGS', 'SBSW', 'SLB', 'ACAD', 'ATI', 'BAC', 'BTBT', 'CGNX', 'CHX', 'CVX', 'LNW', 'NIO', 'PBYI', 'RH', 'SEAS', 'TOPS', 'W', 'WTW', 'APRN', 'AVGR', 'FROG', 'GBT', 'MRTX', 'STX', 'SVC', 'ZION', 'ADS', 'APLS', 'BTWN', 'CPRT', 'EVFM', 'HRB', 'JBLU', 'KO', 'LUMN', 'MITT', 'NG', 'SDGR', 'TPR', 'ZEN', 'CLSK', 'EDIT', 'FAMI', 'KEYS', 'LJPC', 'MTC', 'MULN', 'VVPR', 'ADSK', 'ARWR', 'AVEO', 'CHEF', 'CHNG', 'CRDF', 'CRSP', 'DELL', 'EQT', 'FLDM', 'IMMR', 'IMRN', 'LAB', 'LOGI', 'MESO', 'NUWE', 'NVVE', 'PANW', 'PBR', 'PTON', 'RAPT', 'REAL', 'SEDG', 'STZ', 'T', 'TEN', 'UAA', 'ULTA', 'VIAV', 'WISH', 'WORX', 'CDE', 'CLF', 'DBI', 'DFFN', 'DNB', 'FOLD', 'GNTX', 'HALO', 'HCA', 'INMD', 'OMER', 'OSUR', 'SOL', 'SSL', 'ZTO', 'ANGI', 'BOX', 'DVAX', 'FTCH', 'FUTU', 'KDP', 'MRNS', 'NWSA', 'OPEN', 'PEAK', 'PSTG', 'STM', 'VALE']

        summary = summary[summary['symbol'].isin(symbols_list)]
        return summary



    
    
    def calculate_pl(self,summary: pd.DataFrame,risk: float, fund: float) -> pd.DataFrame:
        i = 0
        dates = summary['date'].unique()
        daily_risk = assist.calculate_risk(fund,risk)
        for date in dates:
            daily_df = summary[summary['date'] == date]
            for index,row in daily_df.iterrows():
                position_attributes = [daily_risk,row['action'],row['buy_point'],row['take_profit'],row['stop_loss']]
                summary.loc[i,'risk'] = daily_risk
                summary.loc[i,'new_quantity'] = assist.calculate_quantity(position_attributes)
                summary.loc[i,'commision'] = assist.calculate_commision(summary.loc[i,'new_quantity'])
                if row['pl'] == 'P' and row['action'] == 'BUY':
                    summary.loc[i,'real_pl'] = round(summary.loc[i,'new_quantity'] * (summary.loc[i,'take_profit'] - summary.loc[i,'buy_point']),2)
                elif row['pl'] == 'P' and row['action'] == 'SELL':
                    summary.loc[i,'real_pl'] = round(summary.loc[i,'new_quantity']  * (summary.loc[i,'buy_point'] - summary.loc[i,'take_profit']),2)
                elif row['pl'] == 'L' and row['action'] == 'BUY':
                    summary.loc[i,'real_pl'] =  round(-1 * (summary.loc[i,'new_quantity'] * (summary.loc[i,'buy_point'] - summary.loc[i,'stop_loss'])),2)
                elif row['pl'] == 'L' and row['action'] == 'SELL':
                    summary.loc[i,'real_pl'] = round(-1 * (summary.loc[i,'new_quantity'] * (summary.loc[i,'stop_loss'] - summary.loc[i,'buy_point'])),2)
                summary.loc[i,'Neto'] = summary.loc[i,'real_pl'] - summary.loc[i,'commision']
                i += 1
            fund += summary[summary['date'] == date]['Neto'].sum()
            rowNumber = summary[summary['date'] == date].index[-1]
            summary.loc[rowNumber,'present value daily'] = round(fund,2)
            daily_risk = assist.calculate_risk(summary.loc[rowNumber,'present value daily'],risk)
        return summary
    
    def calculate_pl_after_commision(self,summary: pd.DataFrame):
        pl_array = np.array(summary['Real_pl'])
        commision_array = np.array(summary['commision'])
        neto_pl = pl_array - commision_array
        return neto_pl

  
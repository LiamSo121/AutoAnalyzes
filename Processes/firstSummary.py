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
        symbols_list = ['TSLA', 'BYND', 'UAL', 'BA', 'ROKU', 'CGC', 'MU', 'AMD', 'DAL', 'CCL', 'WDC', 'SPCE', 'AAL', 'NCLH', 'MRNA', 'ENPH', 'NKLA', 'WYNN', 'SQ', 'ZM', 'PDD', 'CZR', 'OSTK', 'TLRY', 'MAR', 'BIDU', 'SAVE', 'SPG', 'INO', 'BABA', 'UBER', 'CAR', 'WKHS', 'PYPL', 'VLO', 'MGM', 'LYFT', 'BILI', 'PLAY', 'QCOM', 'SPR', 'C', 'META', 'PARA', 'JPM', 'CAT', 'ACB', 'LUV', 'CRON', 'PAAS', 'CRWD', 'ATVI', 'IQ', 'MOMO', 'FANG', 'FITB', 'TWTR', 'MCHP', 'GE', 'ETSY', 'MRVL', 'DFS', 'JWN', 'NVDA', 'BLNK', 'TXN', 'BE', 'BNTX', 'TDOC', 'DIS', 'AIG', 'ON', 'TCOM', 'EBAY', 'JMIA', 'COP', 'GM', 'OKE', 'SNAP', 'GOLD', 'APA', 'XPEV', 'PRU', 'CRM', 'PINS', 'NFLX', 'PLUG', 'UNH', 'CHPT', 'LAZR', 'EOG', 'GS', 'SYF', 'RIDE', 'MSFT', 'NKE', 'CNK', 'DOCU', 'FDX', 'AXP', 'DDOG', 'MS', 'WB', 'SWKS', 'SRNE', 'BBY', 'WBA', 'X', 'TFC', 'RKT', 'CODX', 'GRWG', 'SPWR', 'APPS', 'PLTR', 'FAST', 'QS', 'BBWI', 'LRCX', 'MDT', 'SCHW', 'FSR', 'FTNT', 'BUD', 'USFD', 'KEY', 'PEP', 'MTCH', 'PCG', 'BLDP', 'CFG', 'DBX',
        'ADBE', 'TTD', 'ALLY', 'PK', 'HUYA', 'SU', 'TAL', 'AG', 'FUBO', 'BBBY', 'EXC', 'SIX', 'V', 'MMM', 'WELL', 'MET', 'MUR', 'AMAT', 'HOG', 'CARR', 'SHOP', 'TWLO', 'CPRI', 'NTAP', 'AMGN', 'VXRT', 'VIPS', 'PBF', 'EA', 'NTNX', 'MCD', 'CPE', 'PFE', 'RAD', 'EPD', 'NXPI', 'FL', 'NHWK', 'EAT', 'KIM', 'MNST', 'APT', 'DLTR', 'WMB', 'SIG', 'NET', 'SNOW', 'ORCL', 'KODK', 'AVGO', 'MNDT', 'STNE', 'HD', 'BSX', 'TNXP', 'WY', 'AYTU', 'HST', 'VTR', 'AAPL', 'ADI', 'AZN', 'PNC', 'TRIP', 'CIT', 'CNQ', 'LULU', 'BLMN', 'ACN', 'TEVA', 'KR', 'UNP', 'LITE', 'TER', 'SPLK', 'FISV', 'PM', 'LEN', 'DHI', 'CVS', 'SBUX', 'TRGP', 'UPS', 'VLDR', 'INTC', 'LYV', 'PPBT', 'CLVS', 'VFC', 'BMY', 'ZI', 'NKTR', 'KSS', 'BHC', 'MGNI', 'VOD', 'HPQ', 'DISCA', 'SFIX', 'IP', 'LMND', 'XL', 'GFI', 'HON', 'Z', 'MP', 'CMCSA', 'GPS', 'HA', 'KMI', 'CHGG', 'TSN', 'TTE', 'TTWO', 'LLY', 'MRK', 'M', 'CSCO', 'OVV', 'CAH', 'QLGN', 'TTNP', 'AI', 'DRI', 'PACB', 'GSK', 'NWL', 'RMO', 'ARCC', 'SDC', 'ACAD', 'TOL', 'UPWK', 'WMT', 'EL', 'FTV', 'SWBI', 'CUK', 'HOLX', 'ATNM', 'EMR', 'EXAS', 'KBH', 'EXEL', 'MOS', 'CMA', 'GRPN', 'NNVC', 'URBN', 'FCEL', 'YUMC', 'HAL', 'IGT', 'LTHM', 'AVPT', 'SAP', 'SRRK', 'TSM', 'DHR', 'RH', 'ACHC', 'AMTD', 'TME', 'ARCT', 'BEKE', 'LAKE', 'TTCF', 'FUV', 'LOW', 'TGT', 'ABBV', 'DM', 'XOM', 'CGNX', 'FSLR', 'GDRX', 'IBM', 'OMC', 'SO', 'FLR', 'WRK', 'ABNB', 'CSX', 'ADSK', 'CPB', 'CTSH', 'DE', 'GOOGL', 'GOOS', 'CIEN', 'DLR', 'COMM', 'UNFI', 'BOX', 'TNDM', 'CNX', 'COTY', 'DKS', 'COF', 'GILD', 'JNJ', 'SUMO', 'TXRH', 'UAA', 'WIMI',
        'APDN', 'COUP', 'EGHT', 'HBAN', 'SGMO', 'WFC', 'APPN', 'BJ', 'DASH', 'EW', 'GOEV', 'MAC', 'ROST', 'BIOL', 'FIVE', 'HLT', 'MCRB', 'MO', 'APTV', 'CROX', 'FLEX', 'AKAM', 'CDNS', 'SAVA', 'TPR', 'ANF', 'AXSM', 'BAC', 'CRSR', 'EXPE', 'KL', 'SIOX', 'SSRM', 'XPO', 'BWA', 'ASAN', 'JNPR', 'PAGS', 'PAYX', 'CNC', 'KMB', 'MAXR', 'MT', 'TPX', 'VMW', 'CSIQ', 'LRN', 'OHI', 'PDCO', 'SSNC', 'SY', 'TANH', 'VKTX', 'YUM', 'BIOC', 'CAG', 'CBOE', 'DT', 'KPTI', 'NOV', 'PH', 'RPRX', 'T', 'ADAP', 'ADM', 'BKR', 'BXMT', 'CB', 'EQH', 'ERIC', 'GOOG', 'GP', 'HDB', 'INPX',
        'MPC', 'NSC', 'SNDX', 'CORT', 'IRBT', 'BZUN', 'CENX', 'CLSD', 'DBI', 'EPR', 'ESPR', 'FCX', 'HPE', 'KMX', 'MAT', 'MGNX', 'MYOV', 'OMER', 'SBSW', 'SLB', 'WEN', 'ATI', 'BTBT', 'CHX', 'CVX', 'LNW', 'MLCO', 'MYSZ', 'NIO', 'PBYI', 'SEAS', 'TOPS', 'W', 'WTW', 'APRN', 'AVGR', 'FROG', 'GBT', 'MRTX', 'STX', 'SVC', 'ZION', 'ADS', 'AFL', 'APLS', 'BALL', 'BTWN', 'CPRT', 'CRUS', 'EVFM', 'HRB', 'JBLU', 'KO', 'LUMN', 'MITT', 'NG', 'PBR.A', 'RCII', 'SDGR', 'TJX', 'ZEN', 'CLSK', 'EDIT', 'FAMI', 'GLW', 'KEYS', 'LJPC', 'MTC', 'MULN', 'PGEN', 'VVPR', 'YY', 'ARNA', 'ARWR', 'AVEO', 'AXON', 'BLL', 'CHEF', 'CHNG', 'CRDF', 'CRSP', 'DELL', 'EQT', 'FLDM', 'GDS', 'HEAR', 'IMMR', 'IMRN', 'LAB', 'LKQ', 'LOGI', 'MESO', 'NUWE', 'NVVE', 'PANW', 'PBR', 'PTON', 'RAPT', 'REAL', 'SEDG', 'SLCA', 'STZ', 'TEN', 'UCTT', 'ULTA', 'VIAV', 'WISH', 'WORX', 'CDE', 'CLF', 'DB', 'DFFN', 'DNB', 'ENB', 'FOLD', 'FTCH', 'GNTX', 'HALO', 'HCA', 'IIVI', 'INMD', 'OSUR', 'QD', 'RUN', 'SHEL', 'SOL', 'SPOT', 'SSL', 'ZTO', 'ANGI', 'BB', 'DVAX', 'FUTU', 'KDP', 'MRNS', 'NVAX', 'NWSA', 'OPEN', 'PEAK', 'PSTG', 'PTEN', 'SFM', 'SNES', 'STM', 'VALE'] 

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

  
import matplotlib.pyplot as plt
import seaborn as sns



class Visual:
    def half_hourl_plot(self,export_list):
        half_hour_df = export_list[6]
        print(half_hour_df.loc['Hourly Avg'])
        print(half_hour_df.lov['interval'])

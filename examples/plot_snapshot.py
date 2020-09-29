from pyniviz import main
import datetime
import matplotlib.pyplot as plt

time_of_interest = datetime.datetime(year=2020,month=2,day=11,hour=7)

# Get a list of dataframes where each dataframe represents
# the snowpack at a given point (snapshot) in time.

list_of_snapshots = main.read_pro('sample.pro')

for index, snapshot in enumerate(list_of_snapshots):
    date = snapshot['dates'].iloc[0]

    if date == time_of_interest:
        df_to_plot = snapshot


fig, axs = plt.subplots(nrows=1,ncols=2, figsize = (6,3))

axs[0].plot(df_to_plot['element temperature (degC)'],
         df_to_plot['height [> 0: top, < 0: bottom of elem.] (cm)'])
axs[0].set_ylabel('Height (cm)')
axs[0].set_xlabel(r'Snow Temperature ($\degree$ C)')

axs[0].annotate(datetime.datetime.strftime(time_of_interest, '%d/%m/%Y %H:%M'),
             xy=(-0.2,1.1), xycoords='axes fraction', fontsize = 'large')


axs[1].plot(df_to_plot['grain size (mm)'],
         df_to_plot['height [> 0: top, < 0: bottom of elem.] (cm)'])
axs[1].set_ylabel('Height (cm)')
axs[1].set_xlabel('grain size (mm)')

plt.savefig('snapshot', dpi=500, bbox_inches='tight')
plt.show()
import sys
sys.path.append('..')
from pyniviz import main
import datetime
import matplotlib.pyplot as plt

# Get a list of dataframes where each dataframe represents
# the snowpack at a given point (snapshot) in time.

list_of_snapshots = main.read_pro('sample.pro')

for index, snapshot in enumerate(list_of_snapshots):
    date = snapshot['dates'].iloc[0]

    if date == datetime.datetime(year=2020,month=2,day=11,hour=7):
        df_to_plot = snapshot



plt.plot(df_to_plot['element temperature (degC)'],
         df_to_plot['height [> 0: top, < 0: bottom of elem.] (cm)'])
plt.ylabel('Height (cm)')
plt.xlabel('Snow Temperature (deg C)')
plt.show()

plt.plot(df_to_plot['grain size (mm)'],
         df_to_plot['height [> 0: top, < 0: bottom of elem.] (cm)'])
plt.ylabel('Height (cm)')
plt.xlabel('grain size (mm)')
plt.show()
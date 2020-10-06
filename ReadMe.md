# pyniviz

pyniviz is a Python tool for analysing and visualising the .pro output of the SNOWPACK model.

[![PyPI version](https://badge.fury.io/py/pyniviz.svg)](https://badge.fury.io/py/pyniviz)   [![Build Status](https://travis-ci.org/robbiemallett/pyniviz.svg?branch=master)](https://travis-ci.org/robbiemallett/pyniviz) [![DOI](https://zenodo.org/badge/298647350.svg)](https://zenodo.org/badge/latestdoi/298647350)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pyniviz.

```bash
pip install pyniviz
```
## Documentation & Walkthrough Video

You can find full documentation for pyniviz [here](https://pyniviz.readthedocs.io/en/latest/) and a walkthrough video [here](https://www.youtube.com/watch?v=WXEUVK0xgfY).

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
This project has a highly permissive [MIT licence](https://github.com/robbiemallett/pyniviz/blob/master/LICENCE.txt). However I'd really appreciate it if you could let me know about any published plots made with this code so I can get some feedback on this project.

## Basic Usage for a continuous variable

Here we plot the output of a sample .pro file that comes packaged with pyniviz. Rather than plotting the whole thing, we can choose to plot it between two points in time (start_date and end_date). Furthermore, we choose to just plot part of the snowpack between 400 and 415 cm. Finally, we'd like the y index to start at zero, so we specify yax_shift to subract our baseline height of 400 from the tick labels. We've chosen a color scheme of 'Reds', but could equally have used something like 'plasma'.

```python
from pyniviz import main
import datetime


start_date = datetime.datetime(year=2020,
                               month=1,
                               day=29)
end_date = datetime.datetime(year=2020,
                             month=2,
                             day=8)


main.plot_pro('sample.pro',
                 variable= 'element temperature (degC)', # Could also just be 'temperature'
                 ymin=400,
                 ymax=415,
                 xmin=start_date,
                 xmax=end_date,
                 c_scheme='Reds',
                 yax_shift=400)
```
<img src="https://github.com/robbiemallett/pyniviz/blob/master/examples/temp_fig.png" width="400" height="250">

## Grain type plot

Here we plot the grain types. The code detects this from the ```variable``` keyword and ignores anything passed to c_scheme. 

```python
main.plot_pro('sample.pro',
                 variable= 'grain type (Swiss Code F1F2F3)', # Could also just be 'grain type'
                 ymin=400,
                 ymax=415,
                 xmin=start_date,
                 xmax=end_date,
                 yax_shift=400)
                 
```
<img src="https://github.com/robbiemallett/pyniviz/blob/master/examples/gt_fig.png" width="500" height="250">

## Advanced Usage: Looking at a snapshot of the snowpack

We can also use the pyniviz tools package to investigate the snowpack at certain points in time. Under the hood pyniviz stores the information contained in the .pro file as a pandas dataframe for every timestep. To get a list of these dataframes you can call ```main.read_pro()```. The time that each dataframe represents is stored in the dataframes under the 'dates' column. So to get the DataFrame corresponding to the time you want you must iterate through them all, check a value in their 'dates' column and assign the dataframe of interest to a variable. Once you've selected the DataFrame you want, you can simply plot the variables.

```python

# Specify your time of interest

time_of_interest = datetime.datetime(year=2020,month=2,day=11,hour=7)

# Get a list of dataframes where each dataframe represents
# the snowpack at a given point (snapshot) in time.

list_of_snapshots = main.read_pro('sample.pro')

# Iterate through these dataframes to get the one corresponding to the time of interest

for index, snapshot in enumerate(list_of_snapshots):
    date = snapshot['dates'].iloc[0]

    if date == time_of_interest:
        df_to_plot = snapshot 

# Plotting code

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

```
<img src="https://github.com/robbiemallett/pyniviz/blob/master/examples/snapshot.png" width="500" height="250">


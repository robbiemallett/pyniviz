# pyniviz

pyniviz is a Python tool for visualising the output of the SNOWPACK model 

[![PyPI version](https://badge.fury.io/py/pyniviz.svg)](https://badge.fury.io/py/pyniviz)   [![Build Status](https://travis-ci.org/robbiemallett/pyniviz.svg?branch=master)](https://travis-ci.org/robbiemallett/pyniviz)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pyniviz.

```bash
pip install pyniviz
```
## Documentation

You can find full documentation for pyniviz [here](https://pyniviz.readthedocs.io/en/latest/).

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
![T](https://github.com/robbiemallett/pyniviz/blob/master/examples/temp_fig.png | width=100)

## Grain type plot

```python
main.plot_pro('sample.pro',
                 variable= 'grain type (Swiss Code F1F2F3)', # Could also just be 'grain type'
                 ymin=400,
                 ymax=415,
                 xmin=start_date,
                 xmax=end_date,
                 yax_shift=400)
                 
                 ```

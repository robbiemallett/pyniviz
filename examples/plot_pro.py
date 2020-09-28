import sys
sys.path.append('..')
from pyniviz import main
import datetime


start_date = datetime.datetime(year=2020,
                               month=1,
                               day=29)
end_date = datetime.datetime(year=2020,
                             month=2,
                             day=8)


main.plot_pro('sample.pro',
                 variable= 'element temperature (degC)',
                 ymin=400,
                 ymax=415,
                 xmin=start_date,
                 xmax=end_date,
                 c_scheme='Reds',
                 yax_shift=400)
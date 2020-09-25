
from tools import read_pro
from tools import create_grid
from tools import plot_grid, variable_shortenings
import datetime


def plot_pro(path,
             variable,
             vmin=None,
             vmax=None,
             xmin=None,
             xmax=None,
             ymin=None,
             ymax=None,
             file_name=None,
             c_scheme='plasma_r',
             yax_shift=0):

    variable = variable_shortenings(variable)

    spl = read_pro(path,variable)

    info  = create_grid(spl,
                         variable,
                         xmin,
                         xmax,
                         ymin,
                         ymax)

    plot_grid(info,
                 variable,
                 vmin,
                 vmax,
                 xmin,
                 xmax,
                 ymin,
                 ymax,
                 file_name,
                 c_scheme,
                 yax_shift)

# SAMPLE VARIABLES

# 'element density (kg m-3)',
# 'element temperature (degC)',
# 'liquid water content by volume (%)',
# 'grain size (mm)',
# 'grain type (Swiss Code F1F2F3)',
# 'ice volume fraction (%)',
# 'air volume fraction (%)',
# 'optical equivalent grain size (mm)',
# 'bulk salinity (g/kg)',
# 'brine salinity (g/kg)',
# 'thickness_m',

if __name__ == "__main__":

    start_date = datetime.datetime(year=2020,
                                   month=1,
                                   day=29)
    end_date = datetime.datetime(year=2020,
                                 month=2,
                                 day=8)


    plot_pro('/home/robbie/Dropbox/SERF/Rosie/SERF_SERF_experiment.pro',
         variable= 'temperature',
             ymin=400,
             ymax=415,
             xmin=start_date,
             xmax=end_date,
             c_scheme='Blues',
             yax_shift=400)
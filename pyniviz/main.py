
from pyniviz.tools import read_pro, create_grid, plot_grid, variable_shortenings, read_smet
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

    """

    Args:
        path (str): String pointing to the location of the .PRO file to be read
        variable (str): Variable to plot, can be a .pro recognised code or a niviz approved shortening
        vmin (float): optional, min value for the colorbar
        vmax (float): optional, max value for the colorbar
        xmin (datetime.datetime): optional, represents time from which data appears on the plot
        xmax (datetime.datetime): optional, represents time to which data appears on the plot
        ymin (float): optional, represents min height to which data appears on the plot
        ymax (float): optional, represents max height to which data appears on the plot
        file_name (str): optional, if present represents where the image should be saved
        c_scheme (str): optional, represents the scheme of the colorbar e.g. 'plasma', 'Blues'.
        yax_shift (float): optional, shifts the y axis ticks down a bit (useful if shifted to a ref value , e.g. 400cm)

    Returns:

    """

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

def plot_smet(path, var): 

    df = read_smet(path, var)

    df.plot()

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
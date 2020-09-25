import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from math import floor, ceil
from scipy import interpolate
import math
from matplotlib.colors import LinearSegmentedColormap

def variable_shortenings(code):

    """Converts a list of recognised codes to the required variable string, or takes the strings themselves"""

    shortenings = {'density':'element density (kg m-3)',
                    'temperature':'element temperature (degC)',
                    'lwc':'liquid water content by volume (%)',
                    'grain size':'grain size (mm)',
                    'grain type':'grain type (Swiss Code F1F2F3)',
                    'ivf':'ice volume fraction (%)',
                    'avf':'air volume fraction (%)',
                    'd_opt':'optical equivalent grain size (mm)',
                    'bulk_sal':'bulk salinity (g/kg)',
                    'brine_sal':'brine salinity (g/kg)',
                    'thickness':'thickness_m'}

    if code.lower() in shortenings.keys():
        return(shortenings[code])
    elif code in shortenings.items():
        return(code)
    else:
        print(f'Variable not recognised, must be from the following {list(zip(shortenings.keys(), shortenings.items()))}')
        raise


def grain_type_colormap():
    colors = [('lime'),  # 1, precipitation particles
              ('green'),  # 2, Decomposing fragmented PP
              ('yellow'),  # 3 Rounded Grains (RG)
              ('orange'),  # 4 Faceted Crystals
              ('blue'),  # 5 Depth Hoar
              ('gray'),  # 6 Surface Hoar
              ('red'),  # 7 Melt FOrms
              ('cyan'),  # 8 Ice formations
              ('black'),  # 9 Rounded faceted particles
              ]


    cmap_name = 'grain_type_map'

    my_cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=9)

    return(my_cmap)

def get_grain_tick_labels():

    grain_tick_labels = ['Precipitation particles',
                         'Decomposing fragmented PP',
                         'Rounded Grains',
                         'Faceted Crystals',
                         'Depth Hoar',
                         'Surface Hoar',
                         'Melt Forms',
                         'Ice',
                         'Rounded faceted particles']

    return(grain_tick_labels)

##############################################################################################

def vectorized_rounder():
    def f(num):
        if np.isnan(num):
            return np.nan
        else:
            return num // 10 ** (int(math.log(num, 10)))

    vf = np.vectorize(f)

    return(vf)

def transform_grid_for_grain_type(grid):

    vf = vectorized_rounder()

    grid = vf(grid)
    grid = grid / 10
    grid[0, 0] = 0.05
    grid[0, 1] = 0.95
    return(grid)


def create_grid(spl,
                 var_to_plot,
                 xmin,
                 xmax,
                 ymin,
                 ymax):

    # Find the lowest and the highest heights to calibrate the ylims

    max_heights, min_heights, dates = [], [], []
    for df in spl:
        max_heights.append(df['height [> 0: top, < 0: bottom of elem.] (cm)'].iloc[-1])
        min_heights.append(df['height [> 0: top, < 0: bottom of elem.] (cm)'].iloc[0])
        dates.append(df['dates'].iloc[0])

    if ymin and ymax:
        max_height = ymax
        min_height = ymin
    else:
        max_height = np.max(max_heights)
        min_height = np.min(min_heights)
        max_height = round(max_height ,5 ,'up')
        min_height = round(min_height ,5 ,'down')

    grid_resolution = 100
    vertical_grid = np.linspace(min_height ,max_height ,grid_resolution)

    # Trim spl to fit specified xmin, xmax

    if xmin and xmax:

        spl = [sp for (date,sp) in zip(dates,spl) if (xmin < date < xmax)]
        dates = [date for date  in dates if (xmin < date < xmax)]

    grid = np.full((grid_resolution, len(spl)), np.nan)

    for count, df in enumerate(spl):

        heights = np.array(df['height [> 0: top, < 0: bottom of elem.] (cm)'])
        variables = np.array(df[var_to_plot])

        #         regular_variables = np.interp(vertical_grid, heights, variables, left = np.nan, right = np.nan)

        kind = 'nearest'

        my_interp = interpolate.interp1d(heights,
                                         variables,
                                         kind=kind,
                                         bounds_error = False,
                                         fill_value = (np.nan ,np.nan))

        regular_variables = my_interp(vertical_grid)

        grid[: ,count] = np.flip(regular_variables, axis=0)

    return({'grid':grid,
            'max_height':max_height,
            'min_height':min_height,
            'dates':dates})

def plot_grid(information,
                 var_to_plot,
                 vmin,
                 vmax,
                 xmin,
                 xmax,
                 ymin,
                 ymax,
                 file_name,
                 c_scheme,
                 yax_shift=None):

    grain_type = True if "grain type" in var_to_plot else False

    grid = information['grid']
    dates = information['dates']

    # Make the plot

    fig, ax = plt.subplots(1 ,1 ,figsize=(10 ,6))

    # Specify the colormap

    if grain_type:
        my_cmap = grain_type_colormap()
        grid = transform_grid_for_grain_type(grid)
    else:
        my_cmap = plt.get_cmap(c_scheme)


    # Set the limits of the plot

    x_lims = mdates.date2num([dates[0] ,dates[-1]])
    if xmin and xmax:
        x_lims_specified = mdates.date2num([xmin, xmax])
        # for spec in x_lims_specified:
        #     assert (x_lims[0] < spec < x_lims[1])
        x_lims = x_lims_specified

    if ymin and ymax:
        information['min_height'] = ymin
        information['max_height'] = ymax

    extent = [x_lims[0],
              x_lims[1] ,
              information['min_height'] - yax_shift,
              information['max_height'] - yax_shift]

    ax.xaxis_date()
    date_format = mdates.DateFormatter('%m/%d')
    ax.xaxis.set_major_formatter(date_format)

    #######################

    im = ax.imshow(grid,
                   extent= extent,
                   aspect='auto',
                   vmin=vmin ,vmax=vmax,
                   cmap=my_cmap)


    ax.tick_params(right=True)

    cbar = fig.colorbar(im, ax=ax, pad=0.075)

    if grain_type:           cbar.ax.set_yticklabels(get_grain_tick_labels())
    else:                    cbar.set_label(var_to_plot, fontsize='x-large')

    ax.set_ylabel('Height (cm)', fontsize='x-large')
    plt.show()

    if file_name:
        plt.savefig(file_name ,dpi=500)


def round(num, divisor, direction):
    if direction == 'down':
        return floor(num / divisor) * divisor
    elif direction == 'up':
        return ceil(num / divisor) * divisor

def read_pro(path,var_to_plot):

    """ Reads a .PRO file line by line and turns it into a list of python-usable objects (members of snowpro class).

    PRO files are pretty wild - they're indexed by var codes (0500 - 0605) that represent the snowpack variables of
    interest. This model is only interested in some of them, so has a var_codes list to select those (not interested in
    skiier stability index for instance!). Once the pro file is read into memory, for each var_code, the function
    iterates through the text file and extracts the lines beginning with the code. It breaks up the lines (which each
    correspond to a comma-separated, layer-wise list of values), and turns the line into a list.

    #TODO improve this documentation



    Returns:
        list of snowpro objects corresponding to the evolution of a track.

    """

    # Which variables are you interested in?

    var_codes = ['0500','0501',pro_code_dict(var_to_plot,inverse=True)]

    # Set up the dictionary to be returned. Dictionary is organised by variable name.

    code_dict = pro_code_dict(return_all=True)

    variables = {}
    for var in var_codes:
        variables[code_dict[var]] = []

    # Open the .PRO file

    with open(path, "r") as f:

        # Iterate line by line

        for line in f.readlines():

            # If the variable code (first four chars) matches the variable of interest,
            # append that line to the list of lines

            if line[:4] in var_codes:
                    variables[code_dict[line[:4]]].append(line)


    # Now remove the header data

    for variable in variables.keys():

        variables[variable].pop(0)

    snowpro_list = [snowpro_from_snapshot(date_index, variables) for date_index in range(len(variables['Date']))]

    return (snowpro_list)


def pro_code_dict(code=False, inverse=False, return_all=False):
    """Get the name of a variable from its var_code (four character numeric string).

    Alternatively set return_all=True to just return the full code dictionary, from which you can choose

    #TODO this function currently outputs either a string or a dict. Not great.

    Args:
        code: four character string represening a number (e.g. '0502' -> element density)
        return_all: bool, if you just want to return a dictionary of string codes and corresponding variable names.

    Returns:

    """

    pro_code_dict = {"0500": "Date",
                     "0501": "height [> 0: top, < 0: bottom of elem.] (cm)",
                     "0502": "element density (kg m-3)",
                     "0503": "element temperature (degC)",
                     "0504": "element ID (1)",
                     "0506": "liquid water content by volume (%)",
                     "0508": "dendricity (1)",
                     "0509": "sphericity (1)",
                     "0510": "coordination number (1)",
                     "0511": "bond size (mm)",
                     "0512": "grain size (mm)",
                     "0513": "grain type (Swiss Code F1F2F3)",
                     "0514": "grain type, grain size (mm), and density (kg m-3) of SH at surface",
                     "0515": "ice volume fraction (%)",
                     "0516": "air volume fraction (%)",
                     "0517": "stress in (kPa)",
                     "0518": "viscosity (GPa s)",
                     "0519": "soil volume fraction (%)",
                     "0520": "temperature gradient (K m-1)",
                     "0521": "thermal conductivity (W K-1 m-1)",
                     "0522": "absorbed shortwave radiation (W m-2)",
                     "0523": "viscous deformation rate (1.e-6 s-1)",
                     "0531": "deformation rate stability index Sdef",
                     "0532": "natural stability index Sn38",
                     "0533": "stability index Sk38",
                     "0534": "hand hardness either (N) or index steps (1)",
                     "0535": "optical equivalent grain size (mm)",
                     "0540": "bulk salinity (g/kg)",
                     "0541": "brine salinity (g/kg)",
                     "0601": "snow shear strength (kPa)",
                     "0602": "grain size difference (mm)",
                     "0603": "hardness difference (1)",
                     "0604": "ssi",
                     "0605": "inverse texture index ITI (Mg m-4)",
                     "0606": "critical cut length (m)", }

    if inverse:
        inverse = {value: key for key, value in pro_code_dict.items()}
        return(inverse[code])
    if code:
        return (pro_code_dict[code])
    if return_all:
        return (pro_code_dict)


def snowpro_from_snapshot(date_index, variables):
    """ Takes a dictionary of variables (a processed .Pro file) and returns dataframes

    Args:
        date_index: int representing the index (day) that the snowpro object should be generated for
        variables: what variables should be used in the snowpro to describe the snowpack on that day

    Returns:
        single snowpro object representing the state of the snowpack at a point in time.

    """

    dataframe_dict = {}

    for varname in variables.keys():

        if varname == 'Date':

            my_datetime = series_from_line(variables, varname, date_index)

        else:

            dataframe_dict[varname] = series_from_line(variables, varname, date_index)

    df = pd.DataFrame(dataframe_dict)

    h_0 = df['height [> 0: top, < 0: bottom of elem.] (cm)'][0]
    diffheights = [height - h_0 for height in df['height [> 0: top, < 0: bottom of elem.] (cm)']]

    thickness = [-999]
    for i in range(len(diffheights) - 1):
        thickness.append((diffheights[i + 1] - diffheights[i]) / 100)

    df['thickness_m'] = thickness
    df['dates'] = my_datetime

    df = df.iloc[1:].copy()

    return (df)


def series_from_line(variables, varname, index):
    """ Gets a list of values (for a given variable) from a dictionary representing a barey-processed .PRO file.

    Args:
        variables: a dictionary, top level broken down by variable, next level is a dict of strings which each represent
        the state of a snowpack (for that variable) on a given day.
        varname: the variable of interest
        index: the day on which you should retrun the snowpack state for the variable of interest

    Returns:
        list: floats for the variable of interest, unless variable is day in which case it's a list of datetime objects

    """

    # First split the string apart at the commas

    series = variables[varname][index].split(",")

    # Get the variable code (the first entry in the list)

    varcode = int(series[0])

    # Get the number of actual datapoints (the second entry in the list)

    if varcode > 500:

        nvars = int(series[1])

        # Isolate the actual datapoints from the metadata

        datapoints = series[-nvars:]

        # Remove carriage return from the last datapoint if present
        if "\n" in datapoints[-1]:
            datapoints[-1] = datapoints[-1].replace('\n', '')

        # If we're looking at ice type data, we have to remove a weird graupel classification (bug?)
        if varcode == 513:
            return (list(map(float, datapoints[:-1])))

        # Return a list of floats for that variable in the snowpack

        else:
            return (list(map(float, datapoints)))

    else:

        return (datetime.datetime.strptime(series[1][:-1], "%d.%m.%Y %H:%M:%S"))


class snowpro:
    """A combined column of ice and snow with vertical profiles
    and variables such as date, snow height and ice thickness"""

    def __init__(self, iceframe, snowframe, datetime):

        self.iceframe = iceframe
        self.snowframe = snowframe
        self.datetime = datetime
        self.snowdepth = np.sum(snowframe['thickness_m'])
        self.snowdensity = np.mean(snowframe['element density (kg m-3)'])
        self.icethickness = np.sum(iceframe['thickness_m'])

        if snowframe.empty:
            self.sst, self.ist = np.nan, np.nan
        else:
            self.sst = snowframe['element temperature (degC)'].iloc[0]
            self.ist = snowframe['element temperature (degC)'].iloc[-1]

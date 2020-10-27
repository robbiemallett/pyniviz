from pyniviz import main
import matplotlib.pyplot as plt
import matplotlib as mpl

fig = plt.figure(figsize=(10, 10))

# Make a gridspec to line up the figs

widths = [1, 1]
heights = [0.1, 1, 1, 0.1]

gs = fig.add_gridspec(ncols=2, nrows=4, width_ratios=widths, height_ratios=heights)

variables = ['grain size', 'temperature', 'density', 'bulk_sal']
var_names = ['Grain Size (mm)', r'Temperature ($\degree$C)',
             r'Density (kgm$^{-3}$)', 'Bulk Salinity (g/kg)']
subplot_locs = [[1, 0], [1, 1], [2, 0], [2, 1]]

lims_list = [(0,6), (-15,0), (100,500), (0,15)]

subplot_axes = []

for variable, subplot_loc, lims, var_name in zip(variables, subplot_locs, lims_list, var_names):

    print(variable)

    ax_plot = fig.add_subplot(gs[subplot_loc[0], subplot_loc[1]])

    main.plot_pro('/home/robbie/Dropbox/chris_fuller/Resolute_salty.pro',
                  variable=variable,
                  ymin=400,
                  ymax=420,
                  vmin= lims[0],
                  vmax= lims[1],
                  yax_shift=400,
                  subplot=ax_plot,
                  )

    if subplot_loc[0] == 1: cbar_row = 0
    elif subplot_loc[0] == 2: cbar_row = 3

    ax_cbar = fig.add_subplot(gs[cbar_row, subplot_loc[1]])

    norm = mpl.colors.Normalize(vmin=lims[0], vmax=lims[1])

    cbar = mpl.colorbar.ColorbarBase(ax_cbar,
                                     cmap=mpl.cm.plasma,
                                     norm=norm,
                                     orientation='horizontal')

    cbar.set_label(var_name, fontsize='x-large')

    if subplot_loc[0] == 1:
        ax_cbar.xaxis.set_label_position('top')
        ax_cbar.xaxis.set_ticks_position('top')

    if subplot_loc[1] == 1:
        ax_plot.set_ylabel("")

    subplot_axes.append((ax_plot,ax_cbar))




plt.show()
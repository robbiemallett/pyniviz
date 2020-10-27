from pyniviz import main
import matplotlib.pyplot as plt
import matplotlib as mpl


fig = plt.figure(figsize=(10, 5))

# Make a gridspec to line up the figs

widths = [1,1,0.07]
gs = fig.add_gridspec(ncols=3,nrows=1,width_ratios=widths)



ax1 = fig.add_subplot(gs[0,0])
main.plot_pro('/home/robbie/Dropbox/chris_fuller/Resolute_fresh.pro',
                 variable= 'temperature', # Could also just be 'grain type' or 'temperature'
                 ymin=400,
                 ymax=440,
                 vmin=-20,
                 vmax=0,
                 yax_shift=400,
                 subplot=ax1,
             )

ax2 = fig.add_subplot(gs[0,1])
main.plot_pro('/home/robbie/Dropbox/chris_fuller/Resolute_fresh.pro',
                 variable= 'temperature', # Could also just be 'grain type' or 'temperature'
                 ymin=400,
                 ymax=440,
                  vmin=-20,
                  vmax=0,
                 yax_shift=400,
                 subplot=ax2
             )

#
cbax = fig.add_subplot(gs[0,2])

norm = mpl.colors.Normalize(vmin=-20, vmax=0)

cbar = mpl.colorbar.ColorbarBase(cbax,
                                 cmap=mpl.cm.plasma,
                                norm=norm,
                                orientation='vertical')

cbar.set_label(r'Temperature ($\degree$C)', fontsize = 'x-large')


#####################

ax2.set_ylabel("")

plt.show()
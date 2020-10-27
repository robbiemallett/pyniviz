from pyniviz import main

main.plot_pro('/home/robbie/Dropbox/chris_fuller/Resolute_fresh.pro',
                 variable= 'temperature', # Could also just be 'grain type' or 'temperature'
                 ymin=400,
                 ymax=440,
                  vmin=-1,
                  vmax=1,
                 yax_shift=400,
              difference_with='/home/robbie/Dropbox/chris_fuller/Resolute_salty.pro',
             )

main.plot_pro('/home/robbie/Dropbox/chris_fuller/Resolute_fresh.pro',
                 variable= 'density', # Could also just be 'grain type' or 'temperature'
                 ymin=300,
                 ymax=440,
                  vmin=-50,
                  vmax=50,
                 yax_shift=400,
              difference_with='/home/robbie/Dropbox/chris_fuller/Resolute_salty.pro',
             )
import sys
sys.path.append('..')
from pyniviz import main

# Plot 2 m air temperature (TA) time series from sample.smet
main.plot_smet('sample.smet', 'TA')
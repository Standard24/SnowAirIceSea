#!/usr/bin/env python

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.transforms as mtransforms
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

# use latex to draw text on plots (only for pdf...)
from matplotlib import rc
rc('text', usetex=True)
plt.rc('font', family='serif')


# define plot options
def plotOpts(ax):
    ax.tick_params(axis='both', which='both', direction='in', right=True,
                   top=True)

glacier = 'Blekumbreen'
glacier = 'Tellbreen'

if glacier == 'Blekumbreen':
    xfit = np.array([-1.9, 0.1])
    asp = .0027
else:
    xfit = np.array([-3.1, 0.2])
    asp = .0035

# import all csv files: Create a list of pandas data frames
data = pd.read_csv('../data/elevations/' + glacier + '.txt', sep=' ')


print(data)
#import IPython
#IPython.embed()

# plot MBgradient on blekumbreen
f = plt.figure(figsize=(6, 3.5), tight_layout=True)

x =  data['b']
sx = data['sb']
y =  data['elevation']
plt.errorbar(x, y, xerr=sx, fmt='.', ecolor='lightgrey', label='',
        elinewidth=1)
        
plt.gca().set_aspect(asp)

plt.ylabel('Stake elevation [m]')
plt.xlabel('Mass balance [m/a]')


# FIT

xdat = x
ydat = y

def pol_1st(x, a, b):
    return a + x/(b/1000)

popt, pcov = curve_fit(pol_1st, xdat, ydat, p0=[1, 0.1])

plt.axhline(popt[0], linestyle='--', color='lightgrey', linewidth=.5)
plt.axvline(0, linestyle='--', color='lightgrey', linewidth=.5)

sEL = np.sqrt(pcov[0][0])
sMBG= np.sqrt(pcov[1][1])

plt.plot(xfit, pol_1st(xfit, *popt), 'r-', linewidth=1,
      color='tab:red',
      label='Fit with $y=a+x/b$ \n $a=%1.0f \pm %1.0f \,$m, $b=%1.1f \pm %1.1f \, $mm/m' 
      % tuple([popt[0], sEL, popt[1], sMBG]))

plt.legend()


print(popt)
print('Uncert on equilibrium line: ' + str(sEL))
print('Uncert on MBG: ' + str(sMBG))
# plot data


#import IPython
#IPython.embed()


f.savefig('../protocol/figs/Elevation_' + glacier + '_mbg.pdf')

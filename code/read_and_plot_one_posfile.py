#!/usr/bin/env python

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# use latex to draw text on plots (only for pdf...)
from matplotlib import rc
rc('text', usetex=True)
plt.rc('font', family='serif')

from coordinate_transformation2 import from_latlon

staketitle = 'T1-ii-2017'
corr = '' #_STEC or _LC or ''


# read the filename for the stake from textfile

# for STEC data:
#filenames = pd.read_csv('../data/LC-STEC-data.csv',
#                    sep=' ', index_col=0)
                    
# for LC data
filenames = pd.read_csv('../data/fieldbook_data.csv',
                    sep=' ', index_col=0)
                    
                                 
filename = filenames.loc[staketitle, 'filename'] + '_corr' + corr
print('filename: ' + filename)

# read data from pos file
data_imp = pd.read_csv('../data/processed_data/' + filename + '.pos',
                    sep='\s+',
                    comment='%',
                    names=['date', 'time', 'latitude(deg)', 'longitude(deg)',
                    'height(m)', 'Q', 'ns', 'sdn(m)', 'sde(m)', 'sdu(m)',
                    'sdne(m)', 'sdeu(m)', 'sdun(m)', 'age(s)', 'ratio'])

# read coordinates from trimble data for hlines
data_trimble = pd.read_csv('../data/stake_coordinates/2018_stake_coordinates_trimble_post.csv', sep=' ')         

stake = data_trimble.loc[data_trimble['Name'] == staketitle]
northing_tr = stake['Northing'].values[0]
easting_tr = stake['Easting'].values[0]
elevation_tr = stake['Elevation'].values[0]



# read coordinates from open source data for hlines
data_weightedmean = pd.read_csv('../data/stake_coordinates/2018_stake_coordinates_corr' + corr + '.csv', sep=' ')

stake = data_weightedmean.loc[data_weightedmean['Name'] == staketitle]
northing_wm = stake['Northing'].values[0]
easting_wm = stake['Easting'].values[0]
elevation_wm = stake['Elevation'].values[0]

utm = np.array([from_latlon(lat, lon) for lat, lon in zip(data_imp['latitude(deg)'], data_imp['longitude(deg)']) ]).T

#print(np.mean(utm, axis=1))

east = utm[0,:]#+3*np.sin(1/20*(2*np.pi)*np.arange(len(utm[0])))
north = utm[1,:]
height = data_imp['height(m)']
se = data_imp['sde(m)']
sn = data_imp['sdn(m)']
su = data_imp['sdu(m)']

#print(np.std(east))
#print(np.std(north))

f, (ax1, ax2, ax3) = plt.subplots(3, figsize=(11.5,6))

ax1.axhline(easting_tr, color='k', linewidth=.5, linestyle='--')
ax2.axhline(northing_tr, color='k', linewidth=.5, linestyle='--')
ax3.axhline(elevation_tr, color='k', linewidth=.5, linestyle='--')

ax1.axhline(easting_wm, color='k', linewidth=1)
ax2.axhline(northing_wm, color='k', linewidth=1)
ax3.axhline(elevation_wm, color='k', linewidth=1)


paramlist = [(ax1, east, se, 'Easting [m]'),
             (ax2, north, sn, 'Northing [m]'),
             (ax3, height, su, 'Elevation [m]')]
             
for ax, y, s, ylabel in paramlist:

    x=range(len(y))

    ax.errorbar(x, y, yerr=s, fmt='.', markersize=2,
            ecolor='lightgrey', elinewidth=1)
    
    ax.ticklabel_format(useOffset=False)
    ax.set_ylabel(ylabel)
    
    
    # plot moving average
    #for N in [20, 50, 200]:
    #    ax.plot(x[int(N/2-1):-int(N/2)],
    #            np.convolve(y, np.ones((N,))/N, mode='valid'))

ax3.set_xlabel('Time [s]')
   
plt.savefig('../protocol/figs/timeseries/' + filename + '-' + staketitle +  
        '_Timeseries-east-north-elev.pdf')



if __name__ == '__main__':
#    print(fieldbook)
    print(data_imp.describe())

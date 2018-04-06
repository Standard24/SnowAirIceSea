#!/usr/bin/env python

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from coordinate_transformation2 import from_latlon

staketitle = 'BL5-ii-2017'


# read the filename for the stake from textfile
filenames = pd.read_csv('../data/LC-STEC-data.csv',
                    sep=' ', index_col=0)
filename = filenames.loc[staketitle, 'filename'] + '_corr_STEC'
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

northing = stake['Northing'].values[0]
easting = stake['Easting'].values[0]
elevation = stake['Elevation'].values[0]

        
utm = np.array([from_latlon(lat, lon) for lat, lon in zip(data_imp['latitude(deg)'], data_imp['longitude(deg)']) ]).T

#print(np.mean(utm, axis=1))

east = utm[0,:]#+3*np.sin(1/20*(2*np.pi)*np.arange(len(utm[0])))
north = utm[1,:]
height = data_imp['height(m)']

#print(np.std(east))
#print(np.std(north))

f, (ax1, ax2, ax3) = plt.subplots(3, figsize=(11.5,6))

ax1.axhline(easting, color='k')
ax2.axhline(northing, color='k')
ax3.axhline(elevation, color='k')

for ax, y in [(ax1, east), (ax2, north), (ax3, height)]:

    x=range(len(y))

    ax.plot(x, y)
    for N in [20, 50, 200]:
        ax.plot(x[int(N/2-1):-int(N/2)], np.convolve(y, np.ones((N,))/N, mode='valid'))

   
plt.savefig('../fig/timeseries/' + filename + '-' + staketitle +  
        '_Timeseries-east-north-elev.pdf')



if __name__ == '__main__':
#    print(fieldbook)
    print(data_imp.describe())

#!/usr/bin/env python

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from coordinate_transformation2 import from_latlon




filename = '46250701_corr_off'


# read data from all pos files
data_imp = pd.read_csv('../data/processed_data/' + filename + '.pos',
                    sep='\s+',
                    comment='%',
                    names=['date', 'time', 'latitude(deg)', 'longitude(deg)',
                    'height(m)', 'Q', 'ns', 'sdn(m)', 'sde(m)', 'sdu(m)',
                    'sdne(m)', 'sdeu(m)', 'sdun(m)', 'age(s)', 'ratio'])
                    
#data_trimble = pd.read_csv('../data/stake_coordinates/2018_stake_coordinates_trimble_post.csv',
#                    sep='\s',
#                    names=['Name' 'Northing' 'Easting' 'Elevation'])                    
#           
#print(data_trimble['T1-i-2017'])

# calculate mean values of columns
#mean_values = [stake[stake['Q'] == 2].mean() for stake in data_imp]


        
utm = np.array([from_latlon(lat, lon) for lat, lon in zip(data_imp['latitude(deg)'], data_imp['longitude(deg)']) ]).T

print(np.mean(utm, axis=1))

east = utm[0,:]#+3*np.sin(1/20*(2*np.pi)*np.arange(len(utm[0])))
north = utm[1,:]
height = data_imp['height(m)']

print(np.std(east))
print(np.std(north))

f, (ax1, ax2, ax3) = plt.subplots(3, figsize=(11.5,6))

ax1.axhline(528388.696)
ax2.axhline(8687105.363)
ax3.axhline(342.045)

for ax, y in [(ax1, east), (ax2, north), (ax3, height)]:

    x=range(len(y))

    ax.plot(x, y)
    for N in [20, 50, 200]:
        ax.plot(x[int(N/2-1):-int(N/2)], np.convolve(y, np.ones((N,))/N, mode='valid'))

   
plt.savefig('../fig/' + filename + '_Timeseries-east-north-elev.pdf')



if __name__ == '__main__':
#    print(fieldbook)
    print(data_imp.describe())

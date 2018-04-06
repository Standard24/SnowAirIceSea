#!/usr/bin/env python

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from coordinate_transformation2 import from_latlon

suffix = 'LC'
namefile = pd.read_csv('../data/LC-STEC-data.csv', sep='\s')

filenames = [str(name) + '_corr_' + suffix for name in namefile['filename']]
stakenames = [str(name) for name in namefile['name']]

# read data from all pos files
data_imp = [pd.read_csv('../data/processed_data/' + filename + '.pos',
                    sep='\s+',
                    comment='%',
                    names=['date', 'time', 'latitude(deg)', 'longitude(deg)',
                    'height(m)', 'Q', 'ns', 'sdn(m)', 'sde(m)', 'sdu(m)',
                    'sdne(m)', 'sdeu(m)', 'sdun(m)', 'age(s)', 'ratio'])
            for filename in filenames]


# calculate mean values of columns

# no filtering
#mean_values = [stake.mean() for stake in data_imp]

# only take values with Q==2
#mean_values = [stake[stake['Q'] == 2].mean() for stake in data_imp]

# use weighted average

mean_values = []
for stake in data_imp:
    mean_values += [pd.Series({
    'latitude(deg)' : np.average(stake['latitude(deg)'],
    weights=[1/(s**2) for s in stake['sdn(m)']]),
    'longitude(deg)' : np.average(stake['longitude(deg)'],
    weights=[1/(s**2) for s in stake['sde(m)']]),
    'height(m)' : np.average(stake['height(m)'],
    weights=[1/(s**2) for s in stake['sdu(m)']])
                             })]
               

# give each data frame a name attribute
for i, df in enumerate(mean_values):
    df.df_name = stakenames[i]

###############################################################################
# write mean values to textfile
# header for textfile
header = ['Name', 'Northing', 'Easting', 'Elevation']

# list of lines with data
# convert lonlat to utm
data = [ 
        [mv.df_name,
         from_latlon(mv['latitude(deg)'], mv['longitude(deg)'])[1],
         from_latlon(mv['latitude(deg)'], mv['longitude(deg)'])[0],
         mv['height(m)'] ] 
        for mv in mean_values] 

writeToFile = [header] + data

with open('../data/stake_coordinates/2018_stake_coordinates_corr_'
          + suffix + '.csv', 'w') as f:
    for line in writeToFile:
        # use space as separator, dont write [, ] and '
        write = str(line).replace(',', '').replace('\'', '')[1:-1]
        f.write(write + '\n')

if __name__ == '__main__':
#    print(fieldbook)
    print([d.describe() for d in data_imp])


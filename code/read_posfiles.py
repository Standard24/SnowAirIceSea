#!/usr/bin/env python

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from coordinate_transformation2 import from_latlon


fieldbook = pd.read_csv('../data/fieldbook_data.csv',
                        sep='\s')

filenames = [str(name) + '_corr' for name in fieldbook['filename']]
stakenames = [str(name) for name in fieldbook['name']]

# read data from all pos files
data_imp = [pd.read_csv('../data/processed_data/' + filename + '.pos',
                    sep='\s+',
                    comment='%',
                    names=['date', 'time', 'latitude(deg)', 'longitude(deg)',
                    'height(m)', 'Q', 'ns', 'sdn(m)', 'sde(m)', 'sdu(m)',
                    'sdne(m)', 'sdeu(m)', 'sdun(m)', 'age(s)', 'ratio'])
            for filename in filenames]


# add columns with utm coordinates
for df in data_imp:
    df['latitude(m)'] = df.apply(
      lambda row: from_latlon(row['latitude(deg)'], row['longitude(deg)'])[1],
      axis=1)
    df['longitude(m)'] = df.apply(
      lambda row: from_latlon(row['latitude(deg)'], row['longitude(deg)'])[0],
      axis=1)

# calculate mean values of columns

# no filtering
#mean_values = [stake.mean() for stake in data_imp]

# only take values with Q==2
#mean_values = [stake[stake['Q'] == 2].mean() for stake in data_imp]

# use weighted average
mean_values = []
for stake in data_imp:
    mean_values += [pd.Series({
    'latitude(m)' : np.average(stake['latitude(m)'],
    weights=[1/(s**2) for s in stake['sdn(m)']]),
    'longitude(m)' : np.average(stake['longitude(m)'],
    weights=[1/(s**2) for s in stake['sde(m)']]),
    'height(m)' : np.average(stake['height(m)'],
    weights=[1/(s**2) for s in stake['sdu(m)']])
                             })]

# calculate standard deviations of timeseries for each stake
uncertainties = [
    [np.std(stake['latitude(m)']),
     np.std(stake['longitude(m)']),
     np.std(stake['height(m)'])]
     for stake in data_imp]

# give each data frame a name attribute
for i, df in enumerate(mean_values):
    df.df_name = stakenames[i]

###############################################################################
# write mean values to textfile
# header for textfile
header = ['Name', 'Northing', 'Easting', 'Elevation', 'sN', 'sE', 'sH']

# list of lines with data
# convert lonlat to utm
data = [ 
        [mv.df_name,
         mv['latitude(m)'],
         mv['longitude(m)'],
         mv['height(m)'],
         uc[0],
         uc[1],
         uc[2] ] 
        for mv, uc in zip(mean_values, uncertainties)] 

writeToFile = [header] + data

with open('../data/stake_coordinates/2018_stake_coordinates_corr.csv',
          'w') as f:
    for line in writeToFile:
        # use space as separator, dont write [, ] and '
        write = str(line).replace(',', '').replace('\'', '')[1:-1]
        f.write(write + '\n')

if __name__ == '__main__':
#    print(fieldbook)
    print([d.describe() for d in data_imp])

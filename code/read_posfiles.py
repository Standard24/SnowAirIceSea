#!/usr/bin/env python

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from coordinate_transformation2 import from_latlon


filenames =  ['46250700', '46250700_corr', '46250701', '46250703', '46250704', '46250705']
stakenames = ['T1-2017',  'T1c-2017',      'T1-2018',  'T2-2016',  'T3-2017',  'T3-2018' ]

# read data from all pos files
data_imp = [pd.read_csv('../data/processed_data/' + filename + '.pos',
                    sep='\s+',
                    comment='%',
                    names=['date', 'time', 'latitude(deg)', 'longitude(deg)',
                    'height(m)', 'Q', 'ns', 'sdn(m)', 'sde(m)', 'sdu(m)',
                    'sdne(m)', 'sdeu(m)', 'sdun(m)', 'age(s)', 'ratio'])
            for filename in filenames]

# calculate mean values of columns
mean_values = [stake.mean() for stake in data_imp]

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

with open('../data/stake_coordinates/2018_stake_coordinates.csv', 'w') as f:
    for line in writeToFile:
        # use space as separator, dont write [, ] and '
        write = str(line).replace(',', '').replace('\'', '')[1:-1]
        f.write(write + '\n')


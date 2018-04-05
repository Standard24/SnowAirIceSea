# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 14:54:19 2018

@author: linda
"""

filename = '2018_stake_coordinates_trimble_post'

#data = pd.read_csv('../data/stake_coordinates/' + filename
#        + '.csv', sep=' ')
        
data = pd.read_csv('../data/processed_data/' + filename + '.csv',
                    sep='\s',
                    names=['date', 'Northing', 'Easting', 'Elevation'])
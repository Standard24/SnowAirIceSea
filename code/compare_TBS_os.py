# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 16:08:57 2018

@author: linda
"""

filename_tbc = '2018_stake_coordinates_trimble_post'
data_tbc = pd.read_csv('../data/stake_coordinates/' + filename_tbc
        + '.csv', sep=' ')
        
filename_os = '2018_stake_coordinates_corr_LC'
data_os = pd.read_csv('../data/stake_coordinates/' + filename_os
        + '.csv', sep=' ')

data_tbc_dir = {}
for i in range(0,len(data_tbc['Name'])):
    data_tbc_dir[data_tbc['Name'][i]] = {'Northing': data_tbc['Northing'][i],\
    'Easting': data_tbc['Easting'][i], 'Elevation': data_tbc['Elevation'][i]}
    
    data_os_dir = {}
for i in range(0, len(data_os['Name'])):
    data_os_dir[data_os['Name'][i]] = {'Northing': data_os['Northing'][i],\
    'Easting': data_os['Easting'][i], 'Elevation': data_os['Elevation'][i]}
    
diff_north = [] 
diff_east = []
diff_elev = []
diff_dir = {}
for key in data_os_dir.keys():
    diff_north = data_tbc_dir[key]['Northing']-data_os_dir[key]['Northing']
    diff_east = data_tbc_dir[key]['Easting']-data_os_dir[key]['Easting']
    diff_elev = data_tbc_dir[key]['Elevation']-data_os_dir[key]['Elevation']
    diff_dir[key] = {'Difference_Northing': diff_north, 'Difference_Easting': diff_east, 'Difference_Elevation': diff_elev}
    
df_difference = pd.DataFrame(diff_dir).transpose().reset_index().rename(columns={'index':'Name'})
print df_difference

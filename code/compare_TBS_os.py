# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 16:08:57 2018

@author: linda
"""

filename_tbc = '2018_stake_coordinates_trimble_post_final'
data_tbc = pd.read_csv('../data/stake_coordinates/' + filename_tbc
        + '.csv', sep=' ')
        
filename_os = '2018_stake_coordinates_corr_final'
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
    diff_dir[key] = {'dN': np.abs(round(diff_north,2)), 
    'dE': np.abs(round(diff_east,2)), 
    'dH': np.abs(round(diff_elev,2))}
    
df_difference = pd.DataFrame(diff_dir).transpose().reset_index().rename(columns={'index':'Name'})

df_diff_tab = pd.DataFrame(diff_dir).transpose().reset_index().rename(columns={'index':'Name',
 'dN': 'Difference Northing [m]', 
 'dE': 'Difference Easting [m]', 
 'dH': 'Difference Elevation [m]' })
df_diff_tab = df_diff_tab[['Name', 'Difference Northing [m]', 
'Difference Easting [m]', 'Difference Elevation [m]']]
tab_diff = df_diff_tab.to_latex(index=False)

with open('../protocol/tables/diff_tab.tex', 'w') as f:
    f.write(tab_diff.encode('utf-8'))

# data in .csv-file 
df_diff = pd.DataFrame(diff_dir).transpose().reset_index().rename(columns={'index':'Name'})
df_diff.to_csv('../data/diff_tbc_os.csv', sep=' ', encoding='utf-8')

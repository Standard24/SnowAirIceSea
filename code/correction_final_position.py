# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 14:54:19 2018

@author: linda
"""
import pandas as pd
import numpy as np

# --- read in post processed data
# TBC data
filename = '2018_stake_coordinates_trimble_post'
data_tbc = pd.read_csv('../data/stake_coordinates/' + filename
        + '.csv', sep=' ')
      
data_tbc_dir = {}
for i in range(0, len(data_tbc['Name'])):
    data_tbc_dir[data_tbc['Name'][i]] = {'Northing': data_tbc['Northing'][i],\
    'Easting': data_tbc['Easting'][i], 'Elevation': data_tbc['Elevation'][i]}
    
# open source data 
#filename = '2018_stake_coordinates_open_source_post'
#data_os = pd.read_csv('../data/stake_coordinates/' + filename
#        + '.csv', sep=' ')
#      
#data_os_dir = {}
#for i in range(0, len(data_os['Name'])):
#    data_os_dir[data_os['Name'][i]] = {'Northing': data_os['Northing'][i],\
#    'Easting': data_os['Easting'][i], 'Elevation': data_os['Elevation'][i]}

# fieldbook data
fieldbook = pd.read_csv('../data/fieldbook_data.csv',
                        sep='\s')

# --- data to directory
corr_dir = {}   
fd_dir = {}                  
for k in range(0, len(fieldbook['name'])):
    # --- calculate the correction values 
    # absoute delta
    delta = (fieldbook['snow_depth'][k] + fieldbook['antenna_height'][k] - fieldbook['dh_17_18'][k]) * np.sin(fieldbook['inclination'][k])   
    # correction for the northing    
    delta_north = - delta * np.cos(fieldbook['inc_dir'][k])\
    - fieldbook['distance_top'][k]
    # correction for the easting    
    delta_east = - delta * np.sin(fieldbook['inc_dir'][k])
    # correction for the elevation 
    delta_elev = fieldbook['snow_depth'][k] + fieldbook['antenna_height'][k]
    # correction for the trimble elevation (antenna height already included)
    delta_elev_trimb = fieldbook['snow_depth'][k]
    corr_dir[fieldbook['name'][k]] = {'delta_north': delta_north,\
    'delta_east': delta_east, 'delta_elev': delta_elev,\
    'delta_elev_trimb': delta_elev_trimb}
    
    # creating dict for the fieldbook data table     
    fd_dir[fieldbook['name'][k]] = {'Northing [m]': '{:.2f}'.format(fieldbook['northing'][k]),
    'Easting [m]': '{:.2f}'.format(fieldbook['easting'][k]),
    'Elevation [m]': round(fieldbook['elevation'][k],2),
    'Antenna height [m]': fieldbook['antenna_height'][k], 
    'Snow depth [m]': fieldbook['snow_depth'][k],
    'Inclination [deg]': fieldbook['inclination'][k],
    'Direction of Incl. [deg]': fieldbook['inc_dir'][k],
    'Distance Rover-Stake [m]': fieldbook['distance_top'][k]}   
         
final_tbc_dir = {}      
final_os_dir = {}       
for key in data_tbc_dir.keys():
    # corrected values for TBC
    n_tbc = data_tbc_dir[key]['Northing'] + corr_dir[key]['delta_north']
    e_tbc = data_tbc_dir[key]['Easting'] + corr_dir[key]['delta_east']
    u_tbc = data_tbc_dir[key]['Elevation'] + corr_dir[key]['delta_elev_trimb']
    final_tbc_dir[key] = {'Northing': round(n_tbc,2), 'Easting': round(e_tbc,2), \
    'Elevation': round(u_tbc,2)}
    # corrected values for TBC
#    n_os = data_os_dir[key]['Northing'] + corr_dir[key]['delta_north']
#    e_os = data_os_dir[key]['Easting'] + corr_dir[key]['delta_east']
#    u_os = data_os_dir[key]['Elevation'] + corr_dir[key]['delta_elev']
#    final_os_dir[key] = {'Northing': round(n_os,2), 'Easting': round(e_os,2), \
#    'Elevation': round(u_os,2)}
    
    
# --- data to DataFrame
# TBC    
df_tbc_final = pd.DataFrame(final_tbc_dir).transpose().reset_index().rename(columns={'index':'Name',
 'Northing': 'Northing [m]', 'Easting': 'Easting [m]', 'Elevation': 'Elevation [m]' })
df_tbc_final = df_tbc_final[['Name', 'Northing [m]', 'Easting [m]', 'Elevation [m]']]
tab_tbc_final = df_tbc_final.to_latex(index=False)
 
f = open('../protocol/tables/tbc_tab.tex', 'w')
f.write(tab_tbc_final.encode('utf-8'))

# open source
#df_os_final = pd.DataFrame(final_os_dir).transpose().reset_index().rename(columns={'index':'Name',
# 'Northing': 'Northing [m]', 'Easting': 'Easting [m]', 'Elevation': 'Elevation [m]' })
#df_os_final = df_os_final[['Name', 'Northing [m]', 'Easting [m]', 'Elevation [m]']]
#tab_os_final = df_os_final.to_latex(index=False)
# 
#f = open('../protocol/tables/os_tab.tex', 'w')
#f.write(tab_os_final.encode('utf-8'))

# fieldbook
df_fb_final = pd.DataFrame(fd_dir).transpose().reset_index().rename(columns={'index':'Name'})
df_fb_final = df_fb_final[['Name', 'Northing [m]', 'Easting [m]',
'Elevation [m]', 'Antenna height [m]', 'Snow depth [m]', 'Inclination [deg]',  
'Direction of Incl. [deg]', 'Distance Rover-Stake [m]']]
tab_fb_final = df_fb_final.to_latex(index=False)
 
with open('../protocol/tables/fb_tab.tex', 'w') as f:
    f.write(tab_fb_final.encode('utf-8'))
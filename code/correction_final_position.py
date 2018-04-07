# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 14:54:19 2018

@author: linda
"""
import pandas as pd
import numpy as np

# --- read in post processed data
# TBC data
filename_tbc = '2018_stake_coordinates_trimble_post'
data_tbc = pd.read_csv('../data/stake_coordinates/' + filename_tbc
        + '.csv', sep=' ')
      
data_tbc_dir = {}
for i in range(0, len(data_tbc['Name'])):
    data_tbc_dir[data_tbc['Name'][i]] = {'Northing': data_tbc['Northing'][i],\
    'Easting': data_tbc['Easting'][i], 'Elevation': data_tbc['Elevation'][i]}
    
# open source data 
filename_os = '2018_stake_coordinates_corr'
data_os = pd.read_csv('../data/stake_coordinates/' + filename_os
        + '.csv', sep=' ')
      
data_os_dir = {}
for i in range(0, len(data_os['Name'])):
    data_os_dir[data_os['Name'][i]] = {'Northing': data_os['Northing'][i],\
    'Easting': data_os['Easting'][i], 'Elevation': data_os['Elevation'][i],\
    'sN': data_os['sN'][i], 'sE': data_os['sE'][i],
    'sH': data_os['sH'][i]}

# fieldbook data
fieldbook = pd.read_csv('../data/fieldbook_data.csv',
                        sep='\s')

# --- data to directory
corr_dir = {}   
fd_pos_dir = {}  
fd_other_dir = {} 
error_dir = {}               
for k in range(0, len(fieldbook['name'])):
    # --- calculate the correction values 
    # absoute delta
    delta = (fieldbook['snow_depth'][k] + fieldbook['antenna_height'][k]) * np.sin(np.deg2rad(fieldbook['inclination'][k]))   
    delta_ref_17 = (fieldbook['snow_depth'][k] + fieldbook['antenna_height'][k] - fieldbook['dh_17_18'][k]) * np.sin(np.deg2rad(fieldbook['inclination'][k]))
    delta_ref_16 = (fieldbook['snow_depth'][k] + fieldbook['antenna_height'][k] - fieldbook['dh_16_18'][k]) * np.sin(np.deg2rad(fieldbook['inclination'][k]))
    delta_ref_15 = (fieldbook['snow_depth'][k] + fieldbook['antenna_height'][k] - fieldbook['dh_15_18'][k]) * np.sin(np.deg2rad(fieldbook['inclination'][k]))
    # correction for the northing    
    delta_north = - delta * np.cos(np.deg2rad(fieldbook['inc_dir'][k])) - fieldbook['distance_top'][k]
    delta_north_ref_17 = - delta_ref_17 * np.cos(np.deg2rad(fieldbook['inc_dir'][k])) - fieldbook['distance_top'][k]
    delta_north_ref_16 = - delta_ref_16 * np.cos(np.deg2rad(fieldbook['inc_dir'][k])) - fieldbook['distance_top'][k]
    delta_north_ref_15 = - delta_ref_15 * np.cos(np.deg2rad(fieldbook['inc_dir'][k])) - fieldbook['distance_top'][k]
    # correction for the easting    
    delta_east = - delta * np.sin(np.deg2rad(fieldbook['inc_dir'][k]))
    delta_east_ref_17 = - delta_ref_17 * np.sin(np.deg2rad(fieldbook['inc_dir'][k]))
    delta_east_ref_16 = - delta_ref_16 * np.sin(np.deg2rad(fieldbook['inc_dir'][k]))
    delta_east_ref_15 = - delta_ref_15 * np.sin(np.deg2rad(fieldbook['inc_dir'][k]))
    # correction for the elevation 
    delta_elev = - (fieldbook['snow_depth'][k] + fieldbook['antenna_height'][k])
    # correction for the trimble elevation (antenna height already included)
    delta_elev_trimb = - fieldbook['snow_depth'][k]
    corr_dir[fieldbook['name'][k]] = {
    'delta_north': delta_north,\
    'delta_east': delta_east,\
    'delta_north_ref_17': delta_north_ref_17,\
    'delta_east_ref_17': delta_east_ref_17, 
    'delta_north_ref_16': delta_north_ref_16,\
    'delta_east_ref_16': delta_east_ref_16, 
    'delta_north_ref_15': delta_north_ref_15,\
    'delta_east_ref_15': delta_east_ref_15,\
    'delta_elev': delta_elev,\
    'delta_elev_trimb': delta_elev_trimb}
    
    # --- error propagation:
    s_hs = .02
    s_ha = .05
    s_dh = .1
    s_inc = np.deg2rad(3.)
    s_inc_dir = np.deg2rad(22.5)
    s_delta = np.sqrt((fieldbook['snow_depth'][k]**2 + fieldbook['antenna_height'][k]**2) * np.cos(np.deg2rad(fieldbook['inclination'][k]))**2 * s_inc**2\
            + (s_hs + s_ha)**2 * np.sin(np.deg2rad(fieldbook['inclination'][k]))**2)
    s_delta_north = np.sqrt(s_delta**2 * np.cos(np.deg2rad(fieldbook['inc_dir'][k]))**2 + s_inc_dir**2 * delta**2 * np.sin(np.deg2rad(fieldbook['inc_dir'][k]))**2)
    s_delta_east = np.sqrt(s_delta**2 * np.sin(np.deg2rad(fieldbook['inc_dir'][k]))**2 + s_inc_dir**2 * delta**2 * np.cos(np.deg2rad(fieldbook['inc_dir'][k]))**2)
    s_delta_elev = np.sqrt(s_ha**2 + s_hs**2)
    s_final_north = np.sqrt(data_os_dir[fieldbook['name'][k]]['sN']**2 + s_delta_north**2)
    s_final_east = np.sqrt(data_os_dir[fieldbook['name'][k]]['sE']**2 + s_delta_east**2)
    s_final_elev = np.sqrt(s_delta_elev**2 + data_os_dir[fieldbook['name'][k]]['sH']**2)
    #s_delta_ref_17 =
    #s_delta_ref_16 = 
    #s_delta_ref_15 = 
    
    error_dir[fieldbook['name'][k]] = {'sN': round(s_final_north,2), 'sE': round(s_final_east,2), 'sH': round(s_final_elev,2)}
        
    # creating dict for the fieldbook data table     
    fd_pos_dir[fieldbook['name'][k]] = {'Northing [m]': '{:.2f}'.format(fieldbook['northing'][k]),
    'Easting [m]': '{:.2f}'.format(fieldbook['easting'][k]),
    'Elevation [m]': round(fieldbook['elevation'][k],2)}
    
    fd_other_dir[fieldbook['name'][k]] = {'Antenna height [m]': fieldbook['antenna_height'][k], 
    'Snow depth [m]': fieldbook['snow_depth'][k],
    'Inclination [deg]': fieldbook['inclination'][k],
    'Direction of Incl. [deg]': fieldbook['inc_dir'][k],
    'Distance Rover-Stake [m]': fieldbook['distance_top'][k]}   
         
final_tbc_dir = {}      
final_os_dir = {}     
final_os_ref_dir = {}  
for key in data_tbc_dir.keys():
    # corrected values for TBC
    n_tbc = data_tbc_dir[key]['Northing'] + corr_dir[key]['delta_north']
    e_tbc = data_tbc_dir[key]['Easting'] + corr_dir[key]['delta_east']
    u_tbc = data_tbc_dir[key]['Elevation'] + corr_dir[key]['delta_elev_trimb']
    final_tbc_dir[key] = {'Northing': round(n_tbc,2), 'Easting': round(e_tbc,2), \
    'Elevation': round(u_tbc,2)}
    # corrected values for TBC
    n_os = data_os_dir[key]['Northing'] + corr_dir[key]['delta_north']
    e_os = data_os_dir[key]['Easting'] + corr_dir[key]['delta_east']
    u_os = data_os_dir[key]['Elevation'] + corr_dir[key]['delta_elev']
    n_os_ref_17 = data_os_dir[key]['Northing'] + corr_dir[key]['delta_north_ref_17']
    e_os_ref_17 = data_os_dir[key]['Easting'] + corr_dir[key]['delta_east_ref_17']
    n_os_ref_16 = data_os_dir[key]['Northing'] + corr_dir[key]['delta_north_ref_16']
    e_os_ref_16 = data_os_dir[key]['Easting'] + corr_dir[key]['delta_east_ref_16']
    n_os_ref_15 = data_os_dir[key]['Northing'] + corr_dir[key]['delta_north_ref_15']
    e_os_ref_15 = data_os_dir[key]['Easting'] + corr_dir[key]['delta_east_ref_15']
    
    final_os_dir[key] = {'Northing': round(n_os,2), 'Easting': round(e_os,2), \
    'Elevation': round(u_os,2)}
    
    final_os_ref_dir[key] = {'Northing_17': round(n_os_ref_17,2), 'Easting_17': round(e_os_ref_17,2), \
    'Northing_16': round(n_os_ref_16,2), 'Easting_16': round(e_os_ref_16,2), \
    'Northing_15': round(n_os_ref_15,2), 'Easting_15': round(e_os_ref_15,2), \
    'Elevation': round(u_os,2)}
    
# --- data to DataFrame
# TBC    
#df_tbc_tab_final = pd.DataFrame(final_tbc_dir).transpose().reset_index().rename(columns={'index':'Name',
# 'Northing': 'Northing [m]', 'Easting': 'Easting [m]', 'Elevation': 'Elevation [m]' })
#df_tbc_tab_final = df_tbc_tab_final[['Name', 'Northing [m]', 'Easting [m]', 'Elevation [m]']]
#tab_tbc_final = df_tbc_tab_final.to_latex(index=False)

#with open('../protocol/tables/tbc_tab.tex', 'w') as f:
#    f.write(tab_tbc_final.encode('utf-8'))

## data in .csv-file 
#df_tbc_final = pd.DataFrame(final_tbc_dir).transpose().reset_index().rename(columns={'index':'Name'})
#df_tbc_final.to_csv('../data/stake_coordinates/' + filename_tbc + '_final' + '.csv', sep=' ', encoding='utf-8')

## open source
#df_os_tab_final = pd.DataFrame(final_os_dir).transpose().reset_index().rename(columns={'index':'Name',
# 'Northing': 'Northing [m]', 'Easting': 'Easting [m]', 'Elevation': 'Elevation [m]' })
#df_os_tab_final = df_os_tab_final[['Name', 'Northing [m]', 'Easting [m]', 'Elevation [m]']]
#tab_os_final = df_os_tab_final.to_latex(index=False)

#with open('../protocol/tables/os_tab.tex', 'w') as f:
#    f.write(tab_os_final.encode('utf-8'))

#df_os_final = pd.DataFrame(final_os_dir).transpose().reset_index().rename(columns={'index':'Name'})
#df_error = pd.DataFrame(error_dir).transpose().reset_index().rename(columns={'index':'Name'})
#df_os_final = df_os_final.merge(df_error)
#df_os_final.to_csv('../data/stake_coordinates/' + filename_os + '_final' + '.csv', sep=' ', encoding='utf-8')

## position vales referenced to the last year (for the velocity)
#df_os_ref_final = pd.DataFrame(final_os_ref_dir).transpose().reset_index().rename(columns={'index':'Name'})
#df_os_ref_final.to_csv('../data/stake_coordinates/' + filename_os + '_ref_final' + '.csv', sep=' ', encoding='utf-8')

# fieldbook
#df_fb_final = pd.DataFrame(fd_pos_dir).transpose().reset_index().rename(columns={'index':'Name'})
#df_other_final = pd.DataFrame(fd_other_dir).transpose().reset_index().rename(columns={'index':'Name'})
#df_fb_final = df_fb_final[['Name', 'Northing [m]', 'Easting [m]', 'Elevation [m]']]
#df_other_final = df_other_final[['Name', 'Antenna height [m]', 'Snow depth [m]', 'Inclination [deg]',  
#'Direction of Incl. [deg]', 'Distance Rover-Stake [m]']]
#tab_fb_final = df_fb_final.to_latex(index=False)
#tab_other_final = df_other_final.to_latex(index=False)
 
#with open('../protocol/tables/fb_pos_tab.tex', 'w') as f:
#    f.write(tab_fb_final.encode('utf-8'))
#
#with open('../protocol/tables/fb_other_tab.tex', 'w') as f:
#    f.write(tab_other_final.encode('utf-8'))
 
 
 
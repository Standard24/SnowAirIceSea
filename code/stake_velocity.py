# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 22:22:41 2018

@author: linda
"""
import pandas as pd
import numpy as np
# read in data
filename_ref = '2018_stake_coordinates_corr_ref_final'
data_ref = pd.read_csv('../data/stake_coordinates/' + filename_ref
        + '.csv', sep=' ')
pos_ref_dict = {}
for i in range(0,len(data_ref['Name'])):
    pos_ref_dict[data_ref['Name'][i]] = {'Northing_17': data_ref['Northing_17'][i],
                                      'Easting_17': data_ref['Easting_17'][i],
                                      'Northing_16': data_ref['Northing_16'][i],
                                      'Easting_16': data_ref['Easting_16'][i],
                                      'Northing_15': data_ref['Northing_15'][i],
                                      'Easting_15': data_ref['Easting_15'][i],
                                      'sN_ref_17': data_ref['sN_ref_17'][i],
                                      'sE_ref_17': data_ref['sE_ref_17'][i],
                                      'sN_ref_16': data_ref['sN_ref_16'][i],
                                      'sE_ref_16': data_ref['sE_ref_16'][i],
                                      'sN_ref_15': data_ref['sN_ref_15'][i],
                                      'sE_ref_15': data_ref['sE_ref_15'][i]}
        
filename_pos_17 = '2017_stake_coordinates'
data_17 = pd.read_csv('../data/stake_coordinates/' + filename_pos_17
        + '.csv', sep=' ')
pos_17_dict = {}
for i in range(0,len(data_17['Name'])):
    pos_17_dict[data_17['Name'][i]] = {'Northing': data_17['Northing'][i],
                                      'Easting': data_17['Easting'][i]}
        
filename_pos_16 = '2016_stake_coordinates'
data_16 = pd.read_csv('../data/stake_coordinates/' + filename_pos_16
        + '.csv', sep=' ')
pos_16_dict = {}
for i in range(0,len(data_16['Name'])):
    pos_16_dict[data_16['Name'][i]] = {'Northing': data_16['Northing'][i],
                                      'Easting': data_16['Easting'][i]}
        
filename_pos_15 = '2015_stake_coordinates_deg2utm'
data_15 = pd.read_csv('../data/stake_coordinates/' + filename_pos_15
        + '.csv', sep=' ')
pos_15_dict = {}
for i in range(0,len(data_15['Name'])):
    pos_15_dict[data_15['Name'][i]] = {'Northing': data_15['Northing'][i],
                                      'Easting': data_15['Easting'][i]}
             
sN_mean = 0.40
sE_mean = 0.19                      
# calculation of the velocity and error
vel_dict= {}  
list_2018 = ['BL2-2018', 'BL3-2018', 'BL4-2018', 'T1-2018', 'T2-2018', 'T4-2018', 'T5-2018', 'T6-2018']  
for key in pos_ref_dict.keys():
    if key in list_2018:
        print key, 'no velocities for 2018 stakes'
        pass
    else:
        # 2017 stakes 
        if key == 'BL4-i-2016' or key == 'BL4-ii-2016':
            key_old = 'BL4-2016'
        elif key == 'BL5-i-2017' or key == 'BL5-ii-2017':
            key_old = 'BL5-2017'
        elif key == 'T1-i-2017' or key == 'T1-ii-2017':
            key_old = 'T1-2017'
        elif key == 'T2-i-2017' or key == 'T2-ii-2017':
            key_old = 'T2-2017'
        else:
            key_old = key
            
        try:        
            v17 = np.sqrt((pos_ref_dict[key]['Northing_17'] - pos_17_dict[key_old]['Northing'])**2\
            + (pos_ref_dict[key]['Easting_17'] - pos_17_dict[key_old]['Easting'])**2)
            sN_pos_17 = sN_mean
            sE_pos_17 = sE_mean
            s_v17 = np.sqrt(((pos_ref_dict[key]['Northing_17'] - pos_17_dict[key_old]['Northing'])**2\
            * (pos_ref_dict[key]['sN_ref_17']*2 + sN_pos_17**2)\
            + (pos_ref_dict[key]['Easting_17'] - pos_17_dict[key_old]['Easting'])**2)\
            * (pos_ref_dict[key]['sE_ref_17']**2 + sE_pos_17**2)/((pos_ref_dict[key]['Northing_17'] \
            - pos_17_dict[key_old]['Northing'])**2\
            + (pos_ref_dict[key]['Easting_17'] - pos_17_dict[key_old]['Easting'])**2))
        except Exception as e: 
            print(e,' 2017 data')
            v17 = np.nan
            s_v17 = np.nan
        # 2016 stakes        
        try:
            # velocity
            v16 = np.sqrt((pos_ref_dict[key]['Northing_16'] - pos_16_dict[key_old]['Northing'])**2
            + (pos_ref_dict[key]['Easting_16'] - pos_16_dict[key_old]['Easting'])**2)
            v16 = v16/2
            # error
            sN_pos_16 = sN_mean
            sE_pos_16 = sE_mean
            s_v16 = np.sqrt(((pos_ref_dict[key]['Northing_16'] - pos_16_dict[key_old]['Northing'])**2\
            * (pos_ref_dict[key]['sN_ref_16']**2 + sN_pos_16**2)\
            + (pos_ref_dict[key]['Easting_16'] - pos_16_dict[key_old]['Easting'])**2)\
            * (pos_ref_dict[key]['sE_ref_16']**2 + sE_pos_16**2)/((pos_ref_dict[key]['Northing_16'] \
            - pos_16_dict[key_old]['Northing'])**2\
            + (pos_ref_dict[key]['Easting_16'] - pos_16_dict[key_old]['Easting'])**2)) 
        except Exception as e: 
            print(e, '2016 data')
            v16 = np.nan
            s_v16 = np.nan
        # 2015 stakes        
        try:
            # velocity
            v15 = np.sqrt((pos_ref_dict[key]['Northing_15'] - pos_15_dict[key_old]['Northing'])**2
            + (pos_ref_dict[key]['Easting_15'] - pos_15_dict[key_old]['Easting'])**2)
            v15 = v15/3
            # error
            sN_pos_15 = sN_mean
            sE_pos_15 = sE_mean
            s_v15 = np.sqrt(((pos_ref_dict[key]['Northing_15'] - pos_15_dict[key_old]['Northing'])**2\
            * (pos_ref_dict[key]['sN_ref_15']**2 + sN_pos_15**2)\
            + (pos_ref_dict[key]['Easting_15'] - pos_15_dict[key_old]['Easting'])**2)\
            * (pos_ref_dict[key]['sE_ref_15']**2 + sE_pos_15**2)/((pos_ref_dict[key]['Northing_15'] \
            - pos_15_dict[key_old]['Northing'])**2\
            + (pos_ref_dict[key]['Easting_15'] - pos_15_dict[key_old]['Easting'])**2)) 
        except Exception as e: 
            print(e, '2015 data')
            v15 = np.nan
            s_v15 = np.nan
            
        vel_dict[key] = {'Velocity_17': round(v17,2), 'Error_17':round(s_v17,2), 
            'Velocity_16': round(v16,2), 'Error_16':round(s_v16,2), 
            'Velocity_15': round(v15,2), 'Error_15':round(s_v15,2)}
        

df_vel = pd.DataFrame(vel_dict).transpose().reset_index().rename(columns={'index':'Name'})
df_vel.to_csv('../data/stake_velocities.csv', sep=' ', encoding='utf-8')    

df_vel = pd.DataFrame(vel_dict).transpose().reset_index().rename(columns={'index':'Stake name', 
'Velocity_17': 'Velocity $v_{2017}$ [m/a]', 'Error_17': 'Error (2017) [m/a]', 
'Velocity_16': 'Velocity $v_{2016}$ [m/a]', 'Error_16': 'Error (2016) [m/a]', 
'Velocity_15': 'Velocity $v_{2015}$ [m/a]', 'Error_15': 'Error (2015) [m/a]' })
df_vel = df_vel[['Stake name',
'Velocity $v_{2017}$ [m/a]', 'Error (2017) [m/a]', 
'Velocity $v_{2016}$ [m/a]', 'Error (2016) [m/a]', 
'Velocity $v_{2015}$ [m/a]', 'Error (2015) [m/a]']]

def nice_format(row, i):
    if row[i] != row[i]:
        return '-'
    else:
        ret = '%.2f'%row[i] + ' $\pm$ ' + '%.2f'%row[i+1]
        return ret

df_vel['Velocity $v_{2017}$ [m/a]'] = df_vel.apply(lambda row: nice_format(row, 1), axis=1)
df_vel['Velocity $v_{2016}$ [m/a]'] = df_vel.apply(lambda row: nice_format(row, 3), axis=1)
df_vel['Velocity $v_{2015}$ [m/a]'] = df_vel.apply(lambda row: nice_format(row, 5), axis=1)
df_vel = df_vel.drop('Error (2017) [m/a]', 1)
df_vel = df_vel.drop('Error (2016) [m/a]', 1)
df_vel = df_vel.drop('Error (2015) [m/a]', 1)
#import IPython
#IPython.embed()

#tab_vel = df_vel.to_latex(index=False, na_rep='-', column_format='lcccccc', escape=False)
#with open('../protocol/tables/vel_tab.tex', 'w') as f:
#    f.write(tab_vel.encode('utf-8'))

#!/usr/bin/env python

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.transforms as mtransforms
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

# use latex to draw text on plots (only for pdf...)
from matplotlib import rc
rc('text', usetex=True)
plt.rc('font', family='serif')


# define plot options
def plotOpts(ax):
    ax.tick_params(axis='both', which='both', direction='in', right=True,
                   top=True)

# list of matplotlibs default colors
defcol = plt.rcParams['axes.prop_cycle'].by_key()['color']

# list of all the years we have data from
time = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]
# make a dictionary which assigns a number from 0-N to each year
t_d = dict(zip(time, range(len(time))))


filenames = ['2009_stake_coordinates',
             '2010_stake_coord_deg2utm',
             '2011_stake_coord_deg2utm',
             '2012_stake_coordinates_deg2utm',
             '2013_post-processed_UTM',
             '2014_stake_coordinates_corrected',
             '2015_stake_coordinates_deg2utm',
             '2016_stake_coordinates',
             '2017_stake_coordinates',
             #'2018_stake_coordinates_trimble_post']
             #'2018_stake_coordinates_corr']
             '2018_stake_coordinates_corr_final']
             #'2018_stake_coordinates_corr_STEC']
             #'2018_stake_coordinates_corr_LC']

# import all csv files: Create a list of pandas data frames
data = [pd.read_csv('../data/stake_coordinates/' + filename
        + '.csv', sep=' ') for filename in filenames]

# print imported data
for i, t in enumerate(time):
    print('\n' + str(t) + ':')
    print(data[i])


# choose one title for each stake and make lists which contains the
# different names of the stake and the different years
titles = {'T1': [[2011, 'T1-2011'], [2012, 'T1-2009'], [2013, 'T1-2009'],
                 #[2014, 'T1-2012'],
                 [2014, 'T1-2014'],
                 #[2015, 'T1-2009'], 
                 [2015, 'T1-2014'], [2015, 'T1-2015'],
                 [2016, 'T1-2015'], [2016, 'T1-2016'],
                 [2017, 'T1-2016'], #[2017, 'T1-2017'],
                 [2018, 'T1-i-2017'], [2018, 'T1-ii-2017'], [2018, 'T1-2018']],
          'T2': [[2011, 'T2-2009'], [2012, 'T2-2009'],
                 [2013, 'T2-2009'], [2014, 'T2-2009'],
                 [2015, 'T2-2009'], [2015, 'T2-2015'],
                 [2016, 'T2-2015'], [2016, 'T2-2016'],
                 [2017, 'T2-2016'], [2017, 'T2-2017'],
                 #[2018, 'T2-2016'], [2018, 'T2-i-2017'], [2018, 'T2-ii-2017'],
                 [2018, 'T2-2018']],
          'T3': [[2011, 'T3-2009'], [2012, 'T3-2009'],
                 [2013, 'T3-2012'], [2014, 'T3-2012'],
                 [2015, 'T3-2012'], [2015, 'T3-2015'],
                 [2016, 'T3-2015'], [2017, 'T3-2017'],
                 [2018, 'T3-2017']],
          'T4': [[2011, 'T4-2009'], [2012, 'T4-a2009'],
                 [2013, 'T4-2009'], [2014, 'T4-2014'], 
                 [2015, 'T4-2014'], [2016, 'T4-2016'],
                 [2017, 'T4-2016'],
                 [2018, 'T4-2016'], #[2018, 'T4-2018']
                 ],
          'T5': [[2011, 'T5-2009'], [2012, 'T5-b2009'],
                 [2013, 'T5-2009'], [2014, 'T5-2012'],
                 [2015, 'T5-2009'], [2016, 'T5-2016'],
                 [2017, 'T5-2016'],
                 [2018, 'T5-2016'], #[2018, 'T5-2018']
                 ],
          'T6': [[2011, 'T6-2009'],#[2012, 'T6-2009'], [2013, 'T6-2009'],
                 [2013, 'T6-2013'],
                 [2015, 'T6-2013'], [2016, 'T6-2016'],
                 [2017, 'T6-2016'],
                 #[2018, 'T6-2016'], 
                 [2018, 'T6-2018']],
          'T7': [[2011, 'T7-2009'], [2012, 'T7-2009'], 
                 [2013, 'T7-2009'], [2014, 'T7-2009'],
                 [2015, 'T7-2009'], [2015, 'T7-2015'],
                 [2016, 'T7-2015'], [2017, 'T7-2015'], [2017, 'T7-2017'],
                 [2018, 'T7-2017'], #[2018, 'T7-2015']
                 ],
          'T8': [[2011, 'T8-2009'], [2012, 'T8-2009'],
                 [2013, 'T8-2009'], [2014, 'T8-2009'],
                 [2015, 'T8-2009'], [2015, 'T8-2015'],
                 #[2016, 'T8-2015'], 
                 [2016, 'T8-2016'],
                 [2017, 'T8-2016'], [2017, 'T8-2017'],
                 [2018, 'T8-2017']],
         'BL2': [[2012, 'BL2-2011'], [2013, 'BL2-2011'], [2014, 'BL2-2011'],
                 [2015, 'BL2-2011'],
                 [2016, 'BL2-2016'], [2017, 'BL2-2016'],
                 #[2018, 'BL2-2016'], 
                 [2018, 'BL2-2018']],
         'BL3': [[2011, 'BL3-2011'],
                 [2012, 'BL3-2011'], [2013, 'BL3-2011'], [2014, 'BL3-2011'],
                 [2015, 'BL3-2011'], [2015, 'BL3-2015'],
                 [2016, 'BL3-2015'], [2016, 'BL3-2016'],
                 #[2017, 'BL3-2015'], 
                 [2017, 'BL3-2016'],
                 [2018, 'BL3-2016'], #[2018, 'BL3-2018']
                 ],
         'BL4': [[2012, 'BL4-2011'], [2013, 'BL4-2011'], [2014, 'BL4-2011'],
                 [2015, 'BL4-2011'], [2016, 'BL4-2016'], [2017, 'BL4-2016'],
                 #[2018, 'BL4-i-2016'], 
                 #[2018, 'BL4-ii-2016'],
                 [2018, 'BL4-2018']],
         'BL5': [[2011, 'BL5-2011'],
                 [2012, 'BL5-2011'], [2013, 'BL5-2011'], [2014, 'BL5-2011'],
                 [2015, 'BL5-2011'], [2016, 'BL5-2011'], [2017, 'BL5-2011'],
                 [2017, 'BL5-2017'],
                 [2018, 'BL5-i-2017'], [2018, 'BL5-ii-2017']]         
         }




stakes = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8',
          'BL2', 'BL3', 'BL4', 'BL5']
colordict = {'2009':defcol[3], '2011':defcol[5],
             '2012':defcol[6], '2013':defcol[7], '2014':defcol[8],
             '2015':defcol[0], '2016':defcol[1], '2017':defcol[2],
             '2018':defcol[9]}
keys = list(colordict.keys())
values= list(colordict.values())

patches = [mpatches.Patch(color=c, label=y, 
                          clip_box=mtransforms.Bbox([[0,.01],[0,.01]]))
           for c, y in zip(values, keys)]


###############################################################################


###############################################################################

# define a stake class to make plots for each stake
class stake(object):
    """ Class representing one stake.
    The constructor takes the title of a stake as argument and reads the
    measurement data for the stake.
    The makePlots() method creates different plots for the stake.
    """

    def __init__(self, title):
        """ Read measurement data from data frames and initialize instance
        variables.
        :param title: title of the stake
        :type title: string
        """
        self.title = title
        # get the different names of the different years
        self.names = list(zip(*titles[title]))[1]
        # get the years of the measurements
        self.dates = list(zip(*titles[title]))[0]

        # read the particular row(s) for the stake from each data frame
        self.data = []
        for date, name in zip(self.dates, self.names):
            row = data[t_d[date]].loc[data[t_d[date]]['Name'] == name]
            if row.empty:
                print('--- ' + str(date) + ' ' + name + ' not found.')
            else:
                self.data += [row]
        
        # read northing and easting from the row
        self.northing  = [year['Northing'].values[0]  for year in self.data]
        self.easting   = [year['Easting'].values[0]   for year in self.data]
        self.elevation = [year['Elevation'].values[0] for year in self.data]
        
        # try to read measurement errors from file
        # if not in file, use constant error

        self.sN        = []
        for year in self.data:
            try:
                self.sN += [year['sN'].values[0]]
            except KeyError:
                self.sN += [.2]

        self.sE        = []
        for year in self.data:
            try:
                self.sE += [year['sE'].values[0]]
            except KeyError:
                self.sE += [.2]

        print('Stake ' + title + ' initialized.')

      

#import IPython
#IPython.embed()

###############################################################################
# make a list of all stake objects
ss = [stake(s) for s in stakes]

labels = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8',
          'BL2', 'BL3', 'BL4', 'BL5']
labels = [label + ' \nElev. [m]' for label in labels]

# make a plot of the elevation of all stakes on tellbreen
f, axarr = plt.subplots(8, sharex=True, figsize=(6, 8.5), tight_layout=True)

# list for fitparams to be written to file
writeToFile = [['elevation', 'b', 'sb']]

for i, s in enumerate(ss[:8]):
    # make plotdata: drop nan from elevation, also drop matching year numbers,
    # and do some funny transposing... nan==nan -> False
    plotdata = np.array([[d,e] for d,e in zip(s.dates, s.elevation) if e==e]).T

    axarr[i].plot(plotdata[0], plotdata[1], '.')

    ylimsmean = np.mean(axarr[i].get_ylim())
    axarr[i].set_ylabel(labels[i])
    axarr[i].set_yticks(np.arange(0, 1000, 10))
    axarr[i].grid(axis='y')
    axarr[i].set_ylim([ylimsmean - 12, ylimsmean + 12])

    # FIT

    xdat = plotdata[0]
    ydat = plotdata[1]
    
    def pol_1st(x, a, b):
        return a + b*x

    popt, pcov = curve_fit(pol_1st, xdat, ydat)

    yfit = np.array([2000, 2020])
    axarr[i].plot(yfit, pol_1st(yfit, *popt), 'r-', linewidth=1,
     color='tab:red',
     label='$a=%1.0f\,$m, $b=%1.2f\,$m/a' % tuple(popt))

    writeToFile += [[
        '%1.1f' % np.mean(ydat),
        '%1.2f' % popt[1],
        '%1.2f' % np.sqrt(pcov[1][1])
        ]]

    axarr[i].legend()
    # plot data

    axarr[i].plot(plotdata[0], plotdata[1], '.', color='tab:blue')
    #axarr[i].plot(plotdata[0], plotdata[1], linewidth=.5, color='k')
    plotOpts(axarr[i])


axarr[0].set_xlim([2010.5, 2018.5])
axarr[0].set_xticks(range(2011, 2019))

f.savefig('../protocol/figs/Elevation_Tellbreen.pdf')

with open('../data/elevations/Tellbreen.txt', 'w') as f:
    for line in writeToFile:
        # use space as separator, dont write [, ] and '
        write = str(line).replace(',', '').replace('\'', '')[1:-1]
        f.write(write + '\n')
        
# EXPORT TABLE TO CSV
exp_tab = pd.DataFrame(writeToFile[1:], columns=['Elevation [m]', 'b', 'sb'])
# add column with names
exp_tab['Stake name'] = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8']
# make new column with \pm
exp_tab['Mass balance [m]'] = exp_tab.apply(lambda row: row[1] + ' $\pm$ ' + row[2], axis=1)
# choose three columns for export
exp_tab = exp_tab[['Stake name', 'Elevation [m]', 'Mass balance [m]']]
print(exp_tab)
# convert to latex format
exp_tab = exp_tab.to_latex(index=False, column_format='lcc', escape=False)

with open('../protocol/tables/mbal_tel.tex', 'w') as f:
    f.write(exp_tab)

###############################################################################
# make a plot of the elevation of all stakes on blekumbreen

# list for fitparams to be written to file
writeToFile = [['elevation', 'b', 'sb']]

f, axarr = plt.subplots(4, sharex=True, figsize=(6, 5), tight_layout=True)

for i, s in enumerate(ss[8:]):
    # make plotdata: drop nan from elevation, also drop matching year numbers,
    # and do some funny transposing... nan==nan -> False
    plotdata = np.array([[d,e] for d,e in zip(s.dates, s.elevation) if e==e]).T

    axarr[i].plot(plotdata[0], plotdata[1], '.')
    ylimsmean = np.mean(axarr[i].get_ylim())
    axarr[i].set_ylabel(labels[i+8])
    axarr[i].set_yticks(np.arange(0, 1000, 5))
    axarr[i].grid(axis='y')
    axarr[i].set_ylim([ylimsmean - 8, ylimsmean + 8])

    # FIT

    xdat = plotdata[0]
    ydat = plotdata[1]
    
    def pol_1st(x, a, b):
        return a + b*x

    popt, pcov = curve_fit(pol_1st, xdat, ydat)

    yfit = np.array([2000, 2020])
    axarr[i].plot(yfit, pol_1st(yfit, *popt), 'r-', linewidth=1,
     color='tab:red',
     label='Fit with $y=a+b x$ \n $a=%1.0f\,$m, $b=%1.2f\,$m/a' % tuple(popt))

    writeToFile += [[
        '%1.1f' % np.mean(ydat),
        '%1.2f' % popt[1],
        '%1.2f' % np.sqrt(pcov[1][1])
        ]]

    axarr[i].legend()
    # plot data

    axarr[i].plot(plotdata[0], plotdata[1], '.', color='tab:blue')
    #axarr[i].plot(plotdata[0], plotdata[1], linewidth=.5, color='k')
    plotOpts(axarr[i])
    

#import IPython
#IPython.embed()

axarr[0].set_xlim([2010.5, 2018.5])
axarr[0].set_xticks(range(2011, 2019))

f.savefig('../protocol/figs/Elevation_Blekumbreen.pdf')


with open('../data/elevations/Blekumbreen.txt', 'w') as f:
    for line in writeToFile:
        # use space as separator, dont write [, ] and '
        write = str(line).replace(',', '').replace('\'', '')[1:-1]
        f.write(write + '\n')



# EXPORT TABLE TO CSV
exp_tab = pd.DataFrame(writeToFile[1:], columns=['Elevation [m]', 'b', 'sb'])
# add column with names
exp_tab['Stake name'] = ['BL2', 'BL3', 'BL4', 'BL5']
# make new column with \pm
exp_tab['Mass balance [m]'] = exp_tab.apply(lambda row: row[1] + ' $\pm$ ' + row[2], axis=1)
# choose three columns for export
exp_tab = exp_tab[['Stake name', 'Elevation [m]', 'Mass balance [m]']]
print(exp_tab)
# convert to latex format
exp_tab = exp_tab.to_latex(index=False, column_format='lcc', escape=False)

with open('../protocol/tables/mbal_ble.tex', 'w') as f:
    f.write(exp_tab)


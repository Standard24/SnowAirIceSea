#!/usr/bin/env python

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.transforms as mtransforms
import pandas as pd
import numpy as np

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
                 [2014, 'T1-2012'], [2014, 'T1-2014'],
                 [2015, 'T1-2009'], [2015, 'T1-2014'], [2015, 'T1-2015'],
                 [2016, 'T1-2015'], [2016, 'T1-2016'],
                 [2017, 'T1-2016'], [2017, 'T1-2017'],
                 [2018, 'T1-i-2017'], [2018, 'T1-ii-2017'], [2018, 'T1-2018']],
          'T2': [[2011, 'T2-2009'], [2012, 'T2-2009'],
                 [2013, 'T2-2009'], [2014, 'T2-2009'],
                 [2015, 'T2-2009'], [2015, 'T2-2015'],
                 [2016, 'T2-2015'], [2016, 'T2-2016'],
                 [2017, 'T2-2016'], [2017, 'T2-2017'],
                 [2018, 'T2-2016'], [2018, 'T2-i-2017'], [2018, 'T2-ii-2017'],
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
                 [2018, 'T4-2016'], [2018, 'T4-2018']],
          'T5': [[2011, 'T5-2009'], [2012, 'T5-b2009'],
                 [2013, 'T5-2009'], [2014, 'T5-2012'],
                 [2015, 'T5-2009'], [2016, 'T5-2016'],
                 [2017, 'T5-2016'],
                 [2018, 'T5-2016'], [2018, 'T5-2018']],
          'T6': [[2011, 'T6-2009'],#[2012, 'T6-2009'], [2013, 'T6-2009'],
                 [2013, 'T6-2013'],
                 [2015, 'T6-2013'], [2016, 'T6-2016'],
                 [2017, 'T6-2016'],
                 [2018, 'T6-2016'], [2018, 'T6-2018']],
          'T7': [[2011, 'T7-2009'], [2012, 'T7-2009'], 
                 [2013, 'T7-2009'], [2014, 'T7-2009'],
                 [2015, 'T7-2009'], [2015, 'T7-2015'],
                 [2016, 'T7-2015'], [2017, 'T7-2015'], [2017, 'T7-2017'],
                 [2018, 'T7-2017'], [2018, 'T7-2015']],
          'T8': [[2011, 'T8-2009'], [2012, 'T8-2009'],
                 [2013, 'T8-2009'], [2014, 'T8-2009'],
                 [2015, 'T8-2009'], [2015, 'T8-2015'],
                 [2016, 'T8-2015'], [2016, 'T8-2016'],
                 [2017, 'T8-2016'], [2017, 'T8-2017'],
                 [2018, 'T8-2017']],
         'BL2': [[2012, 'BL2-2011'], [2013, 'BL2-2011'], [2014, 'BL2-2011'],
                 [2015, 'BL2-2011'],
                 [2016, 'BL2-2016'], [2017, 'BL2-2016'],
                 [2018, 'BL2-2016'], [2018, 'BL2-2018']],
         'BL3': [[2011, 'BL3-2011'],
                 [2012, 'BL3-2011'], [2013, 'BL3-2011'], [2014, 'BL3-2011'],
                 [2015, 'BL3-2011'], [2015, 'BL3-2015'],
                 [2016, 'BL3-2015'], [2016, 'BL3-2016'],
                 [2017, 'BL3-2015'], [2017, 'BL3-2016'],
                 [2018, 'BL3-2016'], [2018, 'BL3-2018']],
         'BL4': [[2012, 'BL4-2011'], [2013, 'BL4-2011'], [2014, 'BL4-2011'],
                 [2015, 'BL4-2011'], [2016, 'BL4-2016'], [2017, 'BL4-2016'],
                 [2018, 'BL4-i-2016'], [2018, 'BL4-ii-2016'],
                 [2018, 'BL4-2018']],
         'BL5': [[2011, 'BL5-2011'],
                 [2012, 'BL5-2011'], [2013, 'BL5-2011'], [2014, 'BL5-2011'],
                 [2015, 'BL5-2011'], [2016, 'BL5-2011'], [2017, 'BL5-2011'],
                 [2017, 'BL5-2017'],
                 [2018, 'BL5-i-2017'], [2018, 'BL5-ii-2017']]         
         }

# increase automatic plot limits for some plots in meters
# ((left, right), (bottom, top))
limits = {'T1' : ((.3, 0), (0, 0)),
          'T2' : ((1.5, 1.5), (0, 0)),
          'T3' : ((.1, .2), (0, .9)),
          'T4' : ((.5, .5), (0, 0)),
          'T5' : ((0, .5), (0, 0)),
          'T6' : ((0, 1), (0, 0)),
          'T7' : ((0, .2), (0, 0)),
          'T8' : ((.7, .7), (0, 0)),
          'BL2' : ((0, .2), (0, 0)),
          'BL3' : ((3, 1), (0, 0)),
          'BL4' : ((.7, 0), (0, 0)),          
          'BL5' : ((0, 0), (.3, 1))
          }

# list to move some year labels (dx, dy), up and right are positive
lu = (-.4, -.2) # left under
ru = ( .05, -.2) # right under
lo = (-.4,  .05) # left over
movelabs = {'T1': {3: lo, 5: ru, 9: lu, 11:lu, 12:lo},
            'T2': {1: lo, 3: lu, 4: lu, 5: lo, 6: ru, 8: ru, 11:lo},
            'T3': {2: lu, 3: ru, 5: ru, 6: lo, 8: ru},
            'T4': {1: lu, 2: lu, 5: lo, 7: lu},
            'T5': {0: ru, 1: ru, 2: lo, 3: ru, 5: lo},
            'T6': {0: (.05, -.5), 5: (-1.5, .05)},
            'T7': {3: ru, 5: lo},
            'T8': {0: ru, 1: lu, 2: (.05, -.07), 3: lo, 5: lo, 8: lu},                                    
            'BL2': {4: ru, 5: (.05, -.05)},
            'BL3': {0: ru, 4: ru, 5: ru, 7: (-.2, -.35), 9: (-.5, .1)},
            'BL4': {2: ru, 4: lo, 5: lu, 7: ru},
            'BL5': {8: ru}                         
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


###
# plot all stake positions 2d
###
f3 = plt.figure(figsize=(6, 3.1), tight_layout=True)

markers = ['+', 'x', ',', ',', '+', ',', 'v', '^', '.', '+']
colors = defcol[3:10] + defcol[:3]
markersizes = [10, 8, 8, 8, 8, 5, 5, 5, 5, 10]

for i, d in enumerate(data):
    # only take stakes in flow line
    d = d[d.Name.str.contains('T1|T2|T3|T4|T5|T6|T7|T8|BL2|BL3|BL4|BL5')]
    plt.plot(d['Easting'], d['Northing'], markers[i], label=time[i],
             color=colors[i], markersize=markersizes[i])

# write names of the stakes to some stakes
pos = [0, 1, 14, 2, 3, 4, 5, 6, 7, 8, 9, 11]  # position of the stakes to be labelled in the 2017 data
annotations = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8',
          'BL5', 'BL4', 'BL3', 'BL2']
for row, name in zip([data[-2].iloc[i] for i in pos], annotations):
    plt.annotate(name, (row['Easting'] - 100, row['Northing'] - 250))

plt.gca().set_aspect('equal')
plt.xlim([522600, 528900])
plt.ylim([8685100, 8688400])
plt.xlabel('Easting [m]')
plt.ylabel('Northing [m]')
plt.legend(ncol=2)
plotOpts(f3.gca())

plt.savefig('../protocol/figs/stakePositions.pdf')


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
                self.sN += [.4]

        self.sE        = []
        for year in self.data:
            try:
                self.sE += [year['sE'].values[0]]
            except KeyError:
                self.sE += [.19]

        print('Stake ' + title + ' initialized.')

    def makePlots(self):
        """ Save the following plots for the stake:
        - Time evaluation of the stake position
        - 2 dimensional movement of the stake
        """
        ###
        # plot time evaluation
        ###

        if len(self.dates) == len(self.northing):
            f, (ax1, ax2) = plt.subplots(2, figsize=(6, 4.5), dpi=80)

            # subplot of northing
            ax1.set_title('Time evolution of movement of ' + self.title)
            ax1.errorbar(self.dates, self.northing, yerr=self.sN, fmt='.',
                          capsize=3)
            ax1.plot(self.dates, self.northing, color='k', linewidth=.5)
            ax1.set_ylabel('Northing [m]')
            ax1.set_xticks([2011, 2012, 2013, 2014, 2015, 2016, 2017])
            ax1.set_xlim([2010.7, 2018.3])
            plotOpts(ax1)

            # subplot of easting
            ax2.errorbar(self.dates, self.easting, yerr=self.sE, fmt='.',
                         capsize=3)
            ax2.plot(self.dates, self.easting, color='k', linewidth=.5)
            ax2.set_ylabel('Easting [m]')
            ax2.set_xticks([2011, 2012, 2013, 2014, 2015, 2016, 2017])
            ax2.set_xlim([2010.7, 2018.3])
            plotOpts(ax2)

            plt.savefig('../fig/' + self.title + '_timeEvolution.pdf')
            plt.close(f)
        else:
            print('Could not plot time evaluation for ' + self.title)

        ###
        # plot 2d movement
        ###
        f = plt.figure(figsize=(6, 4.5), dpi=80, tight_layout=True)
        
        plt.gca().set_aspect('equal')
        plt.gca().ticklabel_format(useOffset=False)
        
        colors = [colordict[date[-4:]] for date in self.names]
        for x, y, sx, sy, c in zip(
                self.easting, self.northing, self.sE, self.sN, colors):
            plt.errorbar(x, y, xerr=sx, yerr=sy, fmt='.', color='k', ecolor=c)
        #plt.plot(self.easting, self.northing, color='k', linewidth=.5)

        plt.xlabel('Easting [m]')
        plt.ylabel('Northing [m]')

        # write year next to stake positions    
        for i, (year, x, y) in enumerate(zip(
            self.dates, self.easting, self.northing)):
            try:
                dx, dy = movelabs[self.title][i]
            except KeyError:
                dx, dy = (.05, .05)
                
            plt.annotate(year, (x + dx, y + dy))

        plotOpts(plt.gca())
        plt.legend(handles=patches)
        



        # if entry for stake is present in dict, change limits
        try:
            ylim_bot = plt.gca().get_ylim()[0] - limits[self.title][1][0]
            ylim_top = plt.gca().get_ylim()[1] + limits[self.title][1][1]
            plt.ylim(ylim_bot, ylim_top)
            xlim_lef = plt.gca().get_xlim()[0] - limits[self.title][0][0]
            xlim_rig = plt.gca().get_xlim()[1] + limits[self.title][0][1]
            plt.xlim(xlim_lef, xlim_rig)
        except KeyError:
            pass

        plt.savefig('../protocol/figs/' + self.title + '_2d.pdf')
        plt.close(f)
        print('Saved 2d plot of ' + self.title)

#import IPython
#IPython.embed()

###############################################################################
# make a list of all stake objects
ss = [stake(s) for s in stakes]

# make the plots of the class method
for s in ss:
    s.makePlots()


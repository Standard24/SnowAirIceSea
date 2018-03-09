#!/usr/bin/env python

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np


# define plot options
def plotOpts(ax):
    ax.tick_params(axis='both', which='both', direction='in', right=True,
                   top=True)

defcol = plt.rcParams['axes.prop_cycle'].by_key()['color']

# list of all the years we have data from
time = [2009, 2010, 2013, 2015, 2016, 2017]
# make a dictionary which assigns a number from 0-N to each year
t_d = dict(zip(time, range(len(time))))


filenames = ['2009_stake_coordinates',
             '2010_stake_coord_deg2utm',
             '2013_post-processed_UTM',
             '2015_stake_coordinates_deg2utm',
             '2016_stake_coordinates',
             '2017_stake_coordinates']

# import all csv files: Create a list of pandas data frames
data = [pd.read_csv('../data/stake_coordinates/' + filename
        + '.csv', sep=' ') for filename in filenames]

# print imported data
for i, t in enumerate(time):
    print('\n' + str(t) + ':')
    print(data[i])


# choose measurement error in meters
err = .2

# choose one title for each stake and make lists which contains the
# different names of the stake and the different years

titles = {'T1': [['T1-2009', 'T1-2009', 'T1-2014', 'T1-2015',
                  'T1-2015', 'T1-2016', 'T1-2016', 'T1-2017'],
                 [2013, 2015, 2015, 2015, 2016, 2016, 2017, 2017]],
          'T2': [['T2-2009', 'T2-2009', 'T2-2015', 'T2-2015', 'T2-2016',
                  'T2-2016', 'T2-2017'],
                 [2013, 2015, 2015, 2016, 2016, 2017, 2017]],
          'T3': [['T3-2012', 'T3-2012', 'T3-2015', 'T3-2015', 'T3-2017'],
                 [2013, 2015, 2015, 2016, 2017]],
          'T4': [['T4-2009', 'T4-2014', 'T4-2016', 'T4-2016'],
                 [2013, 2015, 2016, 2017]],
          'T5': [['T5-2009', 'T5-2009', 'T5-2016', 'T5-2016'],
                 [2013, 2015, 2016, 2017]],
          'T6': [['T6-2013', 'T6-2013', 'T6-2016', 'T6-2016'],
                 [2013, 2015, 2016, 2017]],
          'T7': [['T7-2009', 'T7-2009', 'T7-2015', 'T7-2015', 'T7-2015',
                  'T7-2017'],
                 [2013, 2015, 2015, 2016, 2017, 2017]],
          'T8': [['T8-2009', 'T8-2009', 'T8-2015', 'T8-2015', 'T8-2016',
                  'T8-2016', 'T8-2017'],
                 [2013, 2015, 2015, 2016, 2016, 2017, 2017]]}

stakes = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8']
colordict = {'2009':defcol[3], '2010':defcol[4], '2011':defcol[5],
             '2012':defcol[6], '2013':defcol[7], '2014':defcol[8],
             '2015':defcol[0], '2016':defcol[1], '2017':defcol[2]}
keys = list(colordict.keys())
values= list(colordict.values())

patches = [mpatches.Patch(color=c, label=y) for c, y in zip(values, keys)]
#red_patch = mpatches.Patch(color='red', label='The red data')


###############################################################################

###
# plot northings of all stakes for every year
###
f1 = plt.figure(figsize=(8, 6), dpi=80)
for i, d in enumerate(data):
    plt.plot(d['Northing'] + 20*i, '.', label=time[i])
    plt.plot(d['Northing'] + 20*i, color='k', linewidth=.5, label='')

plt.xlabel('Stake')
plt.ylabel('Northing / m')
plt.xticks(range(max([len(d) for d in data])))
plotOpts(f1.gca())
plt.legend()
plt.savefig('../fig/all_Northing.pdf')

###
# plot eastings of all stakes for every year
###
f2 = plt.figure(figsize=(8, 6), dpi=80)
for i, d in enumerate(data):
    plt.plot(d['Easting'] + 50*i, '.', label=time[i])
    plt.plot(d['Easting'] + 50*i, color='k', linewidth=.5, label='')

plt.xlabel('Stake')
plt.ylabel('Easting / m')
plt.xticks(range(max([len(d) for d in data])))
plotOpts(f2.gca())
plt.legend()
plt.savefig('../fig/all_Easting.pdf')

###
# plot all stake positions 2d
###
f3 = plt.figure(figsize=(8, 6), dpi=80)
markers = ['+', 'x', '+', 'v', '^', '.']

colors = defcol[3:6] + defcol[:3]
markersizes = [10, 8, 8, 5, 5, 5]
for i, d in enumerate(data):
    plt.plot(d['Easting'], d['Northing'], markers[i], label=time[i],
             color=colors[i], markersize=markersizes[i])

# write names of the stakes to some stakes
pos = [0, 1, 14, 2, 3, 4, 5, 6]  # position of the stakes to be labelled in the 2017 data
for row, name in zip([data[-1].iloc[i] for i in pos], stakes):
    plt.annotate(name, (row['Easting'] + 80, row['Northing']))

plt.gca().set_aspect('equal')
plt.xlim([522100, 528900])
plt.ylim([8685100, 8688400])
plt.xlabel('Easting / m')
plt.ylabel('Northing / m')
plt.legend()
plotOpts(f3.gca())

plt.savefig('../fig/stakePositions.pdf')


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
        self.names = titles[title][0]
        # get the years of the measurements
        self.dates = titles[title][1]
        # read the particular row(s) for the stake from each data frame
        self.data = [data[t_d[date]].loc[data[t_d[date]]['Name'] == name]
                     for date, name in zip(self.dates, self.names)]
        # read northing and easting from the row
        self.northing  = [year['Northing'].values[0]  for year in self.data]
        self.easting   = [year['Easting'].values[0]   for year in self.data]
        self.elevation = [year['Elevation'].values[0] for year in self.data]


    def makePlots(self):
        """ Save the following plots for the stake:
        - Time evaluation of the stake position
        - 2 dimensional movement of the stake
        """
        ###
        # plot time evaluation
        ###
        f, (ax1, ax2) = plt.subplots(2, sharex=True, figsize=(8, 6), dpi=80)

        # subplot of northing
        ax1.set_title('Time evolution of movement of ' + self.title)
        ax1.errorbar(self.dates, self.northing, yerr=err, fmt='.', capsize=3)
        ax1.plot(self.dates, self.northing, color='k', linewidth=.5)
        plotOpts(ax1)
        ax1.set_ylabel('Northing / m')

        # subplot of easting
        ax2.errorbar(self.dates, self.easting, yerr=err, fmt='.', capsize=3)
        ax2.plot(self.dates, self.easting, color='k', linewidth=.5)
        ax2.set_ylabel('Easting / m')
        ax2.set_xticks([2015, 2016, 2017])
        plotOpts(ax2)

        plt.savefig('../fig/' + self.title + '_timeEvolution.pdf')

        ###
        # plot 2d movement
        ###
        plt.figure(figsize=(8, 6), dpi=80)
        plt.gca().set_aspect('equal')

        
        colors = [colordict[date[-4:]] for date in self.names]
        for x, y, c in zip(self.easting, self.northing, colors):
            plt.errorbar(x, y, yerr=err, xerr=err, fmt='.', color=c)
        plt.plot(self.easting, self.northing, color='k', linewidth=.5)

        plt.xlabel('Easting / m')
        plt.ylabel('Northing / m')

        # write year next to stake positions    
        for year, x, y in zip(self.dates, self.easting, self.northing):
            plt.annotate(year, (x + .05, y + .05))

        plotOpts(plt.gca())
        plt.legend(handles=patches)
        plt.savefig('../fig/' + self.title + '_2d.pdf')




###############################################################################
# make a list of all stake objects
ss = [stake(s) for s in stakes]

# make the plots of the class method
for s in ss:
    s.makePlots()

# make a plot of the elevation of all stakes on tellbreen
f, axarr = plt.subplots(8, sharex=True)

for i, s in enumerate(ss):
    # make plotdata: drop nan from elevation, also drop matching year numbers,
    # and do some funny transposing... nan==nan -> False
    plotdata = np.array([[d,e] for d,e in zip(s.dates, s.elevation) if e==e]).T
    axarr[i].plot(plotdata[0], plotdata[1], '.')
    axarr[i].plot(plotdata[0], plotdata[1], linewidth=.5, color='k')
    plotOpts(axarr[i])
    axarr[i].set_ylabel(stakes[i])
    ylimsmean = np.mean(axarr[i].get_ylim())
    axarr[i].yaxis.set_label_position("right")
    axarr[i].set_yticks(np.arange(0,1000,5))
    axarr[i].grid(axis='y')
    

    
    # make more space on top and bottom: shift ylims by 1.5
    #ylims = axarr[i].get_ylim()
    #axarr[i].set_ylim([ylims[0] - 1.5, ylims[1] + 1.5])

    axarr[i].set_ylim([ylimsmean - 8, ylimsmean + 8])


axarr[0].set_xlim([2012.5, 2017.5])
axarr[0].set_xticks(range(2013, 2018))

f.savefig('../fig/all_Elevation.pdf')


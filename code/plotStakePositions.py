#!/usr/bin/env python

import matplotlib.pyplot as plt
import pandas as pd


# define plot options
def plotOpts(ax):
    ax.tick_params(axis='both', which='both', direction='in', right=True,
                   top=True)


# list of all the years we have data from
time = [2015, 2016, 2017]
# make a dictionary which assigns a number from 0-N to each year
t_d = dict(zip(time, range(len(time))))

# import all csv files: Create a list of pandas data frames
data = [pd.read_csv('../data/stake_coordinates/' + str(y)
        + '_stake_coordinates.csv', sep=' ') for y in time]

# print imported data
for i, t in enumerate(time):
    print('\n' + str(t) + ':')
    print(data[i])


# choose measurement error in meters
err = .2

# choose one title for each stake and make lists which contains the
# different names of the stake and the different years

titles = {'t1': [['t1_2015', 't1_2015', 't1-2016', 't1-2016', 't1-2017'],
                 [2015, 2016, 2016, 2017, 2017]],
          't2': [['t2_2015', 't2_2015', 't2-2016', 't2-2016', 't2-2017'],
                 [2015, 2016, 2016, 2017, 2017]],
          't7': [['t7_2015', 't7_2015', 't7-2015', 't7-2017'],
                 [2015, 2016, 2017, 2017]]}

stakes = ['t1', 't2', 't7']


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
markers = ['v', '^', '.']
for i, d in enumerate(data):
    plt.plot(d['Easting'], d['Northing'], markers[i], label=time[i])

# write names of the stakes to some stakes
pos = [0, 1, 5]  # position of the stakes to be labelled in the 2017 data
for row, name in zip([data[-1].iloc[i] for i in pos], stakes):
    plt.annotate(name, (row['Easting'] + 50, row['Northing'] + 50))

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
        # get the of the measurements
        self.dates = titles[title][1]
        # read the particular row(s) for the stake from each data frame
        self.data = [data[t_d[date]].loc[data[t_d[date]]['Name'] == name]
                     for date, name in zip(self.dates, self.names)]
        # read northing and easting from the row
        self.northing = [year['Northing'].values[0] for year in self.data]
        self.easting  = [year['Easting'].values[0]  for year in self.data]


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
        ax2.set_xticks(time)
        plotOpts(ax2)

        plt.savefig('../fig/' + self.title + '_timeEvolution.pdf')

        ###
        # plot 2d movement
        ###
        plt.figure(figsize=(8, 6), dpi=80)
        plt.gca().set_aspect('equal')

        plt.errorbar(self.easting, self.northing, yerr=err, xerr=err, fmt='.')
        plt.plot(self.easting, self.northing, color='k', linewidth=.5)

        plt.xlabel('Easting / m')
        plt.ylabel('Northing / m')

        # write year next to first and last data point
        plt.annotate(time[0], (self.easting[0] + .05,
                     self.northing[0] + .05))
        plt.annotate(time[-1], (self.easting[-1] + .05,
                     self.northing[-1] + .05))

        plotOpts(plt.gca())
        plt.savefig('../fig/' + self.title + '_2d.pdf')


# make and save plots for stakes in list
for s in stakes:
    stake(s).makePlots()

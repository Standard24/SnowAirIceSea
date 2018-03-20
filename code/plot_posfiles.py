#!/usr/bin/env python

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from coordinate_transformation2 import from_latlon
from read_posfiles import data_imp

dat = data_imp[0]

print(dat.describe())
utm = np.array([from_latlon(lat, lon) for lat, lon in zip(dat['latitude(deg)'], dat['longitude(deg)']) ]).T

print(np.mean(utm, axis=1))

east = utm[0,:]#+3*np.sin(1/20*(2*np.pi)*np.arange(len(utm[0])))
north = utm[1,:]
height = dat['height(m)']

print(np.std(east))
print(np.std(north))

f, (ax1, ax2, ax3) = plt.subplots(3, figsize=(11.5,6))
for ax, y in [(ax1, east), (ax2, north), (ax3, height)]:

    x=range(len(y))

    ax.plot(x, y)
    for N in [20, 50, 200]:
        ax.plot(x[int(N/2-1):-int(N/2)], np.convolve(y, np.ones((N,))/N, mode='valid'))

   
plt.savefig('../fig/00_Timeseries-east-north-elev.pdf')



f2, (ax1, ax2, ax3) = plt.subplots(3, figsize=(11.5,6))
for ax, dat in [[ax1, east], [ax2, north], [ax3, height]]:
    ax.hist(dat, 50)
plt.savefig('../fig/00_Histogram-east-north-elev.pdf')


f3, (ax1, ax2, ax3) = plt.subplots(3, figsize=(11.5,6))
for ax, dat in [[ax1, east], [ax2, north], [ax3, height]]:
    y = abs(np.fft.fft(dat))
    y = y[1:int(len(dat)/2)]
    x = 2*len(y) / np.arange(1, len(y)+1)
    ax.semilogx(x, y, '.')
    ax.semilogx(x, y, color='k', linewidth=.5)
    s = sorted(zip(x,y), key=lambda x: x[1])
    print()
    for p in s[:-10:-1]:
        print(p)


plt.savefig('../fig/00_Spectrum-east-north-elev.pdf')

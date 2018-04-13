#!/usr/bin/env python

import gpxpy
import gpxpy.gpx
import matplotlib.pyplot as plt
import numpy as np
from coordinate_transformation2 import from_latlon
from scipy.optimize import curve_fit

# Parsing an existing file:
# -------------------------


with open('../data/gpx_data/2018-03-15_14-20_tellbreen.gpx', 'r') as gpx_file:
    tellbreen = gpxpy.parse(gpx_file).tracks[0].segments[0].points
    
with open('../data/gpx_data/2018-03-15_11-57_blekumbreen.gpx', 'r') as gpx_file:
    blekumbreen = gpxpy.parse(gpx_file).tracks[0].segments[0].points

#for track in gpx.tracks:
#    for segment in track.segments:
#        for point in segment.points:
#            pass#print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))



tb_lats = [ point.latitude for point in tellbreen ]
#print(tb_lats)

tb_longs = [ point.longitude for point in tellbreen ]
#print(tb_longs)

tb_elev = [ point.elevation for point in tellbreen ]
#print(tb_elev)


bb_lats = [ point.latitude for point in blekumbreen ]
#print(bb_lats)

bb_longs = [ point.longitude for point in blekumbreen ]
#print(bb_longs)

bb_elev = [ point.elevation for point in blekumbreen ]
#print(bb_elev)


tb_coords = [from_latlon(*coord) for coord in zip(tb_lats, tb_longs)]
bb_coords = [from_latlon(*coord) for coord in zip(bb_lats, bb_longs)]

tb_easting = [coord[0] for coord in tb_coords]
tb_northing = [coord[1] for coord in tb_coords]
bb_easting = [coord[0] for coord in bb_coords]
bb_northing = [coord[1] for coord in bb_coords]

#print(tb_coords)

plt.plot(tb_easting, tb_elev, '.', markersize=1)
plt.plot(bb_easting, bb_elev, '.', markersize=1)

# FITS

def pol_1st(x, a, b):
    return a + b*x

# Blekumbreen
xdat = bb_easting
ydat = bb_elev
xfit = np.array([522500, 525000])

popt, pcov = curve_fit(pol_1st, xdat, ydat, p0=[1, 0.1])
sa = np.sqrt(pcov[0][0])
sb= np.sqrt(pcov[1][1])

print(popt)
print('Angle in rad: ' + str(np.arctan(popt[1])))
print('Unc on angle: ' + str(sb))
print('Angle in deg: ' + str(np.arctan(popt[1]) * 180/3.14))

plt.plot(xfit, pol_1st(xfit, *popt), 'r-', linewidth=1,
      color='tab:red',
      label='Fit with $y=a+x/b$ \n $a=%1.0f \pm %1.0f \,$m, $b=%1.1f \pm %1.1f \, $mm/m' 
      % tuple([popt[0], sa, popt[1], sb]))
      
      
# Tellbreen
xdat = tb_easting
ydat = tb_elev
xfit = np.array([525000, 529000])

popt, pcov = curve_fit(pol_1st, xdat, ydat, p0=[1, 0.1])
sa = np.sqrt(pcov[0][0])
sb= np.sqrt(pcov[1][1])


print(popt)
print('Angle in rad: ' + str(np.arctan(popt[1])))
print('Unc on angle: ' + str(sb))
print('Angle in deg: ' + str(np.arctan(popt[1]) * 180/3.14))

plt.plot(xfit, pol_1st(xfit, *popt), 'r-', linewidth=1,
      color='tab:red',
      label='Fit with $y=a+x/b$ \n $a=%1.0f \pm %1.0f \,$m, $b=%1.1f \pm %1.1f \, $mm/m' 
      % tuple([popt[0], sa, popt[1], sb]))
      


plt.savefig('../fig/Elevation_from_gpx.pdf')
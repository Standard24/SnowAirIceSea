#!/usr/bin/env python

import gpxpy
import gpxpy.gpx
import matplotlib.pyplot as plt

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

tb_longs = [ point.longitude for point in tellbreen ]
print(tb_longs)

tb_elev = [ point.elevation for point in tellbreen ]
print(tb_elev)

bb_longs = [ point.longitude for point in blekumbreen ]
print(bb_longs)

bb_elev = [ point.elevation for point in blekumbreen ]
print(bb_elev)

for l in tellbreen:
    print(l.speed)

plt.plot(tb_longs, tb_elev, '.', markersize=1)
plt.plot(bb_longs, bb_elev, '.', markersize=1)
plt.savefig('../fig/Elevation_from_gpx.pdf')
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 14:25:18 2022

@author: Dr. Ngoc Thinh Nguyen
"""

import numpy as np
import matplotlib.pyplot as plt

def laser_scan_extraction(raw_scan_range, range_min, range_max):
    # to transform a scan data into local XY coordinate system
    num_scan = len(raw_scan_range)
    # take value that >= range_min
    idx = np.where(raw_scan_range >= range_min)
    use_range = raw_scan_range[idx]
    # make all value that > range_max to range_max
    use_range = np.where(use_range > range_max, range_max, use_range)
    # create angle array
    angle = 2*np.pi/num_scan * idx[0]
    # x, y data: local
    x = use_range * np.cos(angle)
    y = use_range * np.sin(angle)
    return x, y

def plot_poly_map(ws, ax, col):
    # plot the whole polytope map in subplot ax with color col
    for i in range(len(ws)):
        x_de = [ws[i][k][0] for k in range(len(ws[i]))]
        x_de.append(ws[i][0][0])
        y_de = [ws[i][k][1] for k in range(len(ws[i]))]
        y_de.append(ws[i][0][1])
        ax.plot(x_de, y_de, color = col)
    return 0
"""
Part 1: extract local coordinates of obstacles
"""
# load data
raw_scan_range = np.loadtxt('./test_data/scan_data_1.dat')
# sensor info
range_min = 0.12 # in meters
range_max = 3.5 # in meters
# obstacles in local coordinate system
(x_obstacle, y_obstacle) = laser_scan_extraction(raw_scan_range, range_min, range_max)

# Initial and final poses:
init = [0.5, -1.]
goal = [2.5, -0.8]


""" 
# TODO: 
# E1: find the polytope map from the laser scan data
# E2: find sequence of polytopes leading from init to goal 
      for E2, should solve in file polytope_map_creation.py first.

"""



# this is a saved polytope map, just to plot, please comment it when you obtain your polytope map
with np.load("./test_data/map_1.npz", allow_pickle=True) as data:
    work_space = data['polytope_map']
# comment out 2 lines above.

fig = plt.figure()
ax = fig.add_subplot(111)
# plot scan data in local coordinate
ax.scatter(x_obstacle, y_obstacle, color = 'gray')
plt.scatter(init[0], init[1], color='red', s=20)
plt.scatter(goal[0], goal[1], color='blue', s=20)
plot_poly_map(work_space, ax, 'gray')
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 10:46:58 2021

@author: Dr. Ngoc Thinh Nguyen

Create a polytope map from a laser scan data

"""
import numpy as np
import matplotlib.pyplot as plt
from rdp import rdp
import gdspy
from poly_decomp import poly_decomp as pd

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

###     Part 1: extract local coordinates of obstacles
# load data
raw_scan_range = np.loadtxt('./test_data/scan_data_3.dat')
# sensor info
range_min = 0.12 # in meters
range_max = 3.5 # in meters
# obstacles in local coordinate system
(x_obstacle, y_obstacle) = laser_scan_extraction(raw_scan_range, range_min, range_max)

###     Part 2: Apply RDP algorithm
simplification_result = rdp([(x_obstacle[i], y_obstacle[i]) for i in range(len(x_obstacle))], epsilon = 0.1)
simplification_result_np = np.array(simplification_result)
x_rdp = simplification_result_np[:, 0]
y_rdp = simplification_result_np[:, 1]

###     Part 3: Create outer polygon and making offset
P = gdspy.Polygon(simplification_result)
offset_distance = 0.1 # in meters
offset_operation = gdspy.offset(P, - offset_distance)
offset_result = offset_operation.polygons[0]
# adding the first element at the end to close the boundary for plotting
offset_result_plot = np.append(offset_result, [offset_result[0]], axis = 0)

###     Part 4: Decompose outer polygon into connected polytopes
decompose_result = pd.polygonQuickDecomp(offset_result)


# Initial and final poses:
init = [1., 2.5]
goal = [1.5, 0.]

# TODO after

fig = plt.figure()
ax = fig.add_subplot(111)
# plot scan data in local coordinate
ax.scatter(x_obstacle, y_obstacle, color = 'gray')
# plot rdp result
ax.scatter(x_rdp, y_rdp, color='r')
ax.plot(x_rdp, y_rdp, 'black')
# plot outer polygon after offset operation
ax.plot(offset_result_plot[:, 0], offset_result_plot[:, 1], color='green', linewidth = 2)
# plot decompose result
plot_poly_map(decompose_result, ax, 'gray')
# plot two points
# plt.scatter(init[0], init[1], color='red', s=20)
# plt.scatter(goal[0], goal[1], color='blue', s=20)

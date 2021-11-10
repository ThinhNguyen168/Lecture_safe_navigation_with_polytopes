# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 15:36:25 2021

@author: Dr. Ngoc Thinh Nguyen

Create the scenario used for exercise 2
"""

import numpy as np
import matplotlib.pyplot as plt
import gdspy
from poly_decomp import poly_decomp as pd


def plot_poly_map(ws, ax, col):
    # plot the whole polytope map in subplot ax with color col
    for i in range(len(ws)):
        x_de = [ws[i][k][0] for k in range(len(ws[i]))]
        x_de.append(ws[i][0][0])
        y_de = [ws[i][k][1] for k in range(len(ws[i]))]
        y_de.append(ws[i][0][1])
        ax.plot(x_de, y_de, color = col)
    return 0

ws_limit = [[0,0], [2,0], [2,2], [0,2]]
obstacle1 = [[0.5, 0.5], [1.2, 0.4], [1., 0.7], [1., 1.3]]
obstacle2 = [[1.8, 1.], [1.6, 0.9], [1.5, 1.5], [1.8, 1.7]]
obstacle3 = [[0.2, 1.3], [0.5, 1.4], [0.4, 1.7], [0.3, 1.6]]

ws_poly = gdspy.Polygon(ws_limit)
hole1 = gdspy.Polygon(obstacle1)
hole2 = gdspy.Polygon(obstacle2)
hole3 = gdspy.Polygon(obstacle3)
# enlarge obstacle a little bit
safety_offset = 0.05
hole1_large = gdspy.offset(hole1, safety_offset)
hole2_large = gdspy.offset(hole2, safety_offset)
hole3_large = gdspy.offset(hole3, safety_offset)
# subtraction
poly_with_hole = gdspy.boolean(ws_poly, [hole1_large, hole2_large, hole3_large], "not")
# decomposition
ws = pd.polygonQuickDecomp(poly_with_hole.polygons[0])

# initial pose and final goal
init = [1.9, 1.5]
goal = [0.25, 1.]


"""    
# TODO: now find the sequence of polytopes

def generate_sequence(workspace, init, goal):
    sequence = []
    return sequence

sequence = generate_sequence(ws, init, goal) 


 
"""

# result
sequence = [4, 5, 6, 8]



fig = plt.figure()
ax = fig.add_subplot(111)
plot_poly_map(ws, ax, 'black')
plot_poly_map([obstacle1, obstacle2, obstacle3], ax, 'blue')
plt.scatter(init[0], init[1], color='red', s=20)
plt.scatter(goal[0], goal[1], color='blue', s=20)
plot_poly_map([ws[i] for i in sequence], ax, 'red')
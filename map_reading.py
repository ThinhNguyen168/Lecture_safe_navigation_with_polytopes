# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 10:21:45 2021

@author: Dr. Ngoc Thinh Nguyen

Display a grid map, saved as .npy file
Load a polytope map, saved as .npz file

"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

def plot_poly_map(ws, ax, col):
    # plot the whole polytope map in subplot ax with color col
    for i in range(len(ws)):
        x_de = [ws[i][k][0] for k in range(len(ws[i]))]
        x_de.append(ws[i][0][0])
        y_de = [ws[i][k][1] for k in range(len(ws[i]))]
        y_de.append(ws[i][0][1])
        ax.plot(x_de, y_de, color = col)
    return 0


# load the .npy map file in folder test_data 
data = np.load("./test_data/turtle.npy") 
# there are 3 values in grid map: 0 free, 100 obstacle, -1 unexplored 
# For more clarity, we will replace the obstacle's value by 1 instead of 100
data[data==100] = 1
colormap = colors.ListedColormap(["gray","white","black"])
fig = plt.figure()
ax = fig.add_subplot(111)
plt.imshow(np.transpose(data), cmap=colormap)

# now load the polytope map 
with np.load("./test_data/poly_map_turtle.npz", allow_pickle=True) as data:
    work_space = data['polytope_map']
# plot the polytope map within the grid map
plot_poly_map(work_space, ax, 'red')


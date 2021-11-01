# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 15:27:00 2021

@author: Dr. Ngoc Thinh Nguyen

Solution of Exercise E4 with minimal-length objective [Stoican et al. 2015]
"""

import numpy as np
import matplotlib.pyplot as plt
import pyomo.environ as pyo
from pyomo.opt import SolverFactory
from scipy import interpolate
from navigation_bspline import bspline_matrix as bspl

# starting and ending:
start_point = [0, 0]
end_point = [3, 0]
# connected polytopes:
m = 3
A1 = [[1, 0], [-1, 0], [0, 1], [0, -1]]
B1 = [1, 1, 2.5, 1]
A2 = [[1, 0], [-1, 0], [0, 1], [0, -1]]    
B2 = [4, -1, 2.5, -1] 
A2 = [[1, 0], [-1, 0], [0, 1], [0, -1]]            
B3 = [4, -2, 1, 1]  
# Transition zones:
A_T1 = [[1, 0], [-1, 0], [0, 1], [0, -1]]             
B_T1 = [1, 1, 2.5, -1]  
A_T2 = [[1, 0], [-1, 0], [0, 1], [0, -1]]             
B_T2 = [4, -2, 2.5, -1]

# degree of Bspline
d = 2
# number of control points
npoint = m + (m-1) * d

model = pyo.ConcreteModel()
model.d = pyo.Param(initialize=d)
model.constraints = pyo.ConstraintList()
model.x = pyo.Var(range(npoint)) # 0, 1, ..., npoint-1
model.y = pyo.Var(range(npoint)) # 0, 1, ..., npoint-1
# first point- initial condition
model.constraints.add(model.x[0] == start_point[0])
model.constraints.add(model.y[0] == start_point[1])
# end point - reference
model.constraints.add(model.x[npoint-1] == end_point[0])
model.constraints.add(model.y[npoint-1] == end_point[1])

# d point in transition zone T1:
for i in range(d):
    for j in range(len(B_T1)):
        lhs = A_T1[j][0] * model.x[i+1] + A_T1[j][1] * model.y[i+1]
        model.constraints.add(lhs <= B_T1[j])

# 1 point in 2nd polytope:
for j in range(len(B2)):
    lhs = A2[j][0] * model.x[d+1] + A2[j][1] * model.y[d+1]
    model.constraints.add(lhs <= B2[j]) 
# d point in transition zone T2:
for i in range(d):
    for j in range(len(B_T2)):
        lhs = A_T2[j][0] * model.x[i+d+2] + A_T2[j][1] * model.y[i+d+2]
        model.constraints.add(lhs <= B_T2[j])

def _obj(model):
    # The objective function to minimize the integral of square length
    # Stoican et al. (MED 2015), Nguyen et al. (IJC 2020) and Nguyen et al. (IROS 2021)
    d = model.d.value
    n = len(model.x)

    M = bspl.derivative_M(d,n)
    point_dx = []
    point_dy = []
    for i in range(len(M[0])):
        sum_x = 0
        sum_y = 0
        for j in range(n):
            sum_x += M[j][i] * model.x[j]
            sum_y += M[j][i] * model.y[j]
        point_dx.append(sum_x)
        point_dy.append(sum_y)
    cost = 0
    filename = './navigation_bspline/integral_data/d_' + str(d) +'n_' + str(n) +'.npy'
    integral_matrix = np.load(filename)
    for i in range(n-1):
        for j in range(n-1):
            cost += (point_dx[i]*point_dx[j]+ point_dy[i]*point_dy[j]) * integral_matrix[i][j]
    return cost

model.obj = pyo.Objective(rule=_obj, sense=pyo.minimize)
SolverFactory('ipopt').solve(model)

ctrl_x=[]
ctrl_y=[]
for i in range(npoint):
    ctrl_x.append(model.x[i].value)
    ctrl_y.append(model.y[i].value)
    
knot_vector=np.linspace(0,1,npoint+1-d,endpoint=True)
knot_vector=np.append([0]*d,knot_vector)
knot_vector=np.append(knot_vector,[1]*d)
tck=[knot_vector,[ctrl_x, ctrl_y], d] # define a Bspline function as required by scipy
# calculate Bspline 
t=np.linspace(0,1,(max(npoint*2,100)),endpoint=True)
out = interpolate.splev(t,tck)

# plotting
obstacle1 = np.array([[1, -1], [1, 1], [2, 1], [2, -1], [1, -1]])
plt.figure()
plt.plot(obstacle1[0:2,0],obstacle1[0:2,1],'red',linewidth=2.0)
plt.plot(obstacle1[1:3,0],obstacle1[1:3,1],'green',linewidth=2.0)
plt.plot(obstacle1[2:4,0],obstacle1[2:4,1],'blue',linewidth=2.0)
plt.plot(obstacle1[3:5,0],obstacle1[3:5,1],'black',linewidth=2.0)
plt.scatter(ctrl_x, ctrl_y, color='gray', s= 70, label='Control points')
plt.plot(out[0],out[1],'magenta',linewidth=2.0,label='Second-order B-spline curve')
plt.legend(loc='best')
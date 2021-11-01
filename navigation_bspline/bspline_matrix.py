# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 14:54:55 2020

@author: DELL
"""
import numpy as np
from scipy import interpolate
# Calculate the M_d,d-1(N+1, d)

def knot_vector(d, n, t0, tf):
    knot=np.linspace(t0, tf, n-d+1, endpoint=True)
    knot=np.append([t0]*d, knot)
    knot=np.append(knot, [tf]*d)
    return knot

def derivative_M(d,n,t0=0, tf=1):
    tau = knot_vector(d, n, t0, tf)
    N = n-1
    M = np.zeros((N,N+1))
    for i in range(N):
        M[i][i] = -d/(tau[i+d+1]-tau[i+1])
        M[i][i+1] = d/(tau[i+d+1]-tau[i+1])
    return M.transpose()

def b_spline_derivative_basis_function(d, n, t0=0, tf=1):
    tau = knot_vector(d, n, t0, tf)
    tau_new = tau[1:-1]
    basis_function = []
    for i in range(n-1):
        ctr_point = [0]*(n-1)
        ctr_point[i] = 1.
        spl = interpolate.BSpline(tau_new, ctr_point, d-1) 
        basis_function.append(spl)
    return basis_function

def b_spline_basis_function(d, n, t0=0, tf=1):
    tau = knot_vector(d, n, t0, tf)
    basis_function = []
    for i in range(n):
        ctr_point = [0]*n
        ctr_point[i] = 1.
        spl = interpolate.BSpline(tau, ctr_point, d) 
        basis_function.append(spl)
    return basis_function
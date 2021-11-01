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

def integrate_of_two_bspline_function(spl_1, spl_2, tstart, tend):
    numpoint = 100
    dt = (tend-tstart)*1./numpoint
    integral = 0
    for i in range(numpoint):
        integral += dt * spl_1(tstart + i * dt) * spl_2(tstart + i * dt)
    return integral

def intergrate_of_b_spline_derivative_basis_function(d, n, t0=0, tf=1):
    ctr_point = [0]*n
    tau = knot_vector(d, n, t0, tf)
    tau_new = tau[1:-2]
    integral = []
    for i in range(n-1):
        ctr_point = [0]*(n-1)
        ctr_point[i] = 1.
        spl = interpolate.BSpline(tau_new, ctr_point, d-1) 
        integral.append(spl.integrate(t0, tf, extrapolate=False))
    return integral

def time_of_control_points(d, n, t0=0, tf=1.):
    #time_check = np.linspace(t0, tf, n-d+1, endpoint=True)
    #time_check = time_check + (tf-t0)/(n-d)/2.
    #time_check = time_check[:-1]
    # time_check = np.linspace((tf-t0)/(n-d)/2, 1.-(tf-t0)/(n-d)/2, n-2)
    time_check = np.linspace(t0 + (tf-t0)*0.1, tf - (tf-t0)*0.1, n-2)
    # print('Time check: ', time_check)
    basis_ft = b_spline_basis_function(d, n, t0, tf)
    #print('Number of basis functions: ', len(basis_ft))
    lhs = np.zeros((n-2, n-2))
    rhs = np.zeros((n-2, 1))
    for i in range(n-2):
        t = time_check[i]
        rhs[i] = t - t0 * basis_ft[0](t) - tf * basis_ft[-1](t)
        for j in range(n-2):
            lhs[i][j] = basis_ft[j+1](t)
    result = np.dot(np.linalg.inv(lhs), rhs)
    result = result.transpose()
    result = np.append(t0, result)
    result = np.append(result, tf)
    return result


def comparable_control_points(d, ctrl, interval, t0=0., tf=1.):
    n = len(ctrl)
    knot = knot_vector(d, n, t0, tf)
    time = np.linspace(t0, tf, n-d+1, endpoint=True)
    original_ft = interpolate.BSpline(knot, ctrl, d)
    # knot_new = knot_vector(d, d+1, time[interval-1], time[interval])
    new_basis_ft = b_spline_basis_function(d, d+1, time[interval-1], time[interval])
    lhs = np.zeros((d+1, d+1))
    rhs = np.zeros((d+1, 1))
    dt = time[interval] - time[interval-1]
    time_check = np.linspace(time[interval-1]+0.1*dt, time[interval]-0.1*dt, d+1)
    for i in range(d+1):
        t = time_check[i]
        rhs[i] = original_ft(t) 
        for j in range(d+1):
            lhs[i][j] = new_basis_ft[j](t)
    result = np.dot(np.linalg.inv(lhs), rhs)
    result = result.transpose().tolist()
    return result[0]


def coefficient_fake_control_points(d, n, interval_index):
    #n = 3*d # to ensure the second interval has left and right nodes
    
    # need to perform d+1 test:
    ctrl = []
    ctrl_n = []
    import random
    for i in range(d+1):
        ctrl.append(random.sample(range(0, 100), n))
        ctrl_n.append(comparable_control_points(d, ctrl[i], interval_index))
    
    
    # depends on d+1 ctrl points, from 1-> d+2
    coefficients = []
    for i in range(d+1):
        lhs = []
        rhs = []
        for j in range(d+1):
            lhs.append(ctrl[j][(interval_index-1):(d+interval_index)])
            rhs.append([ctrl_n[j][i]])
        lhs = np.array(lhs)
        rhs = np.array(rhs)
        result = np.dot(np.linalg.inv(lhs), rhs)
        result = result.transpose().tolist()
        coefficients.append(result[0])
    return coefficients

def bspline_to_bezier_conversion_complete(d):
    results = [coefficient_fake_control_points(d, 3*d, 1)]
    for i in range(3*d-d-1):
        new_coefficient = coefficient_fake_control_points(d, i+2)
        if np.sum(np.abs(np.array(results[-1]) - np.array(new_coefficient))) > 0.01:
            results.append(new_coefficient)
    return results

def bspline_to_bezier_conversion_each_interval(d, n):
    results = [coefficient_fake_control_points(d, n, 1)]
    for i in range(n-d-1):
        new_coefficient = coefficient_fake_control_points(d, n, i+2)
        results.append(new_coefficient)
    return results

def bspline_to_bezier_conversion(d, n):
    results= []
    tmp = coefficient_fake_control_points(d, n, 1)
    for line in tmp:
        line = line + [0.] * (n-d-1)
        results.append(line)
    for i in range(n-d-1):
        tmp = coefficient_fake_control_points(d, n, i+2)
        new_coefficient = tmp[1:]
        for line in new_coefficient:
            line = [0.] * (i+1) + line + [0.] * (n-d-1-i-1)
            results.append(line) 
    return results



#test = bspline_to_bezier_conversion(2, 5)
#for solution in test:
    #for i in solution: 
   #print(np.around(solution, 10))
    #print('')
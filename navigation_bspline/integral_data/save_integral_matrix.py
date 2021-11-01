# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 21:29:44 2020

@author: DELL
"""

import time
import numpy as np
import bspline_matrix as bspl


d = 2
for n in range(30,40,1):
    start = time.time()
    basis_derivative_functions = bspl.b_spline_derivative_basis_function(d, n)
    integral_value = np.zeros((n-1, n-1))
    for i in range(n-1):
        for j in range(n-1):
            integral_value[i][j] = bspl.integrate_of_two_bspline_function(basis_derivative_functions[i], basis_derivative_functions[j], 0, 1)
    #print('Integral value: ', integral_value)
    print('Cost calculation time: ', (time.time()-start)*1000, 'ms')
    filename = 'd_' + str(d) + 'n_' + str(n) +'.npy'
    np.save(filename, integral_value)
    
d = 3
for n in range(30,40,1):
    start = time.time()
    basis_derivative_functions = bspl.b_spline_derivative_basis_function(d, n)
    integral_value = np.zeros((n-1, n-1))
    for i in range(n-1):
        for j in range(n-1):
            integral_value[i][j] = bspl.integrate_of_two_bspline_function(basis_derivative_functions[i], basis_derivative_functions[j], 0, 1)
    #print('Integral value: ', integral_value)
    print('Cost calculation time: ', (time.time()-start)*1000, 'ms')
    filename = 'd_' + str(d) + 'n_' + str(n) +'.npy'
    np.save(filename, integral_value)
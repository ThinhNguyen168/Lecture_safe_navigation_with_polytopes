# Lecture on safe navigation with polytopes
The folder contains three execution files:
1) laserscan_reading: to read a laser scan data (samples can be found in test_data) and create a polytope map within the local free space.
2) map_reading: to read the grid map (turtle.npy in test_data) and its polytope map (poly_map_turtle.npz), then, display them together.
3) bspline_path_planner_minimal_length: a Bspline path planner in a predefined sequence of polytopes. The objective is to minimize the integral of the square of velocity. 


Folder poly_decomp contains the libarary for decomposing a polygon into polytopes.

Installation guild:
1) Install Anaconda environment from https://www.anaconda.com/
2) Open Anaconda Prompt
3) Install IPOPT solver: conda install -c conda-forge ipopt=3.11.1 
5) Install Pyomo interface: conda install -c conda-forge pyomo 
6) pip install numpy 
7) pip install scipy 
8) pip install rdp 
9) pip install gdspy
10) pip install matplotlib 

Paper:

Ngoc Thinh Nguyen, et al. B-spline path planner for safe navigation of mobile robots, in 2021 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), pp. 316-322, 2021.








  

# Lecture_safe_navigation_with_polytopes
The folder contains three execution files:
1) laserscan_reading: to read a laser scan data (samples can be found in test_data) and create a polytope map within the local free space.
2) map_reading: to read the grid map (turtle.npy in test_data) and its polytope map (poly_map_turtle.npz), then, display them together.
3) bspline_path_planner_minimal_length: a Bspline path planner in a predefined sequence of polytopes. The objective is to minimize the integral of the square of velocity. 
Folder poly_decomp contains the libarary for decomposing a polygon into polytopes.
Installation guild:
1) Install Anaconda environment from https://www.anaconda.com/
![image](https://user-images.githubusercontent.com/18294000/139742600-5644bbf8-6291-4929-be68-78e9f2006f56.png)
  

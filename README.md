# Lecture_safe_navigation_with_polytopes
The folder contains three execution files:
1) laserscan_reading: to read a laser scan data (samples can be found in test_data) and create a polytope map within the local free space.
2) map_reading: to read the grid map (turtle.npy in test_data) and its polytope map (poly_map_turtle.npz), then, display them together.
3) bspline_path_planner_minimal_length: a Bspline path planner in a predefined sequence of polytopes. The objective is to minimize the integral of the square of velocity. 
Folder poly_decomp contains the libarary for decomposing a polygon into polytopes.

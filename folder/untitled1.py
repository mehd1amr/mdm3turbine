#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 13:11:28 2025

@author: mehdiamara
"""

import numpy as np

# Geometry of the structure (2D right triangle)
# Coordinates of the vertices
A = np.array([0, 0])      # Bottom-left (Float 1)
B = np.array([100, 0])    # Bottom-right (Float 2)
C = np.array([100, 50])   # Top (supporting turbines)

# Properties
beam_weight = 1000 * 9.81  # Weight of each beam (N)
turbine_weight = 500 * 9.81  # Weight of each turbine (N)

# Lengths of beams
AB = np.linalg.norm(B - A)
AC = np.linalg.norm(C - A)
BC = np.linalg.norm(C - B)

# Apply loads
# Beam loads (uniformly distributed)
load_AB = beam_weight / AB  # N/m
load_AC = beam_weight / AC  # N/m
load_BC = beam_weight / BC  # N/m

# Turbine loads (point loads at C)
point_load_C = 2 * turbine_weight  # Both turbines are at point C

# Static equilibrium equations
# ∑F_x = 0, ∑F_y = 0, ∑M_A = 0
# Unknowns: Reaction forces at A (Ax, Ay) and B (Bx, By)

# Moments about A
moment_A = (
    (load_AB * AB * (AB / 2))  # Beam AB's moment about A
    + (load_AC * AC * (AC / 2))  # Beam AC's moment about A
    + (point_load_C * C[0])  # Turbine point load's moment about A
)

# Vertical force equilibrium
total_vertical_load = (beam_weight * 3) + point_load_C
Ay = moment_A / B[0]  # Solve for Ay using moment equilibrium
By = total_vertical_load - Ay  # Solve for By using ∑F_y = 0

# Horizontal force equilibrium
Ax = 0  # No horizontal forces in this problem
Bx = 0  # No horizontal forces in this problem

# Results
print("Reaction forces:")
print(f"Ax = {Ax:.2f} N")
print(f"Ay = {Ay:.2f} N")
print(f"Bx = {Bx:.2f} N")
print(f"By = {By:.2f} N")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 13:13:09 2025

@author: mehdiamara
"""

import numpy as np
import matplotlib.pyplot as plt

# Geometry of the structure (2D right triangle)
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
load_AB = beam_weight / AB  # N/m
load_AC = beam_weight / AC  # N/m
load_BC = beam_weight / BC  # N/m
point_load_C = 2 * turbine_weight  # Both turbines at point C

# Solve for reaction forces using static equilibrium
moment_A = (
    (load_AB * AB * (AB / 2))  # Beam AB's moment about A
    + (load_AC * AC * (AC / 2))  # Beam AC's moment about A
    + (point_load_C * C[0])  # Turbine point load's moment about A
)
total_vertical_load = (beam_weight * 3) + point_load_C
Ay = moment_A / B[0]  # Solve for Ay using moment equilibrium
By = total_vertical_load - Ay  # Solve for By using ∑F_y = 0
Ax = 0  # No horizontal forces
Bx = 0  # No horizontal forces

# Visualization
fig, ax = plt.subplots(figsize=(8, 6))

# Plot the triangle
ax.plot([A[0], B[0]], [A[1], B[1]], 'k-', label='Beam AB')
ax.plot([A[0], C[0]], [A[1], C[1]], 'k-', label='Beam AC')
ax.plot([B[0], C[0]], [B[1], C[1]], 'k-', label='Beam BC')

# Plot floats
ax.scatter(*A, color='blue', s=100, label='Float 1 (A)')
ax.scatter(*B, color='blue', s=100, label='Float 2 (B)')
ax.scatter(*C, color='red', s=100, label='Turbine (C)')

# forces
ax.annotate(f"Ay = {Ay:.2f} N", (A[0], A[1] + 2), color='green', fontsize=10)
ax.annotate(f"By = {By:.2f} N", (B[0], B[1] + 2), color='green', fontsize=10)
ax.annotate(f"Point Load = {point_load_C:.2f} N", (C[0] + 5, C[1] - 5), color='red', fontsize=10)

# Add labels and grid
ax.set_xlabel("X-axis (m)")
ax.set_ylabel("Y-axis (m)")
ax.set_title("2D Structural Model with Forces")
ax.grid(True)
ax.legend()
plt.axis('equal')
plt.show()

#####################################################
# Visualization of Distributed Forces
def plot_distributed_load(ax, start, end, load_per_unit_length, n=10):
    x = np.linspace(start[0], end[0], n)
    y = np.linspace(start[1], end[1], n)
    dx = (end[0] - start[0]) / n
    dy = (end[1] - start[1]) / n
    for i in range(n):
        ax.arrow(x[i], y[i], 0, -load_per_unit_length * 0.001, head_width=2, color='orange')

# Distributed load visualization
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot([A[0], B[0]], [A[1], B[1]], 'k-', label='Beam AB')
ax.plot([A[0], C[0]], [A[1], C[1]], 'k-', label='Beam AC')
ax.plot([B[0], C[0]], [B[1], C[1]], 'k-', label='Beam BC')

# Add distributed load arrows
plot_distributed_load(ax, A, B, load_AB)
plot_distributed_load(ax, A, C, load_AC)
plot_distributed_load(ax, B, C, load_BC)

# Display plot
ax.set_xlabel("X-axis (m)")
ax.set_ylabel("Y-axis (m)")
ax.set_title("2D Structural Model with Distributed Loads")
ax.grid(True)
ax.legend()
plt.axis('equal')
plt.show()


######################## Beam AB
x_positions = np.linspace(0, AB, 100)  # Divide the beam into 100 segments
shear_forces = load_AB * (AB - x_positions)  # Shear force varies linearly
bending_moments = (load_AB * x_positions * (AB - x_positions)) / 2  # Parabolic distribution

# Plotting the results
plt.figure(figsize=(10, 6))
plt.plot(x_positions, shear_forces, label='Shear Force (N)')
plt.plot(x_positions, bending_moments, label='Bending Moment (N·m)')
plt.xlabel('Beam Length (m)')
plt.ylabel('Force / Moment')
plt.title('Shear Force and Bending Moment Distribution')
plt.legend()
plt.grid()
plt.show()



################
from scipy.integrate import solve_ivp

# Define parameters
m = 1e6  # Mass in kg
c = 5e3  # Damping coefficient in N·s/m
k = 1e7  # Stiffness in N/m

# Define external force as a function of time
def external_force(t):
    return 1e6 * np.sin(2 * np.pi * 0.1 * t)  # Sinusoidal force

# Define the equation of motion
def equation_of_motion(t, y):
    x, v = y  # Position and velocity
    dxdt = v
    dvdt = (external_force(t) - c * v - k * x) / m
    return [dxdt, dvdt]

# Initial conditions
initial_conditions = [0, 0]  # Initial displacement and velocity

# Solve the system
time_span = (0, 60)  # 60 seconds
time_eval = np.linspace(0, 60, 1000)  # Time points
solution = solve_ivp(equation_of_motion, time_span, initial_conditions, t_eval=time_eval)

# Plot results
plt.figure(figsize=(10, 6))
plt.plot(solution.t, solution.y[0], label='Displacement (m)')
plt.plot(solution.t, solution.y[1], label='Velocity (m/s)')
plt.xlabel('Time (s)')
plt.ylabel('Response')
plt.title('Dynamic Response of the Structure')
plt.legend()
plt.grid()
plt.show()


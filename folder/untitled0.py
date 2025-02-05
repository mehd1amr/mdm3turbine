#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 13:07:19 2025

@author: mehdiamara
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Define the base of the isosceles triangle
base_vertices = np.array([
    [0, 0, 0],       # Corner 1
    [2, 0, 0],       # Corner 2
    [1, np.sqrt(3), 0]  # Corner 3 (top of the triangle)
])

# Define the beams' endpoints
beam1_top = np.array([0.5, 0, 2])  # Top of the first vertical beam
beam2_top = np.array([1.5, 0, 2])  # Top of the second vertical beam

# Define the middle point of the bottom beam
middle_bottom = np.array([1, 0, 0])

# Create the beams connecting the vertices
beams = [
    [base_vertices[0], beam1_top],  # Beam from Corner 1 to Beam 1
    [base_vertices[1], beam2_top],  # Beam from Corner 2 to Beam 2
    [beam1_top, beam2_top],         # Horizontal beam linking the two vertical beams
    [beam1_top, middle_bottom],     # Diagonal beam from Beam 1 to middle of bottom
    [beam2_top, middle_bottom],     # Diagonal beam from Beam 2 to middle of bottom
    [base_vertices[2], beam1_top],  # Diagonal Beam from Corner 3 to Beam 1
    [base_vertices[2], beam2_top]   # Diagonal Beam from Corner 3 to Beam 2
]

# Visualization
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot the base of the triangle
ax.scatter(base_vertices[:, 0], base_vertices[:, 1], base_vertices[:, 2], color='blue', label='Base vertices')
for i in range(len(base_vertices)):
    ax.plot(
        [base_vertices[i][0], base_vertices[(i + 1) % len(base_vertices)][0]],
        [base_vertices[i][1], base_vertices[(i + 1) % len(base_vertices)][1]],
        [base_vertices[i][2], base_vertices[(i + 1) % len(base_vertices)][2]],
        color='blue'
    )

# Plot the beams
for beam in beams:
    ax.plot(
        [beam[0][0], beam[1][0]],
        [beam[0][1], beam[1][1]],
        [beam[0][2], beam[1][2]],
        color='black', linewidth=1.5
    )

# Plot wind turbines as points on top of the beams
ax.scatter(beam1_top[0], beam1_top[1], beam1_top[2], color='red', s=100, label='Wind Turbine 1')
ax.scatter(beam2_top[0], beam2_top[1], beam2_top[2], color='red', s=100, label='Wind Turbine 2')

# Plot floats as circles at the corners
float_radius = 0.2
for vertex in base_vertices:
    u = np.linspace(0, 2 * np.pi, 100)
    x = vertex[0] + float_radius * np.cos(u)
    y = vertex[1] + float_radius * np.sin(u)
    z = np.full_like(u, vertex[2])
    ax.plot(x, y, z, color='green', label='Float')

# Labels and visualization settings
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')
ax.legend()
plt.title('Wind Turbine Structure Visualization')
plt.show()

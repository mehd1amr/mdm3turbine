#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 16:18:09 2025

@author: mehdiamara
"""

from PyNite import FEModel3D
# Create a new finite element model
model = FEModel3D()

# Define nodes
model.AddNode('N1', 0, 0, 0)
model.AddNode('N2', 0, 10, 0)
model.AddNode('N3', 5, 10, 0)

# Define a material (E = modulus of elasticity, G = shear modulus)
model.AddMaterial('Steel', E=210e9, G=81.2e9)

# Define members
model.AddMember('M1', 'N1', 'N2', 'Steel', 0.01, 0.01)
model.AddMember('M2', 'N2', 'N3', 'Steel', 0.01, 0.01)

# Define supports
model.DefineSupport('N1', True, True, True, False, False, False)
model.DefineSupport('N3', True, True, True, False, False, False)

# Add loads (N/m for members, N for nodes)
model.AddNodeLoad('N2', 'FY', -1000)  # 1000 N downward force on N2

# Analyze the model
model.Analyze()

# Print results
for node in model.Nodes.values():
    print(f"Node {node.Name} displacements: {node.DX}, {node.DY}, {node.DZ}")

for member in model.Members.values():
    print(f"Member {member.Name} axial force: {member.Fx}")

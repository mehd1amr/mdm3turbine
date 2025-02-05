#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 19:47:02 2025

@author: mehdiamara
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Material properties for GRP
#C = 1.5e-10  # Paris’ Law coefficient 
C = 1.08e-12 # CFRP

#m = 3.5  # Paris’ Law exponent
m = 3.5 #CFRP

sigma_min = 30  # Minimum applied stress (MPa)
K_ic = 25  # Fracture toughness (MPa sqrt(m)) - Critical Stress Intensity Factor
a_initial = 0.001  # Initial crack size (meters)
a_final = 0.02  # Failure crack size (meters)
N_cycles = 1_000_000  # Maximum simulation cycles

# Stress values for different beam elements, from Charlie's Abaqus simulation 
# (diagonal beam, bottom beam right under the turbines, left-hand-side bottom beam, vertical beam)
stress_data = {
    "Diagonal Element": [192, 255, 253, 259, 288, 365],  # MPa
    "Bottom Side Element": [192, 192, 192, 197, 197, 201, 209, 
                             218, 201, 207, 206, 212],
    "Bottom Front Element": [192, 198.9, 199.4, 203.4, 204.2, 206.5, 209.6, 
                              215.7, 213.8, 213.9, 218, 216.7, 216.7, 303.4],
    "Vertical Element": [192, 226, 257, 318]
}

# Stress Intensity Factor range (ΔK)
def delta_K(sigma_max, sigma_min, a):
    return (sigma_max - sigma_min) * np.sqrt(np.pi * a)

# Paris' Law: da/dN = C * (ΔK)^m
def crack_growth(sigma_max, a_initial, a_final, N_cycles, C, m):
    a = a_initial
    a_values = [a]
    cycle_values = [0]

    # Adjust step size dynamically
    step = max(500, N_cycles // 1000)  # Ensure enough data points for plotting

    for cycle in range(1, N_cycles + 1):
        dK = delta_K(sigma_max, sigma_min, a)
        da_dN = C * (dK ** m)
        a += da_dN  # Update crack length

        if cycle % step == 0 or a >= a_final:
            a_values.append(a)
            cycle_values.append(cycle)

        if a >= a_final:
            print(f"Failure occurs at cycle {cycle} for {sigma_max} MPa stress")
            return cycle_values, a_values, cycle  # Return early failure data

    return cycle_values, a_values, N_cycles  # If no failure occurs in given cycles

# Run simulations for all elements
results = {}
failure_cycles = {}

for element, stress_values in stress_data.items():
    sigma_max = np.mean(stress_values)  # Use average stress for each element
    cycles, crack_sizes, failure_cycle = crack_growth(sigma_max, a_initial, a_final, N_cycles, C, m)
    results[element] = (cycles, crack_sizes)
    failure_cycles[element] = failure_cycle

# Convert results into a DataFrame for clear display
df_results = pd.DataFrame.from_dict(failure_cycles, orient='index', columns=["Failure Cycles"])
print("\n Fatigue Failure Cycles for Each Element \n")
print(df_results)  # Display failure data in console

# Plot crack growth for all elements
plt.figure(figsize=(10, 6))

for element, (cycles, crack_sizes) in results.items():
    if len(cycles) > 1:
        plt.plot(cycles, crack_sizes, label=f"{element} - Failure at {failure_cycles[element]} cycles")

plt.axhline(y=a_final, linestyle="--", color="black", label="Failure Threshold")
plt.xlabel("Cycles")
plt.ylabel("Crack Length (m)")
plt.title("Crack Growth in GRP Material for Different Beam Elements")
plt.legend()
plt.grid()
plt.show()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 20:10:58 2023

@author: shar_sp
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Oct  1 13:27:59 2023

@author: shar_sp
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import time

# Display a catchy and funky message
print("🚀 Welcome to the Velocity Field Visualizer 🌪")
print("Prepare to be amazed by the power of data!")

# Ask the user for the directory containing the .dat files
directory = input("Please enter the directory containing the .dat files: ")

# Ask the user for the file name (e.g., 'data_00700')
file_prefix = input("Please enter the file name (e.g., 'data_00700'): ")
data_dir = os.path.join(directory, file_prefix)

start_time = time.time()

# Initialize an empty list to store data arrays from each file
data_arrays = []

# Number of rows to skip at the beginning of each file
skip_rows = 5

# Iterate through the .dat files starting with "dmp_"
for filename in os.listdir(data_dir):
    if filename.startswith("dmp_") and filename.endswith(".dat"):
        file_path = os.path.join(data_dir, filename)
        with open(file_path, 'r') as file:
            # Read lines, skip the first 5, and filter out non-numeric lines
            lines = file.readlines()[skip_rows:]
            numeric_lines = [line for line in lines if any(char.isdigit() or char == '.' or char == '-' for char in line)]
            data = np.loadtxt(numeric_lines, dtype=float)
            data_arrays.append(data)
        # Print the name of the file
        print(f"Read file: {filename}")

# Assuming that each data array has the same number of rows
num_rows = data_arrays[0].shape[0]
num_columns = len(data_arrays)

# Create an empty 2D velocity field
velocity_field = np.zeros((num_rows, num_columns))

# Populate the velocity field
for i, data in enumerate(data_arrays):
    velocity_field[:, i] = data[:, 4]  # Assuming the velocities are in the 5th column

# Define the desired colorbar range
vmin = 10  # Minimum value
vmax = 100  # Maximum value
plt.figure(figsize=(12, 6))
# Visualize the 2D velocity field with the specified colorbar range
plt.imshow(velocity_field, cmap='jet', aspect='auto', vmin=vmin, vmax=vmax)
cbar = plt.colorbar()
plt.ylim(950, 1050)
cbar.set_label('Velocity')

# Set custom x-axis ticks
custom_x_ticks = [0, 400, 800, 1200, 1600, 1980]
custom_x_tick_labels = ['0', '20', '40', '60', '80', '100']
plt.xticks(custom_x_ticks, custom_x_tick_labels)
plt.xlabel('x/D')
custom_y_ticks = [950, 975, 1000, 1025, 1050]
custom_y_tick_labels = ['-10', '-5', '0', '5', '10']  # ,'0.1','0.2','0.3','0.4','0.5']
plt.yticks(custom_y_ticks, custom_y_tick_labels)
plt.ylabel('y/D')
# Save the figure with a prefix of the file name
figure_filename = f"{file_prefix}_VelField.pdf"
plt.savefig(figure_filename, dpi=1200, bbox_inches='tight')

# Show the plot (optional)
plt.show()

# Display a message with the saved figure filename
print(f"Figure saved as '{figure_filename}'")

print("--- %s seconds ---" % (time.time() - start_time))

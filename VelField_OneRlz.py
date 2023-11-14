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

# Get a list of "dmp_" files sorted by filename
file_list = sorted([filename for filename in os.listdir(data_dir) if filename.startswith("dmp_") and filename.endswith(".dat")])

# Iterate through the sorted list of "dmp_" files
for filename in file_list:
    file_path = os.path.join(data_dir, filename)
    with open(file_path, 'r') as file:
        # Read lines, skip the first 5, and filter out non-numeric lines
        lines = file.readlines()[skip_rows:]
        numeric_lines = [line for line in lines if any(char.isdigit() or char == '.' or char == '-' for char in line)]
        data = np.loadtxt(numeric_lines, dtype=float)
        data_arrays.append(data)
    
    # Print the name of the file and overwrite the existing line
    print(f"\rRead file: {filename}", end='', flush=True)
    time.sleep(0)  # Optional: Add a short delay to visualize the update

# Print a new line after completing the loop
print()

# Assuming that each data array has the same number of rows
num_rows = data_arrays[0].shape[0]
num_columns = len(data_arrays)

# Create an empty 2D velocity field
velocity_field = np.zeros((num_rows, num_columns))

# Populate the velocity field
for i, data in enumerate(data_arrays):
    velocity_field[:, i] = data[:, 4]  # Assuming the velocities are in the 5th column


# Normalize the x-axis and y-axis by dividing by the diameter of the beam (D)
D = 0.062
num_points = 2497

normalized_x_axis = np.linspace(0/D, 6.2/D, num_points)
normalized_y_axis = np.linspace(1/D, -1/D, len(velocity_field))

# Plot the data with the normalized x and y axes
plt.figure(figsize=(12, 6))
plt.imshow(velocity_field, cmap='jet', aspect='auto',
           extent=[0/D, 6.2/D, -1/D, 1/D],
           vmin=velocity_field[:, 1:].min(), vmax=velocity_field[:, 1:].max())
cbar = plt.colorbar()
cbar.set_label('Velocity')
plt.xlabel('x/D')
plt.ylabel('y/D')

# Save the figure with a prefix of the file name
figure_filename = f"{file_prefix}_VelField.pdf"
plt.savefig(figure_filename, dpi=1200, bbox_inches='tight')

# Show the plot (optional)
plt.show()

# Display a message with the saved figure filename
print(f"Figure saved as '{figure_filename}'")

print("--- %s seconds ---" % (time.time() - start_time))

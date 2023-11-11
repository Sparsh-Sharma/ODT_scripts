# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 11:34:06 2023

@author: shar_sp
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 14:57:47 2023

@author: shar_sp
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import time

# Display a catchy and funky message
print("🚀 Welcome to the Ensemble Average Velocity Field Visualizer 🌪")
print("Prepare for the spectacular ensemble average display!")

# Ask the user for the base directory containing multiple simulation directories
base_dir = input("Please enter the base directory containing simulation data: ")

# Ask the user for the number of ensembles based on directories with the 'data_' prefix
num_ensembles = int(input("How many 'data_' directories would you like to use for the ensemble average? "))

# Initialize empty lists to store data arrays and ensemble sum
data_arrays = []
ensemble_sum = None

# Number of rows to skip at the beginning of each file
skip_rows = 5
start_time = time.time()

# Get a list of "data_" directories sorted by name
sim_dirs = sorted([sim_dir for sim_dir in os.listdir(base_dir) if sim_dir.startswith("data_")])

# Iterate through simulation directories
for sim_dir in sim_dirs:
    sim_dir_path = os.path.join(base_dir, sim_dir)
    if os.path.isdir(sim_dir_path):
        sim_data = []  # Store data from the current simulation

        # Get a list of "dmp_" files sorted by filename
        file_list = sorted([filename for filename in os.listdir(sim_dir_path) if filename.startswith("dmp_") and filename.endswith(".dat")])

        # Iterate through the sorted list of "dmp_" files
        print(f"Processing directory {sim_dir}")
        for filename in file_list:
            file_path = os.path.join(sim_dir_path, filename)
            with open(file_path, 'r') as file:
                # Read lines, skip the first 5, and filter out non-numeric lines
                lines = file.readlines()[skip_rows:]
                numeric_lines = [line for line in lines if any(char.isdigit() or char == '.' or char == '-' for char in line)]
                data = np.loadtxt(numeric_lines, dtype=float)
                sim_data.append(data)
                # If ensemble_sum is None, initialize it with the first data array
                if ensemble_sum is None:
                    ensemble_sum = data
                else:
                    ensemble_sum += data

        # Add the data from the current simulation to the list
        data_arrays.append(sim_data)

        # Check if the desired number of ensembles has been reached
        if len(data_arrays) == num_ensembles:
            break

        # Calculate the time elapsed and display a dynamic message
        elapsed_time = time.time() - start_time
        print(f"Processed directory {sim_dir}, Elapsed time: {elapsed_time:.2f} seconds")

# Calculate the ensemble average by dividing the sum by the number of simulations
ensemble_average = ensemble_sum / len(data_arrays)

# Assuming that each data array has the same number of rows
num_rows = data_arrays[0][0].shape[0]
num_columns = len(data_arrays[0])

# Create an empty 2D velocity field for the ensemble average
velocity_field_ensemble = np.zeros((num_rows, num_columns))

# Populate the ensemble average velocity field
for i in range(num_columns):
    for sim_data in data_arrays:
        velocity_field_ensemble[:, i] += sim_data[i][:, 4]  # Assuming the velocities are in the 5th column
    velocity_field_ensemble[:, i] /= len(data_arrays)

# Define the desired colorbar range
vmin = 0  # Minimum value
vmax = 170  # Maximum value

# Visualize the ensemble average 2D velocity field with the specified colorbar range
plt.figure(figsize=(12, 6))
plt.imshow(velocity_field_ensemble, cmap='jet', aspect='auto', vmin=vmin, vmax=vmax)
cbar = plt.colorbar()
plt.ylim(950, 1050)
cbar.set_label('Velocity')
plt.xlabel('File Index (Time)')
plt.ylabel('Vertical Position Index')

# Set custom x-axis ticks
custom_x_ticks = [0, 400, 800, 1200, 1600, 1980]
custom_x_tick_labels = ['0', '20', '40', '60', '80', '100']
plt.xticks(custom_x_ticks, custom_x_tick_labels)
plt.yticks([950, 975, 1000, 1025, 1050], ['-10', '-5', '0', '5', '10'])
plt.ylabel('y/D')

# Ask the user for the figure filename
figure_filename = input("Please enter the filename to save the figure (e.g., 'average_velocity_field.pdf'): ")

plt.savefig(figure_filename, dpi=300, bbox_inches='tight')

# Show the plots (optional)
plt.show()

# Display a message with the saved figure filename
print(f"Figure saved as '{figure_filename}'")

print("--- %s seconds ---" % (time.time() - start_time))

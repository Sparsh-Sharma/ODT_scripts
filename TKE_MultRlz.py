# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 12:53:35 2023

@author: shar_sp
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 09:06:28 2023

@author: shar_sp
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import time

def process_data(base_dir):
    # Initialize an empty list to store the results
    mean_A_values = []

    # Iterate over directories that match the pattern 'data_*'
    for folder_name in sorted(os.listdir(base_dir)):
        if folder_name.startswith("data_") and os.path.isdir(os.path.join(base_dir, folder_name)):
            data_dir = os.path.join(base_dir, folder_name)
            # Rest of your code remains the same with slight modifications
            data_arrays = []
            skip_rows = 5
            message = "\033[1;31mProcessing directory {}\033[0m".format(folder_name)
            print(message)
            start_time = time.time()
            
            # Sort the list of "dmp_" files
            file_list = sorted([filename for filename in os.listdir(data_dir) if filename.startswith("dmp_") and filename.endswith(".dat")])

            for filename in file_list:
                file_path = os.path.join(data_dir, filename)
                with open(file_path, 'r') as file:
                    lines = file.readlines()[skip_rows:]
                    numeric_lines = [line for line in lines if any(char.isdigit() or char == '.' or char == '-' for char in line)]
                    data = np.loadtxt(numeric_lines, dtype=float)
                    data_arrays.append(data)
                    # Print the name of the file and overwrite the existing line
                    print(f"\rRead file: {filename}", end='', flush=True)
                    # time.sleep(0.0001)  # Optional: Add a short delay to visualize the update
            # Print a new line after completing the loop
            print()
            num_rows = data_arrays[0].shape[0]
            num_columns = len(data_arrays)
            velocity_field = np.zeros((num_rows, num_columns))

            # # Assuming velocity_field_ensemble is defined somewhere
            # velocity_field_ensemble = np.zeros((num_rows, num_columns))

            for i, data in enumerate(data_arrays):
                velocity_field[:, i] = data[:, 4]

            difference_field = np.abs(velocity_field_ensemble[:, 1:] - velocity_field[:, 1:])
            elapsed_time = time.time() - start_time
            processed_message = "\033[1;32mProcessed {}, Elapsed time: {:.2f} seconds\033[0m".format(folder_name, elapsed_time)
            print(processed_message)
            # difference_field = np.abs(velocity_field - velocity_field[:, 1:])
            mean_A_values.append(difference_field)

    # Compute the mean of A0, A1, ..., An
    mean_A = np.mean(mean_A_values, axis=0)

    return mean_A

start_time = time.time()
# Yellow text for the first message
welcome_message = "\033[1;33m🚀 Welcome to the Ensemble Average & Mean A Visualizer 🌪\033[0m"
print(welcome_message)

# Cyan text for the second message
explore_message = "\033[1;36mGet ready to explore the power of 'data_' directories!\033[0m"
print(explore_message)


# Base directory containing multiple simulation directories
input_message = "\033[1;31mPlease enter the base directory containing simulation data: \033[0m"
base_dir = input(input_message)
# Initialize empty lists to store data arrays and ensemble sum
data_arrays = []
ensemble_sum = None

# Number of rows to skip at the beginning of each file
skip_rows = 5

# Iterate through simulation directories
for sim_dir in sorted([d for d in os.listdir(base_dir) if d.startswith("data_")]):
    sim_dir_path = os.path.join(base_dir, sim_dir)
    if os.path.isdir(sim_dir_path):
        sim_data = []  # Store data from the current simulation
        print(f"\033[1;35mProcessing directory {sim_dir}\033[0m")
        start_time = time.time()
        # Sort the list of "dmp_" files
        dmp_files = sorted([filename for filename in os.listdir(sim_dir_path) if filename.startswith("dmp_") and filename.endswith(".dat")])

        # Iterate through the sorted list of "dmp_" files
        for filename in dmp_files:
            file_path = os.path.join(sim_dir_path, filename)
            with open(file_path, 'r') as file:
                # Read lines, skip the first 5, and filter out non-numeric lines
                lines = file.readlines()[skip_rows:]
                numeric_lines = [line for line in lines if any(char.isdigit() or char == '.' or char == '-' for char in line)]
                data = np.loadtxt(numeric_lines, dtype=float)
                sim_data.append(data)
                print(f"\rRead file: {filename}", end='', flush=True)
                # time.sleep(0.0001)  # Optional: Add a short delay to visualize the update

                # If ensemble_sum is None, initialize it with the first data array
                if ensemble_sum is None:
                    ensemble_sum = data
                else:
                    ensemble_sum += data
        # Print a new line after completing the loop
        print()
        # Add the data from the current simulation to the list
        data_arrays.append(sim_data)

        # Calculate the time elapsed and display a dynamic message
        elapsed_time = time.time() - start_time
        # Yellow text for the processing message
        print(f"\033[1;33mProcessed directory {sim_dir}, Elapsed time: {elapsed_time:.2f} seconds\033[0m")



# ... (continue with the rest of your code)
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

# Process the data using the function and save it
print("Let's find out the fluctuations")
mean_A = process_data(base_dir)

# Set font properties
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 11

# Normalize the x-axis and y-axis by dividing by the diameter of the beam (D)
D = 0.062
num_points = 2497

normalized_x_axis = np.linspace(0/D, 6.2/D, num_points)
normalized_y_axis = np.linspace(1/D, -1/D, len(velocity_field_ensemble))

# Plot the ensemble average 2D velocity field
plt.figure(figsize=(12, 6))
plt.imshow(velocity_field_ensemble, cmap='jet', aspect='auto',
           extent=[0/D, 6.2/D, -1/D, 1/D],
           vmin=velocity_field_ensemble[:, 1:].min(), vmax=velocity_field_ensemble[:, 1:].max())
cbar = plt.colorbar()
cbar.set_label('Velocity')
plt.xlabel('x/D')
plt.ylabel('y/D')
plt.savefig('average_velocity_field1.pdf', dpi=300, bbox_inches='tight')
plt.show()

# Plot the mean TKE field
plt.figure(figsize=(12, 6))
TKE = (mean_A ** 2) / 2000
plt.imshow(TKE, cmap='jet', aspect='auto',
           extent=[0/D, 6.2/D, -1/D, 1/D],
           vmin=TKE[:, 1:].min(), vmax=TKE[:, 1:].max()/1.8)
cbar = plt.colorbar()
cbar.set_label('TKE')
plt.ylim(-5, 5)
plt.xlim(0, 20)
plt.xlabel('x/D')
plt.ylabel('y/D')
plt.savefig('mean_TKE_field_ZoomIn.pdf', dpi=1200, bbox_inches='tight')
plt.show()

# Plot another view of the mean TKE field
plt.figure(figsize=(12, 6))
plt.imshow(TKE, cmap='jet', aspect='auto',
           extent=[0/D, 6.2/D, -1/D, 1/D],
           vmin=TKE[:, 1:].min(), vmax=TKE[:, 1:].max())
cbar = plt.colorbar()
cbar.set_label('TKE')
plt.xlabel('x/D')
plt.ylabel('y/D')
plt.savefig('mean_TKE_field_ZoomOut.pdf', dpi=1200, bbox_inches='tight')
plt.show()

# Save 'velocity_field_ensemble' and 'mean_A' in .npy format
np.save('velocity_field_ensemble.npy', velocity_field_ensemble)
np.save('mean_A.npy', mean_A)

# Print messages
print("\033[1;32mEnsemble averaged velocity is saved as velocity_field_ensemble.npy\033[0m")
print("\033[1;35mTKE is saved as velocity_field_ensemble.npy\033[0m")

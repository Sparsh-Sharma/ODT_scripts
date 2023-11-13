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
                    time.sleep(0.0001)  # Optional: Add a short delay to visualize the update
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
                time.sleep(0.0001)  # Optional: Add a short delay to visualize the update

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
#%%
# Continue with plotting or saving the mean A field as needed
# Visualize the ensemble average 2D velocity field with the specified colorbar range
# Define the desired colorbar range
# Set the font family and font size
plt.rcParams['font.family'] = 'serif'
# plt.rcParams['font.serif'] = ['Computer Modern Roman']
# plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['font.size'] = 11

# vmin = 0  # Minimum value
# vmax = 100  # Maximum value

plt.figure(figsize=(12, 6))
plt.imshow(velocity_field_ensemble, cmap='jet', aspect='auto', vmin=velocity_field_ensemble[:,1:].min(), vmax=velocity_field_ensemble[:,1:].max())
cbar = plt.colorbar()
plt.ylim(950, 1050)
cbar.set_label('Velocity')
plt.xlabel('File Index (Time)')
plt.ylabel('Vertical Position Index')

# Set custom x-axis ticks
custom_x_ticks = [0, 400, 800, 1200, 1600, 1980]
custom_x_tick_labels = ['0', '20', '40', '60', '80', '100']
plt.xticks(custom_x_ticks, custom_x_tick_labels)
plt.xlabel('x/D')

custom_y_ticks = [950, 975, 1000, 1025, 1050]
custom_y_tick_labels = ['-10', '-5', '0', '5', '10']
plt.yticks(custom_y_ticks, custom_y_tick_labels)
plt.ylabel('y/D')

# Save the ensemble average figure as a high-resolution PDF
plt.savefig('average_velocity_field1.pdf', dpi=300, bbox_inches='tight')

plt.show()

#%%
# Plot or save the mean A field as needed
plt.figure(figsize=(12, 6))
plt.ylim(800, 1200)
plt.xlim(0, 500)
plt.imshow((mean_A ** 2) / 2000, cmap='jet', aspect='auto')
cbar = plt.colorbar()
cbar.set_label('TKE')
custom_x_ticks = [0,40,80,120,160,200]
custom_x_tick_labels = ['0','2','4','6','8','10']
plt.xticks(custom_x_ticks, custom_x_tick_labels)
plt.xlabel('x/D')
custom_y_ticks = [980,990,1000,1010,1020]
custom_y_tick_labels = ['-4','-2','0','2','4']#,'0.1','0.2','0.3','0.4','0.5']
plt.yticks(custom_y_ticks, custom_y_tick_labels)
plt.ylabel('y/D')
plt.savefig('mean_TKE_field_ZoomIn.pdf', dpi=1200, bbox_inches='tight')
plt.show()

plt.figure(figsize=(12, 6))
plt.ylim(950,1050)
plt.imshow((mean_A ** 2) / 2000, cmap='jet', aspect='auto')
cbar = plt.colorbar()
cbar.set_label('TKE')
custom_x_ticks = [0,400,800,1200,1600, 1980]
custom_x_tick_labels = ['0','20','40','60','80','100']
plt.xticks(custom_x_ticks, custom_x_tick_labels)
plt.xlabel('x/D')
custom_y_ticks = [950,975,1000,1025,1050]
custom_y_tick_labels = ['-10','-5','0','5','10']#,'0.1','0.2','0.3','0.4','0.5']
plt.yticks(custom_y_ticks, custom_y_tick_labels)
plt.ylabel('y/D')
plt.savefig('mean_TKE_field_ZoomOut.pdf', dpi=1200, bbox_inches='tight')
plt.show()

#%%
# Save 'velocity_field_ensemble' and 'mean_A' in .npy format
np.save('velocity_field_ensemble.npy', velocity_field_ensemble)
np.save('mean_A.npy', mean_A)
message = "\033[1;32mEnsemble averaged velocity is saved as velocity_field_ensemble.npy\033[0m"
print(message)
message = "\033[1;35mTKE is saved as velocity_field_ensemble.npy\033[0m"
print(message)
print("--- %s seconds ---" % (time.time() - start_time))

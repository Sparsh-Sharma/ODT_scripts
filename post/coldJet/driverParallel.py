# driverParallel.py

from __future__ import division
import os
import sys
import multiprocessing
from parallel_tasks import perform_basic_tasks, process_velocity_profiles, perform_remaining_tasks

def wrapper_perform_basic_tasks(DI):
    perform_basic_tasks(DI)

def wrapper_process_velocity_profiles(DI):
    process_velocity_profiles(DI)

def wrapper_perform_remaining_tasks(DI):
    perform_remaining_tasks(DI)

# Main execution
if __name__ == '__main__':
    try:
        caseN = sys.argv[1]
    except IndexError:
        raise ValueError("Include the case name in the call to driver.py")

    DI = {'pdir': '../../data/' + caseN + '/post/', \
          'ddir': '../../data/' + caseN + '/data/', \
          'cdir': '../../data/' + caseN + '/', \
          'cn': caseN}

    if not os.path.exists(DI['pdir']):
        os.mkdir(DI['pdir'])

    # Number of processes
    num_processes = 3

    # Split the tasks for parallel execution
    tasks = [wrapper_perform_basic_tasks, wrapper_process_velocity_profiles, wrapper_perform_remaining_tasks]

    # Execute tasks in parallel
    with multiprocessing.Pool(processes=num_processes) as pool:
        pool.map(lambda task: task(DI), tasks)

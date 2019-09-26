#   Author: Jagadishwar R. Sirigiri
#   Bridge12 Technologies Inc.
#   37 Loring Drive, Framingham, MA 01702
#   Date Created: September 25, 2019
#   Top level file to automate Corrug runs

#   Revision history:

import sys
sys.path.insert(0, '..\\designs')
import os, shutil
import json
from datetime import datetime

import CorrugSimInput, CorrugUtils


def main():

    nodes, results_path, var_list, var_range = CorrugSimInput.simulation_parameters()

    var_register = var_range.copy()
    # remove all variations in the list and retain nominal values
    for item in var_register:
        var_register[item] = [(var_register[item][0])]  # important to keep () in the expression

    project_directory=os.getcwd()

    #  start setting up directories for evenutal runs
    tnow = datetime.now()
    this_run_time_stamp = tnow.strftime("%Y-%m-%d-%H-%M-%S")
    run_directory = results_path + '/' + var_register['version_num'][0] + '-' + this_run_time_stamp
    local_run_directory = this_run_time_stamp
    # prepare the run directories on the local machine so that it is easy to sort and remove duplicates
    # After sorting is done locally then copy the files to the 'remote' run directory and delete the lccal copies
    # manipulating directories during the sort on a remote fileserver is slow and hence the above trick

    #os.mkdir(run_directory)
    print('Results for this run are stored in: ',run_directory)

    os.mkdir(local_run_directory)

    step = 0

    for var in var_list:
        if len(var) == 1: #1D scans
            scan_range = var_range[var[0]]
            for count in range(0,len(scan_range)):   # start from 1 to avoid the nominal value of the parameter
                var_register[var[0]] = [scan_range[count]]
                step +=1
                step_directory = local_run_directory + '/' + str(step)
                os.mkdir(step_directory)
                CorrugSimInput.create_corrug_input_file(var_register, step_directory)
                with open (step_directory + '/' + 'parameter.dict', 'w') as keyfile:
                    keyfile.write(json.dumps(var_register))
            var_register = var_range.copy() # restore the value of var_register after iteration
            # remove all variations in the list and retain nominal values
            for item in var_register:
                var_register[item] = [var_register[item][0]]

        elif len(var) == 2:  #2D scans

            scan_range_outer = var_range[var[0]]
            for count_outer in range(0,len(scan_range_outer)):   # start from 1 to avoid the nominal value of the parameter
                var_register[var[0]] = [scan_range_outer[count_outer]]
                scan_range_inner = var_range[var[1]]
                for count_inner in range(0,len(scan_range_inner)):  # start from 1 to avoid the nominal value of the parameter
                    var_register[var[1]] = [scan_range_inner[count_inner]]
                    step += 1
                    step_directory = local_run_directory + '/' + str(step)
                    os.mkdir(step_directory)
                    CorrugSimInput.create_corrug_input_file(var_register, step_directory)
                    with open(step_directory + '/' + 'parameter.dict', 'w') as keyfile:
                        keyfile.write(json.dumps(var_register))
                var_register = var_range.copy()  # restore the value of var_register after iteration
                # remove all variations in the list and retain nominal values
                for item in var_register:
                    var_register[item] = [var_register[item][0]]

        elif len(var) == 3:  #3D scans

            scan_range_loop3 = var_range[var[0]]
            for count_loop3 in range(0,len(scan_range_loop3)):   # start from 1 to avoid the nominal value of the parameter
                var_register[var[0]] = [scan_range_loop3[count_loop3]]
                scan_range_loop2 = var_range[var[1]]
                for count_loop2 in range(0,len(scan_range_loop2)):  # start from 1 to avoid the nominal value of the parameter
                    var_register[var[1]] = [scan_range_loop2[count_loop2]]
                    scan_range_loop1 = var_range[var[2]]
                    for count_loop1 in range(0, len(scan_range_loop1)):  # start from 1 to avoid the nominal value of the parameter
                        var_register[var[2]] = [scan_range_loop1[count_loop1]]
                        # print(var_register[var[0]], var_register[var[1]], var_register[var[2]],
                        #       var_register['current'], var_register['beam_radius'])
                        step += 1
                        step_directory = local_run_directory + '/' + str(step)
                        os.mkdir(step_directory)
                        CorrugSimInput.create_corrug_input_file(var_register, step_directory)
                        with open(step_directory + '/' + 'parameter.dict', 'w') as keyfile:
                            keyfile.write(json.dumps(var_register))
            var_register = var_range.copy()  # restore the value of var_register after iteration
            # remove all variations in the list and retain nominal values
            for item in var_register:
                var_register[item] = [var_register[item][0]]

    # remove all the duplicate directories
    CorrugUtils.remove_duplicate_parameter_simulation_directories(local_run_directory)

    # copy the unique simulation folders to the remote file server
    shutil.copytree(local_run_directory, run_directory)
    # now clean up local folder
    shutil.rmtree(local_run_directory)

    for files in os.listdir(project_directory):
        if files.endswith(".plt"):
            shutil.copy(files,run_directory)
        if files.endswith(".dat"):
            shutil.copy(files, run_directory)
    shutil.copy(project_directory + '\\CorrugSimInput.py',run_directory)
    # write the scan parameters in a file for visualization
    write_scan_parameters_to_list_file(run_directory, var_range, var_list)
    # write nominal parameter values to run directory to help in postprocessing
    with open(run_directory + '\\' + 'NominalParameters.dict', 'w') as file:
        file.write(json.dumps(var_register))
    with open(run_directory + '\\' + 'ScanVariables.list', 'w') as file:
        json.dump(var_list,file)

    sim_folders = os.listdir(run_directory)
    jobs_dir = [run_directory + '/' + folder for folder in sim_folders]

    #  start execution of parameter sweeps
    print('-------------------------------------------------------------')
    print ('Executing all variations....')
    print('-------------------------------------------------------------')
    print('')
    CorrugUtils.execute_parameter_sweeps(jobs_dir, var_register, nodes, run_directory)


def write_scan_parameters_to_list_file(run_directory,var_range,var_list):
    # write the scan parameters in a file for visualization
    with open(run_directory + '\\' + 'ScanParameters.dat','w') as file:
        for var in var_list:
            if len(var) == 1:
                file.write(var[0]+','+ ("".join(str(var_range[var[0]]))))
                file.write('\n \n')

            if len(var) == 2:
                file.write(var[0] + ',' + ("".join(str(var_range[var[0]]))))
                file.write('\n')
                file.write(var[1] + ',' + ("".join(str(var_range[var[1]]))))
                file.write('\n \n')

            if len(var) == 3:
                file.write(var[0] + ',' + ("".join(str(var_range[var[0]]))))
                file.write('\n')
                file.write(var[1] + ',' + ("".join(str(var_range[var[1]]))))
                file.write('\n')
                file.write(var[2] + ',' + ("".join(str(var_range[var[2]]))))
                file.write('\n \n')
    return

if __name__ == '__main__':
    main()

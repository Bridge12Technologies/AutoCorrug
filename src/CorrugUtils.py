#   Author: Jagadishwar R. Sirigiri
#   Bridge12 Technologies Inc.
#   37 Loring Drive, Framingham, MA
#   Date Created: 2 September 2017
#   Last Modified: 2 September 2017
#   Executes the program

#   Ver 1.0 20170902 - 

import os,string,shutil,csv

#   Author: Jagadishwar R. Sirigiri
#   Bridge12 Technologies, Inc.
#   37 Loring Drive, Framingham, MA 01702
#   Date Created: September 25, 2019
#   Utilities for automating CORRUG runs

from numpy import savetxt

def write_corrug_input_file(geometry,var_register,step_directory):

    NumSegments = 0
    for section in geometry:
        section.points()
        NumSegments = NumSegments + section.numsegments

    with open(step_directory+'\\'+'input.i', 'w') as inputfile:
        inputfile.write(str(var_register['Frequency'][0]) + ' ' + str(1)+ ' '+ str(NumSegments))
        inputfile.write('\n')

        for section in geometry:
            savetxt(inputfile,section.z)
        
        for section in geometry:
            savetxt(inputfile,(section.rn), fmt="%s")

        # specify input mode mixture
        if (var_register['Input Modes'][0] == 'TE11'):
            inputfile.write(str(1))
            inputfile.write('\n')
            inputfile.write(str(1) + '  ' + str(0))
            inputfile.write('\n')
        elif (var_register['Input Modes'][0] == 'HE11'):
            inputfile.write(str(4))
            inputfile.write('\n')
            inputfile.write(str(0.91978) + '  ' + str(0)) #TE11
            inputfile.write('\n')
            inputfile.write(str(0.38079) + '  ' + str(180)) #TM11
            inputfile.write('\n')
            inputfile.write(str(0.031623) + '  ' + str(0)) #TE12
            inputfile.write('\n')
            inputfile.write(str(0.07746) + '  ' + str(180)) #TM12
            inputfile.write('\n')

    # write a list file with runtime input for corrug.exe
    with open(step_directory+'\\'+'commands.in', 'w') as inputfile:
        inputfile.write('input.i')
        inputfile.write('\n')  
        inputfile.write('output.o')
        inputfile.write('\n')  
        inputfile.write('pattern.pat')
        inputfile.write('\n')  
        inputfile.write(str(var_register['NTheta'][0]))
        inputfile.write('\n')  
        inputfile.write(str(var_register['DTheta'][0]))
        inputfile.write('\n')  
        inputfile.write('Y')
        inputfile.close()
    return


def write_output_geometry(geometry,step_directory):
    with open(step_directory+'\\'+'geometry.out', 'w') as geometryfile:
        zold = 0
        seccount = 1
        for section in geometry:    
            if seccount == 1:
                j = 0
                for k in section.z:
                    geometryfile.write(str(zold)+','+str(section.r[j])+'\n')
                    zold = k + zold
                    j = j + 1
                seccount = seccount + 1
                geometryfile.write(str(zold)+','+str(section.r[j-1])+'\n')
            else:
                j = 0
                for k in section.z:
                    geometryfile.write(str(zold)+','+str(section.r[j])+'\n')
                    geometryfile.write(str(k+zold)+','+str(section.r[j])+'\n')
                    zold = k + zold
                    j = j + 1
                seccount = seccount + 1
    return


def run_corrug(run_directory, var_register, results_path):
    import socket,os,shutil
    from distutils.dir_util import copy_tree

    host = socket.gethostname()

    # make a local run directory to run simulations and then copy over the results to results folder
    # pick up the last part of the run directory to get the 'step_directory)
    print('test')
    local_run_directory = run_directory.rsplit('/')[-1]
    local_run_directory = os.getcwd()+ '\\' + local_run_directory
    os.mkdir(local_run_directory)
    copy_tree(run_directory, local_run_directory)
    os.chdir(local_run_directory)
    os.system('%CORRUG% < commands.in')

    # copy completed results to the central run directory
    copy_tree(local_run_directory + '\\..\\', run_directory + '\\..\\')
    # delete the local run directories to reclaim disk space
    os.chdir('\\..')
    shutil.rmtree(local_run_directory, ignore_errors=True)

    return (host)

def execute_parameter_sweeps(jobs_dir, var_register, nodes, run_directory):
    # runs MAGY for each of the parameter variation.
    import socket, time
    import dispy
    import contextlib

    hostname = socket.gethostbyname(socket.gethostname())
    cluster = dispy.JobCluster(run_corrug, nodes=nodes, cleanup=True, pulse_interval=30,reentrant=True)

    # import dispy's httpd module, create http server for this cluster
    import dispy.httpd
    http_server = dispy.httpd.DispyHTTPServer(cluster, host=hostname, show_job_args=False)

    # cluster can now be monitored / managed in web browser at
    # http://<host>:8181 where <host> is name or IP address of
    # computer running this program

    ClusterLogFilename = run_directory + '/' + 'RunStats.log'
    with open(ClusterLogFilename, 'w') as logfile:
        logfile.write('Log file for run ' + run_directory + '\n')

        jobs = []
        for step_count in range(1,len(jobs_dir)+1):
            step_directory=jobs_dir[step_count-1]
            job = cluster.submit(step_directory, var_register, run_directory)
            job.id = step_count
            jobs.append(job)

        for job in jobs:
            host = job()

            print (job.ip_addr,' started job ', job.id, ' at ', time.strftime("%a, %d %b %Y %H:%M:%S ",
                    time.localtime(job.start_time)), ' and took',
                    format((float(job.end_time)-float(job.start_time)),"5.0f"), 's')

            print(job.ip_addr, ' started job ', job.id, ' at ', time.strftime("%a, %d %b %Y %H:%M:%S ",
                    time.localtime(job.start_time)), ' and took',
                     format((float(job.end_time) - float(job.start_time)), "5.0f"), 's', file=logfile)

        cluster.print_status()
        with contextlib.redirect_stdout(logfile):
            cluster.print_status()

    cluster.wait()
    http_server.shutdown() # this waits until browser gets all updates
    cluster.close()

    return

def remove_duplicate_parameter_simulation_directories(run_directory):
 # compares the parameter.dict to see if the parameters in the simulation directory are duplicate to a
 # previous simulation setup

    import os, shutil, json

    os.mkdir(run_directory + '/temp')
    numfolders = 0
    for _, dirnames, filenames in os.walk(run_directory):
        # "_," this idiom means "we won't be using this value"
        numfolders += len(dirnames)

    while len([item for item in os.listdir(run_directory)
                        if os.path.isdir(os.path.join(run_directory, item))]) > 2:
        # at the last leg of compare we will have the last folder and the temp folder (which has all the
        # previously compared, unique folders
        dirnames = [item for item in os.listdir(run_directory) if os.path.isdir(os.path.join(run_directory, item))]
        dirnames.remove('temp')

        primary_directory = run_directory + '/' + dirnames.pop(0)
        primnary_list = json.load(open(primary_directory + '\\parameter.dict'))

        for j in dirnames:
            secondary_directory = run_directory + '/' + j
            secondary_list = json.load(open(secondary_directory + '\\parameter.dict'))
            if dict_compare(primnary_list, secondary_list) == 1:
                # delete the duplicate folders
                shutil.rmtree(secondary_directory, ignore_errors=True)
        # move the folder that has been compared to a different temp folder
        shutil.move(primary_directory,run_directory + '/temp' )

    if len([item for item in os.listdir(run_directory)
            if os.path.isdir(os.path.join(run_directory, item))]) == 2:
        dirnames = [item for item in os.listdir(run_directory) if os.path.isdir(os.path.join(run_directory, item))]
        shutil.move(run_directory + '/' + dirnames.pop(0), run_directory + '/temp')

    folders = os.listdir(run_directory + '/temp')
    # now move back the unique sim folders to the run_directory
    for item in folders:
        shutil.move(run_directory + '/temp/' + item, run_directory)
    # time to delete the temp folder
    shutil.rmtree(run_directory + '/temp', ignore_errors=True)

    return

def flatten(l):
    import collections
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el

def dict_compare(dict1,dict2):
    for key in dict1.keys():
        if dict1[key] != dict2[key]:
            return (0)
    return(1)

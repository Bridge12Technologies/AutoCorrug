#   Author: Jagadishwar R. Sirigiri
#   Bridge12 Technologies, Inc.
#   37 Loring Drive, Framingham, MA 01702
#   Date Created: September 25, 2019
#   Postr Processing Utilities for CORRUG

import sys, os
sys.path.insert(0, '..\\src')
import numpy as np
import scipy

from CorrugUtils import dict_compare

def read_output_file(infilename):
    import os,string,shutil,math

    run_fail = False
    TE11_amp = np.nan
    TE11_phase = np.nan
    HE11_amp = np.nan
    HE11_phase = np.nan
    HE12_amp = np.nan
    HE12_phase = np.nan
    Return_Loss = np.nan

    if os.path.exists(infilename):
        with open(infilename, 'r') as fin:
            linelist = fin.readlines()
            if (len(linelist)) == 0:
                run_fail = True
                run_fail = True
                TE11_amp = np.nan
                TE11_phase = np.nan
                HE11_amp = np.nan
                HE11_phase = np.nan
                HE12_amp = np.nan
                HE12_phase = np.nan
                Return_Loss = np.nan
                return (run_fail,TE11_amp,TE11_phase,HE11_amp,HE11_phase,HE12_amp,HE12_phase,Return_Loss)
    else:
        run_fail = True
        TE11_amp = np.nan
        TE11_phase = np.nan
        HE11_amp = np.nan
        HE11_phase = np.nan
        HE12_amp = np.nan
        HE12_phase = np.nan
        Return_Loss = np.nan            
        return (run_fail,TE11_amp,TE11_phase,HE11_amp,HE11_phase,HE12_amp,HE12_phase,Return_Loss)
        
    with open(infilename, 'r') as fin:
        for count in range(0,len(linelist)):
            nextline = fin.readline()
            if 'Aperture Modal Coefficients' in nextline:
                nextline = fin.readline()
                nextline = fin.readline()
                TE11_amp_line = fin.readline()
                TE11 = TE11_amp_line.split()
                TE11_amp = float(TE11[6])
                TE11_phase = float(TE11[7])
            if 'Ind.#   Bg (/m)  Cyclic Dist.(mm) Amplitude  Phase(deg)' in nextline:
                nextline = fin.readline()
                HE11_amp_line = nextline.split()
                HE11_amp = float(HE11_amp_line[3])
                HE11_phase = float(HE11_amp_line[4])
                nextline = fin.readline()
                HE12_amp_line = nextline.split()
                HE12_amp = float(HE12_amp_line[4])
                HE12_phase = float(HE12_amp_line[5])
            if 'Reflection at Input with HE Mode Termination' in nextline:
                temp = nextline.split()
                Return_Loss = float(temp[7])
    
    return (run_fail,TE11_amp,TE11_phase,HE11_amp,HE11_phase,HE12_amp,HE12_phase,Return_Loss)

def tabulate_parameter_variations (run_directory):
    import os, json
    import numpy as np
    import PlotUtils

    os.chdir(run_directory)
    listdic = []
    sim_directories = next(os.walk('.'))[1]  # to just get directories and not files
    print('Starting tabulation of parameter variations')
    count = 1
    for sim_directory in sim_directories:
        print('Parsing simulation directory #', sim_directory, ': Progress ', count, 'of', len(sim_directories))
        count = count + 1
        if os.path.exists(run_directory + '/' +  sim_directory + '/' + 'parameter.dict'):
            try:
                var_list = json.load(open(run_directory + '/' +  sim_directory + '/' + 'parameter.dict'))
                listdic.append(var_list.copy())
            except:
                print('problem loading parameter dictionary in simulation directory : ', sim_directory, '  --- ignoring')
                listdic.append(var_list.copy())
        else:
            print('parameter dictionary not found in simulation directory : ', sim_directory, '  --- ignoring')
            listdic.append(var_list.copy())

    with open ('parameters.sort', 'w') as outfile:
        json.dump(listdic, outfile)

    print('Completed tabulation of parameter variations')
    
    return listdic

def postprocess_2parameters_1variable(run_directory,listdic,var_range,var_list,plot_variable1,plot_variable1_units, 
                                        parameter1,parameter1_units,parameter1_range,parameter2,parameter2_units,parameter2_range, 
                               plotxrange='[]',plotyrange='[]',labels='False'):
    import os, json
    import numpy as np
    import PlotUtils

    os.chdir(run_directory)
    
    legend1 = [None]*(len(parameter2_range))

    datafile_prefix = parameter2 + '-' + parameter1
    datafile1 = datafile_prefix + plot_variable1 + '.dat'
    datafile1.replace(" ", "-")

    data_array0 = np.zeros((len(parameter1_range),1+len(parameter2_range)+len(parameter2_range)))
    
    # add additional column as the first column in parameter1
    # add additional len(range2) to include the folder # corresponding to the simulation results
    for i in range(0, len(parameter1_range)):
        data_array0[i, 0] = parameter1_range[i]

    for j in range(0,len(parameter2_range)):
        legend1[j] = (parameter2 + ' ' + ' = ' + str(parameter2_range[j]))
        
    sim_directories = next(os.walk('.'))[1]  # to just get directories and not files
    var_nominal_list = json.load(open(run_directory + '\\NominalParameters.dict'))
          
    for i in range (0,len(parameter1_range)):
        for j in range (0,len(parameter2_range)):
            match_found = 0
            print('Searching for ', parameter1, ' = ', parameter1_range[i], 'and ', parameter2, ' = ', parameter2_range[j])
            var_nominal_list_copy = var_nominal_list.copy()
            if parameter2 == 'Modes': parameter2_range[j] = list(parameter2_range[j])
            var_nominal_list_copy[parameter1][0] = parameter1_range[i]
            var_nominal_list_copy[parameter2][0] = parameter2_range[j]
            count = 0
            for sim_directory in sim_directories:
                if dict_compare(var_nominal_list_copy, listdic[count]) == 1:
                    print('Match found in simulation directory #', sim_directory)
                    match_found = 1
                    #filename = listdic[count]['version_num'][0] + '.pwbal.out'
                    filename = run_directory + '\\' + sim_directory + '\\' + 'output.o'
                    #datafiles[k] = datafile_prefix + '-' + str(k) + '-power.dat'
                    run_fail,TE11_amp,TE11_phase,HE11_amp,HE11_phase,HE12_amp,HE12_phase,Return_Loss = read_output_file(filename)

                    if plot_variable1 == 'TE11 Power':
                        data_array0[i, j + 1] = TE11_amp**2
                        data_array0[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                    elif plot_variable1 == 'TE11 Phase':
                        data_array0[i, j + 1] = TE11_phase
                        data_array0[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                    elif plot_variable1 == 'HE11 Power':
                        data_array0[i, j + 1] = HE11_amp**2
                        data_array0[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                    elif plot_variable1 == 'HE11 Phase':
                        data_array0[i, j + 1] = HE11_phase
                        data_array0[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                    elif plot_variable1 == 'HE12 POwer':
                        data_array0[i, j + 1] = HE12_amp**2
                        data_array0[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                    elif plot_variable1 == 'HE12 Phase':                        
                        data_array0[i, j + 1] = HE12_phase
                        data_array0[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                    elif plot_variable1 == 'Return_Loss':
                        data_array0[i, j + 1] = Return_Loss
                        data_array0[i, j + 1 + len(parameter2_range)] = int(sim_directory)

                count = count+1
            if match_found == 0:
                    print('Match failed')  
                    data_array0[i, j + 1] = 0.0
                    data_array0[i, j + 1 + len(parameter2_range)] = int(sim_directory)
     

    np.savetxt(datafile1,data_array0,delimiter=',', fmt=' '.join(['%1.4f,']*(len(parameter2_range)+1)
                                                               + ['%i,']*len(parameter2_range)))

    PlotUtils.create_gnuplot_file_2parameters_1variable(run_directory,datafile1,plot_variable1,plot_variable1_units,
                                        parameter1,parameter1_units,parameter1_range,legend1,parameter2,parameter2_units,parameter2_range,
                                      plotxrange=plotxrange,plotyrange=plotyrange,labels=labels)

    return

def postprocess_2parameters_2variables(run_directory,listdic,var_range,var_list,plot_variable1,plot_variable1_units,plot_variable2,
                               plot_variable2_units,parameter1,parameter1_units,parameter1_range,parameter2,
                               parameter2_units,parameter2_range, 
                               plotxrange='[]',plotyrange='[]',ploty2range='[]',labels='False',parameter1_parameter2_map_labels='False'):
    import os, json
    import numpy as np
    import PlotUtils

    os.chdir(run_directory)
    
    
    legend1 = [None]*(len(parameter2_range))
    legend2 = [None]*(len(parameter2_range))

    datafile_prefix = parameter2 + '-' + parameter1
    datafile1 = datafile_prefix + plot_variable1 + '.dat'
    datafile1.replace(" ", "-")
    datafile2 = datafile_prefix + plot_variable2 + '.dat'
    datafile2.replace(" ", "-")


    data_array0 = np.zeros((len(parameter1_range),1+len(parameter2_range)+len(parameter2_range)))
    data_array1 = np.zeros((len(parameter1_range),1+len(parameter2_range)+len(parameter2_range)))
    
    # add additional column as the first column in parameter1
    # add additional len(range2) to include the folder # corresponding to the simulation results
    for i in range(0, len(parameter1_range)):
        data_array0[i, 0] = parameter1_range[i]
        data_array1[i, 0] = parameter1_range[i]

    for j in range(0,len(parameter2_range)):
        legend1[j] = (plot_variable1 + ' for '+parameter2 + ' ' + ' = ' + str(parameter2_range[j]))
        legend2[j] = (plot_variable2 + ' for '+parameter2 + ' ' + ' = ' + str(parameter2_range[j]))
        
    sim_directories = next(os.walk('.'))[1]  # to just get directories and not files
    var_nominal_list = json.load(open(run_directory + '\\NominalParameters.dict'))
          
    for i in range (0,len(parameter1_range)):
           for j in range (0,len(parameter2_range)):
            match_found = 0
            print('Searching for ', parameter1, ' = ', parameter1_range[i], 'and ', parameter2, ' = ', parameter2_range[j])
            var_nominal_list_copy = var_nominal_list.copy()
            if parameter2 == 'Modes': parameter2_range[j] = list(parameter2_range[j])
            var_nominal_list_copy[parameter1][0] = parameter1_range[i]
            var_nominal_list_copy[parameter2][0] = parameter2_range[j]
            count = 0
            for sim_directory in sim_directories:
                if dict_compare(var_nominal_list_copy, listdic[count]) == 1:
                    print('Match found in simulation directory #', sim_directory)
                    match_found = 1
                    #filename = listdic[count]['version_num'][0] + '.pwbal.out'
                    filename = run_directory + '\\' + sim_directory + '\\' + 'output.o'
                    #datafiles[k] = datafile_prefix + '-' + str(k) + '-power.dat'
                    run_fail,TE11_amp,TE11_phase,HE11_amp,HE11_phase,HE12_amp,HE12_phase,Return_Loss = read_output_file(filename)

                    if plot_variable1 == 'TE11 Power':
                        data_array0[i, j + 1] = TE11_amp**2
                        data_array0[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                    elif plot_variable1 == 'TE11 Phase':
                        data_array0[i, j + 1] = TE11_phase
                        data_array0[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                    elif plot_variable1 == 'HE11 Power':
                        data_array0[i, j + 1] = HE11_amp**2
                        data_array0[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                    elif plot_variable1 == 'HE11 Phase':
                        data_array0[i, j + 1] = HE11_phase
                        data_array0[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                    elif plot_variable1 == 'HE12 POwer':
                        data_array0[i, j + 1] = HE12_amp**2
                        data_array0[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                    elif plot_variable1 == 'HE12 Phase':                        
                        data_array0[i, j + 1] = HE12_phase
                        data_array0[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                    elif plot_variable1 == 'Return_Loss':
                        data_array0[i, j + 1] = Return_Loss
                        data_array0[i, j + 1 + len(parameter2_range)] = int(sim_directory)

                    if plot_variable2 == 'TE11 Power':
                        data_array1[i, j + 1] = TE11_amp**2
                        data_array1[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                    elif plot_variable2 == 'TE11 Phase':
                        data_array1[i, j + 1] = TE11_phase
                        data_array1[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                    elif plot_variable2 == 'HE11 Power':
                        data_array1[i, j + 1] = HE11_amp**2
                        data_array1[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                    elif plot_variable2 == 'HE11 Phase':
                        data_array1[i, j + 1] = HE11_phase
                        data_array1[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                    elif plot_variable2 == 'HE12 Power':
                        data_array1[i, j + 1] = HE12_amp**2
                        data_array1[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                    elif plot_variable2 == 'HE12 Phase':                        
                        data_array1[i, j + 1] = HE12_phase
                        data_array1[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                    elif plot_variable2 == 'Return_Loss':
                        data_array1[i, j + 1] = Return_Loss
                        data_array1[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                count = count+1
            if match_found == 0:
                    print('Match failed')  
                    data_array0[i, j + 1] = 0.0
                    data_array0[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                    data_array1[i, j + 1] = 0.0
                    data_array1[i, j + 1 + len(parameter2_range)] = int(sim_directory)        

    np.savetxt(datafile1,data_array0,delimiter=',', fmt=' '.join(['%1.4f,']*(len(parameter2_range)+1)
                                                               + ['%i,']*len(parameter2_range)))
    np.savetxt(datafile2,data_array1,delimiter=',', fmt=' '.join(['%1.4f,']*(len(parameter2_range)+1)
                                                               + ['%i,']*len(parameter2_range)))

    PlotUtils.create_gnuplot_file_2parameters_2variables(run_directory,datafile1,plot_variable1,plot_variable1_units,datafile2,
                                      plot_variable2,plot_variable2_units,parameter1,parameter1_units,
                                      parameter1_range,legend1,parameter2,parameter2_units,parameter2_range,legend2,
                                      plotxrange=plotxrange,plotyrange=plotyrange,ploty2range=ploty2range,labels=labels)

    return


def postprocess_3parameters_1variable(run_directory,listdic,var_range,var_list,plot_variable1,plot_variable1_units,
                                    parameter1,parameter1_units,parameter1_range,
                                    parameter2,parameter2_units,parameter2_range,
                                    parameter3,parameter3_units,parameter3_range,
                                    plotxrange ='[]', plotyrange = '[]', labels = 'False',subplot_columns = 3):
    import os, json
    import numpy as np
    import PlotUtils

    os.chdir(run_directory)

    legend = [None]*(len(parameter2_range))
    for j in range(0, len(parameter2_range)):
        legend[j] = (parameter2 + ' = ' + str(parameter2_range[j]))

    subplot_title = [None]*(len(parameter1_range))
    for k in range(0, len(parameter1_range)):
        subplot_title[k] = (parameter1 + ' = ' + str(parameter1_range[k]))

    datafiles = [None]*(len(parameter3_range))

    datafile_prefix = parameter3 + '-' + parameter2 + '-' + parameter1 +  '-' + plot_variable1 
    datafile_prefix.replace(" ", "-")

    var_nominal_list = json.load(open(run_directory + '\\NominalParameters.dict'))
    for k in range(0,len(parameter3_range)):

        data_array = np.zeros((len(parameter1_range), len(parameter2_range)+ 1 + len(parameter2_range)))
        # add additional column as the first column in parameter1
        # add additional len(range2) to include the folder # corresponding to the simulation results
        for i in range(0, len(parameter1_range)):
            data_array[i, 0] = parameter1_range[i]

        sim_directories = next(os.walk('.'))[1]  # to just get directories and not files


        for i in range (0,len(parameter1_range)):
            for j in range (0,len(parameter2_range)):
                match_found = 0
                print('Searching for ', parameter1, ' = ', parameter1_range[i], ', ', parameter2, ' = ', parameter2_range[j], 'and ', parameter3, ' = ', parameter3_range[k])
                var_nominal_list_copy = var_nominal_list.copy()
                if parameter2 == 'Modes': parameter2_range[j] = list(parameter2_range[j])
                var_nominal_list_copy[parameter1][0] = parameter1_range[i]
                var_nominal_list_copy[parameter2][0] = parameter2_range[j]
                var_nominal_list_copy[parameter3][0] = parameter3_range[k]
                count = 0
                for sim_directory in sim_directories:
                    if dict_compare(var_nominal_list_copy, listdic[count]) == 1:
                        print('Match found in simulation directory #', sim_directory)
                        match_found = 1
                        filename = run_directory + '\\' + sim_directory + '\\' + 'output.o'
                        datafiles[k] = datafile_prefix + '-' + str(k) + '.dat'
                        run_fail,TE11_amp,TE11_phase,HE11_amp,HE11_phase,HE12_amp,HE12_phase,Return_Loss = read_output_file(filename)

                        if plot_variable1 == 'TE11 Power':
                            data_array[i, j + 1] = TE11_amp**2
                        elif plot_variable1 == 'TE11 Phase':
                            data_array[i, j + 1] = TE11_phase
                        elif plot_variable1 == 'HE11 Power':
                            data_array[i, j + 1] = HE11_amp**2
                        elif plot_variable1 == 'HE11 Phase':
                            data_array[i, j + 1] = HE11_phase
                        if plot_variable1 == 'HE12 Power':
                            data_array[i, j + 1] = HE12_amp**2
                        elif plot_variable1 == 'HE12 Phase':
                            data_array[i, j + 1] = HE12_phase
                        elif plot_variable1 == 'Return Loss':
                            data_array[i, j + 1] = Return_Loss
                        
                        data_array[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                    count = count+1
                if match_found == 0:
                        print('Match failed')  
                        data_array[i, j + 1] = 0.0
                        data_array[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                    
        if datafiles[k] is not None:
            np.savetxt(datafiles[k],data_array,delimiter=',', fmt=' '.join(['%1.4f,']*(len(parameter2_range)+1)
                                                                   + ['%i,']*len(parameter2_range)))
        else:
            print('Simulations for this parameter are not yet complete')

    PlotUtils.create_gnuplot_file_3parameters_1variable(run_directory,datafiles,plot_variable1,plot_variable1_units,legend,
                                                        parameter1,parameter1_units,parameter1_range,
                                                        parameter2,parameter2_units,parameter2_range,
                                                        parameter3,parameter3_units,parameter3_range,
                                                        subplot_title,plot_title='',subplot_columns=subplot_columns,
                                                        plotxrange=plotxrange,plotyrange=plotyrange,labels=labels)
    return


def postprocess_3parameters_2variables(run_directory,listdic,var_range,var_list,plot_variable1,plot_variable1_units,plot_variable2,plot_variable2_units,
                                        parameter1,parameter1_units,parameter1_range,
                                        parameter2,parameter2_units,parameter2_range,
                                        parameter3,parameter3_units,parameter3_range,
                                        plotxrange ='[]', plotyrange = '[]', labels = 'False',subplot_columns = 3):
    import os, json
    import numpy as np
    import PlotUtils

    os.chdir(run_directory)

    legend1 = [None]*(len(parameter2_range))
    legend2 = [None]*(len(parameter2_range))
    
    for j in range(0, len(parameter2_range)):
        legend1[j] = (parameter2 + ' = ' + str(parameter2_range[j]))
        legend2[j] = (parameter2 + ' = ' + str(parameter2_range[j]))

    subplot_title = [None]*(len(parameter1_range))
    for k in range(0, len(parameter1_range)):
        subplot_title[k] = (parameter1 + ' = ' + str(parameter1_range[k]))

    datafiles1 = [None]*(len(parameter3_range))
    datafiles2 = [None]*(len(parameter3_range))

    datafiles_prefix = parameter3 + '-' + parameter2 + '-' + parameter1 
    datafiles_prefix.replace(" ", "-")


    data_array0 = np.zeros((len(parameter1_range),1+len(parameter2_range)+len(parameter2_range)))
    data_array1 = np.zeros((len(parameter1_range),1+len(parameter2_range)+len(parameter2_range)))

    var_nominal_list = json.load(open(run_directory + '\\NominalParameters.dict'))
    kcount = 0
    for k in range(0,len(parameter3_range)):
        datafiles1[kcount] = datafiles_prefix + '-' + plot_variable1 + '-'+ str(kcount) + '.dat'
        datafiles2[kcount] = datafiles_prefix + '-' + plot_variable2 + '-'+ str(kcount) + '.dat'

        data_array0 = np.zeros((len(parameter1_range), len(parameter2_range)+ 1 + len(parameter2_range)))
        data_array1 = np.zeros((len(parameter1_range), len(parameter2_range)+ 1 + len(parameter2_range)))
        # add additional column as the first column in parameter1
        # add additional len(range2) to include the folder # corresponding to the simulation results
        for i in range(0, len(parameter1_range)):
            data_array0[i, 0] = parameter1_range[i]
            data_array1[i, 0] = parameter1_range[i]

        sim_directories = next(os.walk('.'))[1]  # to just get directories and not files

        for i in range (0,len(parameter1_range)):
            for j in range (0,len(parameter2_range)):
                match_found = 0
                print('Searching for ', parameter1, ' = ', parameter1_range[i], ', ', parameter2, ' = ', parameter2_range[j], 'and ', parameter3, ' = ', parameter3_range[k])
                var_nominal_list_copy = var_nominal_list.copy()
                if parameter2 == 'Modes': parameter2_range[j] = list(parameter2_range[j])
                var_nominal_list_copy[parameter1][0] = parameter1_range[i]
                var_nominal_list_copy[parameter2][0] = parameter2_range[j]
                var_nominal_list_copy[parameter3][0] = parameter3_range[k]
                count = 0
                for sim_directory in sim_directories:
                    if dict_compare(var_nominal_list_copy, listdic[count]) == 1:
                        print('Match found in simulation directory #', sim_directory)
                        match_found = 1
                        filename = run_directory + '\\' + sim_directory + '\\' + 'output.o'
                        run_fail,TE11_amp,TE11_phase,HE11_amp,HE11_phase,HE12_amp,HE12_phase,Return_Loss = read_output_file(filename)

                        if plot_variable1 == 'TE11 Power':
                            data_array0[i, j + 1] = TE11_amp**2
                            data_array0[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                        elif plot_variable1 == 'TE11 Phase':
                            data_array0[i, j + 1] = TE11_phase
                            data_array0[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                        elif plot_variable1 == 'HE11 Power':
                            data_array0[i, j + 1] = HE11_amp**2
                            data_array0[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                        elif plot_variable1 == 'HE11 Phase':
                            data_array0[i, j + 1] = HE11_phase
                            data_array0[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                        elif plot_variable1 == 'HE12 POwer':
                            data_array0[i, j + 1] = HE12_amp**2
                            data_array0[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                        elif plot_variable1 == 'HE12 Phase':                        
                            data_array0[i, j + 1] = HE12_phase
                            data_array0[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                        elif plot_variable1 == 'Return_Loss':
                            data_array0[i, j + 1] = Return_Loss
                            data_array0[i, j + 1 + len(parameter2_range)] = int(sim_directory)

                        if plot_variable2 == 'TE11 Power':
                            data_array1[i, j + 1] = TE11_amp**2
                            data_array1[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                        elif plot_variable2 == 'TE11 Phase':
                            data_array1[i, j + 1] = TE11_phase
                            data_array1[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                        elif plot_variable2 == 'HE11 Power':
                            data_array1[i, j + 1] = HE11_amp**2
                            data_array1[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                        elif plot_variable2 == 'HE11 Phase':
                            data_array1[i, j + 1] = HE11_phase
                            data_array1[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                        elif plot_variable2 == 'HE12 Power':
                            data_array1[i, j + 1] = HE12_amp**2
                            data_array1[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                        elif plot_variable2 == 'HE12 Phase':                        
                            data_array1[i, j + 1] = HE12_phase
                            data_array1[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                        elif plot_variable2 == 'Return_Loss':
                            data_array1[i, j + 1] = Return_Loss
                            data_array1[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                    count = count+1
            if match_found == 0:
                    print('Match failed')  
                    data_array0[i, j + 1] = 0.0
                    data_array0[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                    data_array1[i, j + 1] = 0.0
                    data_array1[i, j + 1 + len(parameter2_range)] = int(sim_directory)

        np.savetxt(datafiles1[k],data_array0,delimiter=',', fmt=' '.join(['%1.4f,']*(len(parameter2_range)+1) + ['%i,']*len(parameter2_range)))
        np.savetxt(datafiles2[k],data_array1,delimiter=',', fmt=' '.join(['%1.4f,']*(len(parameter2_range)+1) + ['%i,']*len(parameter2_range)))
        kcount = kcount +1


    PlotUtils.create_gnuplot_file_3parameters_2variables(run_directory,datafiles1,plot_variable1,plot_variable1_units,legend1,datafiles2,plot_variable2,plot_variable2_units,legend2,
                                                        parameter1,parameter1_units,parameter1_range,
                                                        parameter2,parameter2_units,parameter2_range,
                                                        parameter3,parameter3_units,parameter3_range,
                                                        subplot_title,plot_title= '',subplot_columns=subplot_columns,
                                                        plotxrange=plotxrange,plotyrange=plotyrange,labels = labels)
    return


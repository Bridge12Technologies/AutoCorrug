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


def PPP_3V_1A(run_directory, listdic, var_range, var_list, plot_variable1, plot_variable1_units, parameter1,
                      parameter1_units, parameter1_range, parameter2, parameter2_units, parameter2_range,
                      parameter3, parameter3_units, parameter3_range,
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

    datafile_prefix = parameter3 + '-' + parameter2 + '-' + parameter1
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
                        # filename = listdic[count]['version_num'][0] + 'output.o'
                        filename = run_directory + '\\' + sim_directory + '\\' + 'output.o'
                        datafiles[k] = datafile_prefix + '-' + str(k) + '-power.dat'
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

    PlotUtils.create_subplot_files(run_directory, datafiles, plot_variable1, plot_variable1_units, parameter1,
                                      parameter1_units, parameter1_range, parameter2, parameter2_units,
                                      parameter2_range, parameter3, parameter3_units, parameter3_range,legend,
                                      subplot_title, plot_title = '', subplot_columns = subplot_columns,
                                      plotxrange = plotxrange, plotyrange = plotyrange,
                                      labels = labels)
    return


def PPP_1V_1A_P2Sing(runstamp, var_range, var_list, plot_variable1, plot_variable1_units, parameter1,
                               parameter1_units, parameter1_range, plotxrange ='[]',plotyrange = '[]',
                               labels = 'False'):
    import os, json
    import numpy as np
    import PlotUtils
    os.chdir(runstamp)
    run_directory = os.getcwd()

    data_array = np.zeros((len(parameter1_range),3))  # first Col-1 is primary variable, Col-2 is value, Col-3 is sim directory
    # add additional column as the first column in parameter1
    # add additional one column at the end to include the folder # corresponding to the simulation results
    for i in range(0, len(parameter1_range)):
        data_array[i, 0] = parameter1_range[i]

    for i in range (0,len(parameter1_range)):
        for sim_directory in next(os.walk('.'))[1]: # to just get directories and not files
            var_list = json.load(open(sim_directory + '\\parameter.dict'))
            if var_list[parameter1][0] == parameter1_range[i]:
                if plot_variable1 == 'Power':
                    filename = var_list['version_num'][0] + '.pwbal.out'
                    datafile ='Power-' + parameter1 + '-t1.dat'
                    ohm_loss, out_power, spent_beam_power, run_fail  = \
                        read_pwbal_file(run_directory + '\\' + sim_directory + '\\' +
                                                  filename, int(var_list['num_avg_z_points'][0]))
                    data_array[i, 1] = out_power
                    data_array[i, 2] = sim_directory

                elif plot_variable1 == "Frequency":
                    filename = 'freq_converge.log'
                    datafile = 'Frequency-' + parameter1 + '-t1.dat'
                    frequency_GHz = get_frequency(run_directory + '\\' + sim_directory + '\\' + filename)
                    data_array[i, 1] = frequency_GHz
                    data_array[i, 2] = sim_directory

    np.savetxt(datafile,data_array,delimiter=',',fmt=' '.join(['%1.4f,']*2 + ['%i,']))

    PlotUtils.create_type1_plot_files(run_directory, datafile, plot_variable1, plot_variable1_units,
                                      parameter1, parameter1_units, plotxrange = plotxrange, plotyrange = plotyrange,
                                      labels = labels)
    return

def PPP_1V_1A_P2Range(runstamp, var_range, var_list, plot_variable1, plot_variable1_units, parameter1,
                      parameter1_units, parameter1_range, parameter2, parameter2_units, parameter2_range,
                      plotxrange ='[]', plotyrange = '[]', labels = 'False'):
    import os, json
    import numpy as np
    import PlotUtils

    os.chdir(runstamp)
    run_directory = os.getcwd()

    data_array = np.zeros((len(parameter1_range), len(parameter2_range)+ 1 + len(parameter2_range)))
    # add additional column as the first column in parameter1
    # add additional len(range2) to include the folder # corresponding to the simulation results
    for i in range(0, len(parameter1_range)):
        data_array[i, 0] = parameter1_range[i]

    legend = [None]*(len(parameter2_range))

    for i in range (0,len(parameter1_range)):
        for j in range (0,len(parameter2_range)):
            match_found = 0
            legend[j] = (parameter2 + ' = ' + str(parameter2_range[j]))
            print('Searching for ', parameter1, ' = ', parameter1_range[i], 'and ', parameter2, ' = ', parameter2_range[j])
            for sim_directory in next(os.walk('.'))[1]: # to just get directories and not files
                var_list = json.load(open(sim_directory + '\\parameter.dict'))

                if parameter2 == 'Modes': parameter2_range[j] = list(parameter2_range[j])

                if var_list[parameter1][0] == parameter1_range[i] and var_list[parameter2][0] == parameter2_range[j]:
                    print('Match found in simulation directory #', sim_directory)
                    match_found = 1
                    if plot_variable1 == 'Power':
                        filename = var_list['version_num'][0] + '.pwbal.out'
                        datafile = 'power-t2.dat'
                        ohm_loss, out_power, spent_beam_power, run_fail  = \
                            read_pwbal_file(run_directory + '\\' + sim_directory + '\\' +
                                                      filename, int(var_list['num_avg_z_points'][0]))
                        data_array[i, j + 1] = out_power
                        data_array[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                        break

                    elif plot_variable1 == 'Frequency':
                        filename = 'freq_converge.log'
                        datafile = 'frequency-t2.dat'
                        frequency_GHz = get_frequency(run_directory + '\\' + sim_directory + '\\' + filename)
                        data_array[i, j + 1] = frequency_GHz
                        data_array[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                        break
            
            if match_found == 0:
                print('Match failed')  
                data_array[i, j + 1] = np.nan
                data_array[i, j + 1 + len(parameter2_range)] = np.nan  

    np.savetxt(datafile,data_array,delimiter=',', fmt=' '.join(['%1.4f,']*(len(parameter2_range)+1)
                                                               + ['%i,']*len(parameter2_range)))

    PlotUtils.create_type2_plot_files(run_directory, datafile, plot_variable1, plot_variable1_units, parameter1,
                                      parameter1_units, parameter1_range, parameter2, parameter2_units, parameter2_range, legend,
                                      plotxrange = plotxrange, plotyrange = plotyrange, labels = labels)
    return


def PPP_2V_2A_P2Range(runstamp, listdic, var_range, var_list, plot_variable1, plot_variable1_units, plot_variable2,
                               plot_variable2_units, parameter1, parameter1_units, parameter1_range, parameter2,
                               parameter2_units, parameter2_range, plotxrange ='[]',plotyrange = '[]', ploty2range = '[]',
                               labels = 'False', parameter1_parameter2_map_labels = 'False'):
    import os, json
    import numpy as np
    import PlotUtils

    os.chdir(runstamp)
    run_directory = os.getcwd()

    data_array = np.zeros((len(parameter1_range),len(parameter2_range)+1 + len(parameter2_range)))
    map_data_array = np.zeros((len(parameter1_range),2*len(parameter2_range)))

    # add additional column as the first column in parameter1
    # add additional len(range2) to include the folder # corresponding to the simulation results
    for i in range(0, len(parameter1_range)):
        data_array[i, 0] = parameter1_range[i]

    legend1 = [None]*(len(parameter2_range))
    for j in range(0, len(parameter2_range)):
        legend1[j] = (parameter2 + ' = ' + str(parameter2_range[j]))


    sim_directories = next(os.walk('.'))[1]  # to just get directories and not files
    var_nominal_list = json.load(open(run_directory + '\\NominalParameters.dict'))

    P1P2Mapfile = plot_variable2 + '-' + plot_variable1 + '-' + parameter1 + '-' + parameter2 + '.dat'
    with open(P1P2Mapfile, "w") as mapfile:
          
        datafile1 = parameter1 + '-' + parameter2 + '-' + plot_variable1 + '.dat'
        for i in range (0,len(parameter1_range)):
            tempstr = ''
            for j in range (0,len(parameter2_range)):
                match_found = 0
                print('Searching for ', parameter1, ' = ', parameter1_range[i], 'and ', parameter2, ' = ', parameter2_range[j])
                var_nominal_list_copy = var_nominal_list.copy()
                if parameter2 == 'Modes': parameter2_range[j] = list(parameter2_range[j])
                var_nominal_list_copy[parameter1][0] = parameter1_range[i]
                var_nominal_list_copy[parameter2][0] = parameter2_range[j]
                count=0
                for sim_directory in sim_directories:
                    if dict_compare(var_nominal_list_copy, listdic[count]) == 1:
                        print('Match found in simulation directory #', sim_directory)
                        match_found = 1
                        filename = listdic[count]['version_num'][0] + '.pwbal.out'
                        ohm_loss, out_power, spent_beam_power, run_fail  = \
                            read_pwbal_file(run_directory + '\\' + sim_directory + '\\' +
                                                        filename, int(listdic[count]['num_avg_z_points'][0]))
                        data_array[i, j + 1] = out_power
                        data_array[i, j + 1 + len(parameter2_range)] = int(sim_directory)

                        filename = 'freq_converge.log'
                        frequency_GHz = get_frequency(run_directory + '\\' + sim_directory + '\\' +
                                                        filename)
                        # map_data_array[i, 2*j] = frequency_GHz
                        map_data_array[i, 2*j+1] = out_power
                        if out_power < 0.001:
                            freq_GHz_str = '-'
                        else:
                            freq_GHz_str = str(frequency_GHz)

                        tempstr = tempstr + freq_GHz_str + ',' + str(out_power) + ',"(' + str(parameter1_range[i]) + ',' + str(parameter2_range[j]) + ')",'

                    count = count+1
                if match_found == 0:
                        print('Match failed')  
                        data_array[i, j + 1] = 0.0
                        data_array[i, j + 1 + len(parameter2_range)] = int(sim_directory)        
            mapfile.write(tempstr + '\n')

    np.savetxt(datafile1,data_array,delimiter=',', fmt=' '.join(['%1.4f,']*(len(parameter2_range)+1)
                                                               + ['%i,']*len(parameter2_range)))
 

    data_array = np.zeros((len(parameter1_range),len(parameter2_range)+1 + len(parameter2_range)))
    # add additional column as the first column in parameter1
    # add additional len(range2) to include the folder # corresponding to the simulation results
    for i in range(0, len(parameter1_range)):
        data_array[i, 0] = parameter1_range[i]

    legend2 = [None]*(len(parameter2_range))
    for j in range(0, len(parameter2_range)):
        legend2[j] = (parameter2 + ' = ' + str(parameter2_range[j]))

    datafile2 = parameter1 + '-' + parameter2 + '-' + plot_variable2 + '.dat'
    for i in range (0,len(parameter1_range)):
        for j in range (0,len(parameter2_range)):
            match_found = 0
            print('Searching for ', parameter1, ' = ', parameter1_range[i], 'and ', parameter2, ' = ', parameter2_range[j])
            var_nominal_list_copy = var_nominal_list.copy()
            if parameter2 == 'Modes': parameter2_range[j] = list(parameter2_range[j])
            var_nominal_list_copy[parameter1][0] = parameter1_range[i]
            var_nominal_list_copy[parameter2][0] = parameter2_range[j]
            count=0
            for sim_directory in sim_directories:
                if dict_compare(var_nominal_list_copy, listdic[count]) == 1:
                    print('Match found in simulation directory #', sim_directory)
                    match_found = 1
                    filename = 'freq_converge.log'
                    frequency_GHz = get_frequency(run_directory + '\\' + sim_directory + '\\' +
                                                    filename)
                    data_array[i, j + 1] = frequency_GHz
                    data_array[i, j + 1 + len(parameter2_range)] = int(sim_directory)
                count = count+1
        if match_found == 0:
                print('Match failed')  
                data_array[i, j + 1] = 0.0
                data_array[i, j + 1 + len(parameter2_range)] = int(sim_directory)  

    np.savetxt(datafile2,data_array,delimiter=',', fmt=' '.join(['%1.4f,']*(len(parameter2_range)+1) +
                                                               ['%i,']*len(parameter2_range)))

    PlotUtils.create_plot_files_2V_2A_P2Range_2Datafile(run_directory, datafile1, plot_variable1, plot_variable1_units, datafile2,
                                      plot_variable2, plot_variable2_units, parameter1, parameter1_units,
                                      parameter1_range, legend1, parameter2, parameter2_units, parameter2_range,
                                      legend2, plotxrange = plotxrange, plotyrange = plotyrange,
                                      ploty2range=ploty2range, labels = labels)

    PlotUtils.create_mapfile(run_directory, P1P2Mapfile, parameter1, parameter1_range, parameter1_units,
     parameter2, parameter2_range, parameter2_units, plot_variable1, plot_variable1_units,
                                      plot_variable2, plot_variable2_units, plotxrange = plotxrange, plotyrange = plotyrange,
                                      labels = parameter1_parameter2_map_labels)                                      

    return

